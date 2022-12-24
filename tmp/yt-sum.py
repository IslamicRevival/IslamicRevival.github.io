from gensim.summarization.summarizer import summarize
from gensim.summarization import keywords
import os
from youtube_transcript_api import YouTubeTranscriptApi

def main():

# input Youtube link

    Videolink = "https://youtu.be/htLprHRqzTY"

    #selecting summarization technique


#retrieving and arranging transcript

    video_id = Videolink.split("=")[1]
    YouTubeTranscriptApi.get_transcript(video_id)
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    result = ""
    for i in transcript:
        result += '\n. ' + i['text']
    print("Using Gensim Summarizer...")

    #printing transcript backend

    print(transcript)

# printing summary
# percentage summary

    summary = summarize(result, ratio = 100/100)
    print(summary)

# word count summary
    summary = summarize(result, word_count = 10000)
    print(summary)

# original transcript

    print(result) #backend


if __name__ == '__main__':
    main()