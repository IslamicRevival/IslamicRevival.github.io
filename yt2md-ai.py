#!/usr/bin/env python3

import datetime
import logging
import os
import time

from pyyoutube import Api
from youtube_transcript_api import YouTubeTranscriptApi

import requests
import re

from markdownify import markdownify as md


API_KEY = os.getenv('API_KEY3') ## codespaces secrets
channel_ids_input = ["UC_SLXSHcCwK2RSZTXVL26SA", "UC0uyPbeJ56twBLoHUbwFKnA", "UC57cqHgR_IZEs3gx0nxyZ-g"]  ## bloggingtheology, docs, doc

logging.basicConfig(level=3, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()


def get_channel_video_ids(channel_id: str):
    """Get the video IDs for all videos in a channel.
    
    Args:
        channel_id (str): The ID of the YouTube channel.
        
    Returns:
        List[str]: A list of video IDs for all videos in the channel.
    """
    api = Api(api_key=API_KEY)
    playlists = api.get_playlists(channel_id=channel_id, count=200)
    video_ids = []
    for playlist in playlists.items:
        videos = api.get_playlist_items(playlist_id=playlist.id, count=200)
        for video in videos.items:
            video_id = video.snippet.resourceId.videoId
            video_ids.append(video_id)
    return video_ids

def get_caption_markdown(video_id: str):
    """Get the captions for a YouTube video in markdown format.
    
    Args:
        video_id (str): The ID of the YouTube video.
        
    Returns:
        List[str]: A list of strings containing the captions in markdown format.
    """
    captions = YouTubeTranscriptApi.get_transcript(video_id)
    markdown = [
        "[{time}](https://youtu.be/{id}?t={seconds}) {text}\n".format(
            time=str(datetime.timedelta(seconds=int(caption['start']))),
            seconds=int(caption['start']),
            id=video_id,
            text=caption["text"]
        ) for caption in captions
    ]

def get_preview_image(img_file_name:str, img_url: str, video_id: str, path: str) -> str:
    """
    Downloads an image from the given URL and saves it to the specified file path.

    Args:
        img_file_name (str): The file name for the image.
        img_url (str): The URL of the image.
        video_id (str): The ID of the video associated with the image.
        path (str): The file path to save the image to.
        
    Returns:
        str: The file name of the saved image. Returns None if the image could not be fetched.
    """
    with open(img_file_name, 'wb') as handle:
        headers = {'Content-Type': 'application/json','Referer': '*.[my-app].appspot.com/*'}
        response = requests.get(img_url, stream=True, headers=headers)

        if not response.ok:
            logger.warning("Couldn't fetch preview: %s", response)
            return None

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
        return img_file_name

def gen_markdown_page(video_id: str, title: str, description: str, smarkdown: str, path: str, date: datetime, captions: list) -> str:
    """
    Generates a markdown page for the given video information.

    Copy code
    Args:
        video_id (str): The ID of the video.
        title (str): The title of the video.
        description (str): The description of the video.
        smarkdown (str): The markdown content for the video.
        path (str): The file path to save the markdown page to.
        date (datetime): The date the video was uploaded.
        captions (list): A list of caption dictionaries, each containing 'start' and 'text' keys.
        
    Returns:
        str: The generated markdown page content.
    """
    markdown = ""

    markdown += f"# {title} ({date})\n\n"
    markdown += f"![alt {title}]({video_id}.jpg \"{title}\")\n\n"
    markdown += "## Description\n\n"
    markdown += description.strip()
    markdown += "\n\n"
    markdown += smarkdown.strip()
    markdown += "\n\n"
    markdown += "## Full transcript with timestamps\n\n"
    for c in captions:
        markdown += f"[{datetime.timedelta(seconds=int(c['start']))}](https://youtu.be/{video_id}?t={int(c['start'])}) {c['text']}  \n"
    return markdown          

def string_to_filename(filename: str, raw: bool = False):
    """
    Converts a string to a valid file name. If raw is True, all illegal characters will be removed.
    Otherwise, "?" will be replaced with "¿" and all other illegal characters will be replaced with "-".
    Any non-English characters will also be removed.

    Copy code
    Args:
        filename (str): The original file name.
        raw (bool, optional): Whether to remove all illegal characters or replace them with "¿" or "-". Defaults to False.

    Returns:
        str: The modified file name.
    """
    illegal_characters_in_file_names = r'"/\*?<>|:\' \#'

    if raw:
        return ''.join(c for c in filename if c not in illegal_characters_in_file_names)

    for x in [["?", "¿"]] + [[x, "_"] for x in illegal_characters_in_file_names.replace("?", "")]:
        filename = filename.replace(x[0], x[1])
        filename = filename.encode('ascii', errors='ignore').decode() # remove non-english
    return filename


def main(channel_ids=channel_ids_input):
    """Fetch metadata for all videos in the specified YouTube channels
    
    Args:
        channel_ids (list[str]): List of YouTube channel ids to fetch videos from.
    """
    for channel_id in channel_ids:
        api = Api(api_key=API_KEY)

        # TODO make the channel_id list a dict with paths
        if channel_id == 'UC_SLXSHcCwK2RSZTXVL26SA':
            path="content/blogging_theology/"
        else:
            path="content/massari/"

        videos_ids = []
        limit = 100
        count = 25
        try:
            logger.info(f"Fetching all vids in channel {channel_id}")
            response = api.search(channel_id=channel_id, limit=limit, count=count)
            next_page_token = response.nextPageToken
            while next_page_token:
                for res in response.items:
                    if res.id.videoId:
                        videos_ids.append(res.id.videoId)
                        #print(res.id.videoId)
                next_page_token = response.nextPageToken
                response = api.search(
                    channel_id=channel_id,
                    limit=limit,
                    count=count,
                    page_token=next_page_token
                )
        except Exception as E:
            logger.exception(f'Error getting vids for channel: {E}')
        vid_count = len(videos_ids)
        logger.info(f"Gathered {vid_count} videos for {channel_id} now pulling metadata for each video")
        #videos_ids= ['37K1mPnMIeE'] ## enter single video_id here if overridding full list for testing
        ## search for vids missing AI summary: grep -riL "AI" *.md

        for video_id in videos_ids:
            try:
                video_metadata = api.get_video_by_id(video_id=video_id).items[0]
                img_file_name = os.path.join(path, video_id) + '.jpg'
                title = video_metadata.snippet.title

                # check if video was already downloaded
                md_file_name = os.path.join(path, string_to_filename(title)) + '.md'
                if os.path.exists(md_file_name):
                    logging.warning(f"MD FILE FOR {video_id} {title} md already downloaded, skipping.")
                    continue
                #if os.path.exists(img_file_name):
                #    print(f"IMG FOR {video_id} img already downloaded, skipping. ", end="")
                #    continue
                preview_path = get_preview_image(img_file_name=img_file_name, img_url=video_metadata.snippet.thumbnails.default.url, video_id=video_id, path=path) 
                logging.info(f"\n\nVideo ID is {video_id} with title {title}")
                description = video_metadata.snippet.description
                date = datetime.datetime.strptime(video_metadata.snippet.publishedAt, "%Y-%m-%dT%H:%M:%S%z")
                captions = YouTubeTranscriptApi.get_transcript(video_id)

                # Get AI summary
                # from requests_html import HTMLSession
                url = f"https://www.summarize.tech/www.youtube.com/watch?v={video_id}"

                # sudo apt  install chromium-chromedriver --fix-missing
                # wget https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip
                from selenium import webdriver
                from selenium.webdriver.chrome.options import Options
                from selenium.webdriver.support.ui import WebDriverWait
                from selenium.webdriver.common.by import By
                from selenium.webdriver.support import expected_conditions as EC

                ## configure webdriver
                options = Options()
                options.headless = True  # hide GUI
                options.add_argument('--headless')
                options.add_argument('--disable-infobars')
                options.add_argument('--no-sandbox')
                #options.add_argument('--remote-debugging-port=9222')
                #options.add_argument("--window-size=1920,1080")  # set window size to native GUI size
                #options.add_argument("--start-maximized")  # ensure window is full-screen
                options.add_argument("--disable-extensions")
                options.add_argument("--disable-gpu")
                options.add_argument("--disable-dev-shm-usage")
                options.binary_location = "/usr/bin/google-chrome-stable"    #chrome binary location specified here

                # configure chrome browser to not load images and javascript
                chrome_options = webdriver.ChromeOptions()
                chrome_options.add_argument('--headless')
                #chrome_options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2}) 
                #chrome_options.add_argument("--disable-setuid-sandbox") 
                #chrome_options.add_argument("--remote-debugging-port=9222")  # this
                chrome_options.add_argument("--disable-extensions") 
                chrome_options.add_argument("--disable-gpu") 
                #chrome_options.add_argument("--start-maximized") 
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                #chrome_options.add_argument('--profile-directory=Default')  # use default Chrome browser profile
                chrome_options.binary_location = "/usr/bin/google-chrome-stable"  # specify chrome binary location

                # start the webdriver and load the webpage
                driver = webdriver.Chrome('./chromedriver', options=options, chrome_options=chrome_options)
                driver.get(url)
                wait = WebDriverWait(driver, 30)
                wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
                #wait.until(EC.presence_of_element_located((By.ID,"__NEXT_DATA__")))
                time.sleep(20) #sleep for X sec
                mdresponse = driver.page_source
                driver.close()
                driver.quit()

                # find ./ -type f -name "*.md" -exec sed -i 's/*  discusses / Discusses /g' {} \;
                smarkdown = md(mdresponse, strip=['title', 'head', 'gtag', 'props', 'could not summarize', '<could not summarize>', 'In this video,', 'in this video,',
                    'In this YouTube video','The video', 'This video', 'According to this video,', 'This short video', 'This YouTube video is titled', 'The YouTube video', 'In this video,', ' In this short video,',
                    'The speaker in the video ', 'The speaker ', 'This YouTube video ', 'In the video, ', 'In the YouTube video ', 'The author ', 'The main points of this video are that ', 'The narrator of this video ' ])
                smarkdown = re.sub(r'\* of this video ', '', smarkdown)
                smarkdown = re.sub(r'\*\s+discusses ', ' Discusses', smarkdown)
                smarkdown = re.sub(r'\{\"props.*\"', '', smarkdown)
                smarkdown = re.sub(r'See more\* ','', smarkdown)
                smarkdown = re.sub(r'summary for:.*summarize.tech.*Summary','## Summary', smarkdown)
                smarkdown = re.sub(r'summarize.tech ','', smarkdown)
                smarkdown = re.sub(r'<could not summarize>','', smarkdown)
                smarkdown = re.sub(r'Summarize another video','', smarkdown)
                smarkdown = re.sub(r'.*gtag.*','', smarkdown)
                smarkdown = re.sub(r'.*dataLayer.*','', smarkdown)
                smarkdown = re.sub(r'.==.*','', smarkdown)
                print(smarkdown)

                with open(md_file_name, 'w') as handle:
                        handle.write(
                    gen_markdown_page(video_id=video_id,
                                    title=title,
                                    path=preview_path,
                                    smarkdown=smarkdown,
                                    description=description,
                                    date=date,
                                    captions=captions))
            except Exception as e:
                print(e)
        print(f"Finished processing videos and md for {channel_id}")
    

if __name__ == '__main__':
    #get_transcript()
    main()