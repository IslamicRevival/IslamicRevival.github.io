import os, time
import asyncio
import logging
import requests
from google.api_core.exceptions import InternalServerError 
from random import shuffle
from typing import List, Dict, Tuple

import openai  # Import OpenAI library
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

"""
## YouTube Transcript Summarizer

This script processes YouTube video transcripts, extracts key information, and generates a summarized markdown output.

**Features:**

- Processes single videos or entire channels.
- Extracts timestamps and generates questions from transcripts.
- Uses OpenAI or Gemini for advanced natural language processing.
- Option to simulate LLM processing with a local HuggingFace model.
- Stores processed video IDs to avoid redundant processing.

**Requirements:**
python3 -m pip install openai google-generativeai youtube-transcript-api langchain langchain_community langchain_huggingface requests
"""

# Configuration
YOUTUBE_API_KEY = '-' #'-'  # Replace with your actual API key
huggingfacehub_api_token = ''
GENAI_API_KEY = '' # https://www.cloudskillsboost.google/focuses/86502?catalog_rank=%7B%22rank%22%3A30%2C%22num_filters%22%3A1%2C%22has_search%22%3Atrue%7D&parent=catalog&search_id=38481400
OPENAI_API_KEY = 'sk-'
USE_PROXY = False  # Set to True to use proxies, False otherwise
USE_OPENAI = False  # Set to True to use OpenAI, False for Gemini
SIMULATE_LLM = False  # Set to True to use a local LLM (HuggingFaceHub), False for OpenAI/Gemini
MAX_VIDEOS_TO_PROCESS = None  # Set to an integer to limit the number of videos processed, None for no limit
run_final_summary_only = False  # Set to True to skip video processing

# Global variables
PROXIES = {}
PROCESSED_VIDEOS_FILE = "processed_videos.txt"
OUTPUT_MARKDOWN_FILE = "summary.md"  # File to store the summarized output


# Initialize loggers
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# --- LLM Configuration and Utilities ---
def initialize_llm():
    """Initializes and returns the selected LLM."""
    if SIMULATE_LLM:
        # Use a fast, local LLM for simulation 
        from langchain.prompts import PromptTemplate
        from langchain_community.llms import HuggingFaceHub
        from transformers import pipeline
        from langchain_huggingface import HuggingFacePipeline
        from langchain.text_splitter import RecursiveCharacterTextSplitter

        hf_pipeline = pipeline(
            "text2text-generation",
            model="google/flan-t5-xl",  # Consider a smaller model if Flan-T5-XL is too slow
            model_kwargs={
                "temperature": 1.0,  # Increase temperature for more randomness (less accuracy)
                "do_sample": True,
                "top_k": 40,       # Reduce top_k for faster sampling
                "num_beams": 1,     # Disable beam search (greedy decoding)
            },
            trust_remote_code=True,
            device=0  # Use GPU if available
        )
    
        # Create a Langchain LLM wrapper
        llm = HuggingFacePipeline(pipeline=hf_pipeline)
    elif USE_OPENAI:
        openai.api_key = OPENAI_API_KEY
        # Use OpenAI for content generation
        llm = openai.ChatCompletion
    else:
        genai.configure(api_key=GENAI_API_KEY)
        # Use Gemini for content generation
        llm = genai.GenerativeModel("gemini-1.5-flash") # gemini-1.5-pro  gemini-1.5-flash gemini-1.5-flash-8b
    return llm

# --- YouTube Data Retrieval ---
async def get_video_transcript(video_id: str) -> str:
    """Extracts and returns the transcript of a YouTube video."""
    try:
        if USE_PROXY:
            proxies = [f"http://{p}" for p in PROXIES.values()]
            shuffle(proxies)
        else:
            proxies = None

        for i in range(len(proxies)) if proxies else range(1):
            if proxies:
                proxy = proxies[i]
                logger.info(f"Trying proxy {proxy}")
            else:
                proxy = None

            try:
                transcript = await asyncio.wait_for(
                    asyncio.to_thread(
                        lambda: YouTubeTranscriptApi.get_transcript(
                            video_id, proxies={"http": proxy, "https": proxy} if proxy else None
                        )
                    ),
                    timeout=5,
                )
                return "\n".join(
                    [str(line["start"]) + "s : " + line["text"] for line in transcript]
                )
            except (
                YouTubeTranscriptApi.NoTranscriptAvailable,
                YouTubeTranscriptApi.NoTranscriptFound,
                YouTubeTranscriptApi.TranscriptsDisabled,
            ) as e:
                logger.error(f"No transcript found for video ID {video_id}: {e}")
                if not proxies:
                    break
            except asyncio.TimeoutError:
                logger.error(f"Timeout error for video ID {video_id}")
                await asyncio.sleep(1)
                continue
            except Exception as e:
                logger.error(f"General error for video ID {video_id}: {e}")
                await asyncio.sleep(1)
                continue
        return ""

    except Exception as e:
        logger.error(f"Error fetching transcript for video ID {video_id}: {e}")
        return ""

async def get_channel_video_ids(channel_id: str) -> List[str]:
    """Fetches and returns a list of video IDs from a YouTube channel."""
    video_ids = []
    next_page_token = None
    base_url = "https://www.googleapis.com/youtube/v3/search"

    while True:
        params = {
            "key": YOUTUBE_API_KEY,
            "channelId": channel_id,
            "part": "snippet",
            "type": "video",
            "maxResults": 50,  # Fetch up to 50 videos per request
            "pageToken": next_page_token
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()

            if "items" in data:
                for item in data["items"]:
                    video_ids.append(item["id"]["videoId"])

            if "nextPageToken" in data:
                next_page_token = data["nextPageToken"]
            else:
                break  # No more pages

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 403:  # Forbidden error
                logger.warning(f"YouTube API Forbidden error (likely invalid pageToken): {e}")
                break  # Stop fetching videos for this channel
            else:
                raise  # Re-raise other HTTP errors

    return video_ids

def generate_summary(transcript_text: str, prompt: str, llm) -> str:
    """Generates a summarized markdown output from the transcript."""
    if SIMULATE_LLM:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=450,  # Reduce chunk size to be well below 512
            chunk_overlap=50,  # You can adjust overlap as needed
            length_function=len,
        )
        transcript_chunks = text_splitter.create_documents([transcript_text])

        # Process each chunk and combine the results
        all_responses = []
        for chunk in transcript_chunks:
            formatted_prompt = prompt + "```\n" + chunk.page_content + "\n```"
            response = llm.invoke(formatted_prompt, max_new_tokens=200)  # Set max_new_tokens here
            all_responses.append(response)
        return "\n\n".join(all_responses)
    elif USE_OPENAI:
        # Use OpenAI for content generation
        response = llm.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt + transcript_text},
            ]
        )
        return response.choices[0].message['content']
    else:
        # Use Gemini for content generation
        for attempt in range(3):  # Try up to 3 times
            try:
                response = llm.generate_content(prompt + transcript_text)
                return response.text
            except InternalServerError as e:
                logger.warning(f"Gemini API Internal Server Error: {e}. Retrying (attempt {attempt + 1})...")
                time.sleep(5)  # Wait for 5 seconds before retrying
                logger.warning("Gemini API Internal Server Error persisted after multiple retries.")
                return ""  # Return an empty string to indicate failure


def process_transcript(transcript_text: str, video_url: str, llm) -> str:  # Add llm as argument
    """Processes the transcript to extract questions, generate summaries, and format the output."""
    prompt = """You are Youtube video summarizer. You will read the transcript text of a youtube video and extract questions that are asked.
    You will summarize each of those questions (to maximum of 100 words), always include the timestamp, and give a summary of the answer (maximum 100 words), 
    do not number the questions. Do not waste space with filler words such as 'The Speaker says' or "the speaker asks", do not create a section called 
    Summary just give the answer after the question. Keep it succint, remove any Ums or Ahs from the speakers. Format it all into markdown. 
    Add a category label under each question, it should be a succint keyword describing the content category.
    Please do that for the text given here:  """
    summary = generate_summary(transcript_text, prompt, llm)
    return summary  # Don't forget to return the summary

# --- State Management (Processed Videos) ---
def load_processed_videos() -> List[str]:
    """Loads the list of processed video IDs from the state file."""
    processed_videos = []
    if os.path.exists(PROCESSED_VIDEOS_FILE):
        with open(PROCESSED_VIDEOS_FILE, "r") as f:
            processed_videos = f.read().splitlines()
    return processed_videos

def save_processed_videos(processed_videos: List[str]):
    """Saves the updated list of processed video IDs to the state file."""
    with open(PROCESSED_VIDEOS_FILE, "w") as f:
        f.write("\n".join(processed_videos))

# --- Final LLM Processing ---
async def create_final_summary(input_md_file: str, output_md_file: str, llm):  # Add llm as a parameter

    """Processes the intermediate markdown file to create the final output."""
    with open(input_md_file, "r") as f:
        all_content = f.read()

    final_summary_prompt = f"""
You are a markdown document organizer. Your task is to take the content below, which consists of video summaries with timestamps and category 
labels, and transform it into a well-structured markdown document with a clickable table of contents and categorized questions. 
Please complete all the tasks of also adding all actual video content summaries within the designated sections below the relevant table of contents entries.  
Ensure you go to the end of all file, process all content, do not truncate.

**Here's how the output should be structured:**

1. **Table of Contents:**
   - The document should start with a numbered table of contents.
   - Each entry in the table of contents should be a category name followed by a link to the corresponding section in the document (using markdown link syntax).
   - Example:
     ```
     1. [Name & Language](#name-language)
     2. [Translation & Meaning](#translation-meaning)
     3. [Miracles & Theology](#miracles-theology)
     ```

2. **Categorized Sections:**
   - After the table of contents, the document should be divided into sections, one for each category.
   - Each section should have a heading with the category name (using `##` for the heading level).
   - Example:
     ```
     ## Name & Language
     ```

3. **Questions as Links:**
   - Within each category section, list the questions as clickable links to the corresponding video timestamps.
   - Use the video URL provided at the beginning of each question/answer block and append the timestamp to create the link.
   - The question text should be the link text.
   - Example:
     ```
     ### [What is the significance of the Greek writing of the name Issa?](https://www.youtube.com/watch?v=VIDEO_ID#t=TIMESTAMP)
     ```

4. **Answer Summaries:**
   - Below each question link, include the answer summary provided in the input content.

**Here is the actual content for you to generate:**

    ```
    {all_content}
    ```
    """

    # Directly invoke the LLM for the final summary
    if SIMULATE_LLM:
        final_summary = llm.invoke(final_summary_prompt, max_new_tokens=200) 
    else:  # Assuming this is for Gemini
        response = llm.generate_content(final_summary_prompt)
        final_summary = response.text

    with open(output_md_file, "w") as f:
        f.write(final_summary)

# --- Main Execution Flow ---
async def main():
    """Main function to orchestrate the video processing pipeline."""
    global PROXIES

    # Load previously processed videos
    processed_videos = load_processed_videos()

    # Initialize LLM
    llm = initialize_llm()

    if not run_final_summary_only:
        # Logic to handle single video vs. channel input
        #video_id = input("Enter a YouTube video ID or channel ID: ")
        #video_id = "https://www.youtube.com/watch?v=b6INC5e_jhw"
        video_id = "https://www.youtube.com/channel/UC0uyPbeJ56twBLoHUbwFKnA"
        # Extract Channel ID if a URL is provided
        if "/channel/" in video_id:
            video_id = video_id.split("/channel/")[1]  # Extract the part after "/channel/"

        if "watch?v=" in video_id:
            video_ids = video_id.split("watch?v=")[1]
        else:
            video_ids = await get_channel_video_ids(video_id)  # Pass the extracted Channel ID
            print(video_ids)

        # Open the output markdown file in append mode
        with open(OUTPUT_MARKDOWN_FILE, "a") as md_file:
            for video_id in video_ids:
                if video_id in processed_videos:
                    logger.info(f"Skipping already processed video: {video_id}")
                    continue

                if MAX_VIDEOS_TO_PROCESS is not None and len(processed_videos) >= MAX_VIDEOS_TO_PROCESS:
                    logger.info(f"Reached maximum number of videos to process: {MAX_VIDEOS_TO_PROCESS}")
                    break

                video_url = f"https://www.youtube.com/watch?v={video_id}"
                transcript_text = await get_video_transcript(video_id)

                if transcript_text:
                    # Process the transcript and generate the summary
                    summary = process_transcript(transcript_text, video_url, llm)

                    # Append the summary to the markdown file
                    md_file.write(f"## {video_url}\n\n{summary}\n\n")

                    # Update processed videos and save the state
                    processed_videos.append(video_id)
                    save_processed_videos(processed_videos)
                else:
                    logger.warning(f"No transcript found for video: {video_url}")
        
        await create_final_summary(OUTPUT_MARKDOWN_FILE, "final_summary.md", llm) 
    else:
         # Run only the final summary routine
        await create_final_summary(OUTPUT_MARKDOWN_FILE, "final_summary.md", llm)

if __name__ == "__main__":
    asyncio.run(main())