#!/usr/bin/env python3

import datetime
import logging
import os
import time
               

import requests
from markdownify import markdownify as md
import re

from py_youtube import Data ## doesn't need API key

import pyyoutube  ## Needs Google Data (YouTube v3 key)
from pyyoutube import Api

from youtube_transcript_api import YouTubeTranscriptApi

## sample run: ./yt2md.py -u https://www.youtube.com/watch?v=39Vep9aTNa4

API_KEY = os.getenv('API_KEY7') ## codespaces secrets
CHANNEL_ID = ["UC_SLXSHcCwK2RSZTXVL26SA", "UC0uyPbeJ56twBLoHUbwFKnA", "UC57cqHgR_IZEs3gx0nxyZ-g"] # bloggingtheology, docs, doc
#CHANNEL_ID = ["UC_SLXSHcCwK2RSZTXVL26SA"] # doc, bloggingtheology,


log = logging.getLogger(__file__)

def _configure_logging(verbosity: int):
    loglevel = max(3 - verbosity, 0) * 10
    logging.basicConfig(level=loglevel, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    if loglevel >= logging.DEBUG:
        # Disable debugging logging for external libraries
        for loggername in 'urllib3':
            logging.getLogger(loggername).setLevel(logging.CRITICAL)

def get_channel_video_ids(channelId: str):
    api = pyyoutube.Api(api_key=API_KEY)
    pl = api.get_playlists( channel_id =channelId , count=200)

    #all_videos = []
    for j,i in enumerate(pl.items):
        #print(f"-- Loading - {j} Playlist")
        videos = api.get_playlist_items(playlist_id=i.id , count=200)

        for k,vid in enumerate(videos.items):
            vidId = vid.snippet.resourceId.videoId
            print(vidId)

def get_caption_markdown(video_id: str):
    captions = YouTubeTranscriptApi.get_transcript(video_id)
    return [
        "[{time}](https://youtu.be/{id}?t={seconds}) {text}\n".format(time=str(
            datetime.timedelta(seconds=int(c['start']))),
                                                                      seconds=int(c['start']),
                                                                      id=video_id,
                                                                      text=c["text"]) for c in captions
    ]

def get_preview_image(img_file_name:str, img_url: str, video_id: str, path: str):
    with open(img_file_name, 'wb') as handle:
        headers = {'Content-Type': 'application/json','Referer': '*.[my-app].appspot.com/*'}
        response = requests.get(img_url, stream=True, headers=headers)

        if not response.ok:
            log.warning("Couldn't fetch preview: %s", response)
            return None

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
        return img_file_name


def gen_markdown_page(video_id: str, title: str, description: str, smarkdown: str, path: str, date: datetime, captions: list):
    markdown = ""

    markdown += "# {title} ({date})\n\n".format(title=title, date=date)
    markdown += "![alt {title}]({video_id}.jpg \"{title}\")\n\n".format(title=title, video_id=video_id)
    markdown += "## Description\n\n"
    markdown += description.strip()
    markdown += "\n\n"
    markdown += smarkdown.strip()
    markdown += "\n\n"
    markdown += "## Full transcript with timestamps\n\n"
    for c in captions:
        markdown += "[{time}](https://youtu.be/{id}?t={seconds}) {text}  \n".format(time=str(
            datetime.timedelta(seconds=int(c['start']))),
                                                                                    seconds=int(c['start']),
                                                                                    id=video_id,
                                                                                    text=c["text"])

    return markdown

def string_to_filename(filename, raw=False):
    """if raw, will delete all illegal characters. Else will replace '?' with '¿' and all others with '-'"""
    illegal_characters_in_file_names = r'"/\*?<>|:\' \#'

    if raw:
        return ''.join(c for c in filename if c not in illegal_characters_in_file_names)

    for x in [["?", "¿"]] + [[x, "_"] for x in illegal_characters_in_file_names.replace("?", "")]:
        filename = filename.replace(x[0], x[1])
        filename = filename.encode('ascii', errors='ignore').decode() # remove non-english
    return filename

def main(channel_ids=CHANNEL_ID):

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
            print(f"Fetching all vids in channel {channel_id}")
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
        except Exception as e:
            print('Error getting vids for channel:', e)
        vid_count = len(videos_ids)
        print(f"Gathered {vid_count} videos for {channel_id} now pulling metadata for each video" )
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
                    print(f"MD FILE FOR {video_id} {title} md already downloaded, skipping. ", end="")
                    continue
                #if os.path.exists(img_file_name):
                #    print(f"IMG FOR {video_id} img already downloaded, skipping. ", end="")
                #    continue
                preview_path = get_preview_image(img_file_name=img_file_name, img_url=video_metadata.snippet.thumbnails.default.url, video_id=video_id, path=path) 
                print(f"\n\nVideo ID is {video_id} with title {title}")
                description = video_metadata.snippet.description
                date = datetime.datetime.strptime(video_metadata.snippet.publishedAt, "%Y-%m-%dT%H:%M:%S%z")
                captions = YouTubeTranscriptApi.get_transcript(video_id)

                ## Get AI summary
                ## from requests_html import HTMLSession
                url = f"https://www.summarize.tech/www.youtube.com/watch?v={video_id}"

                ## sudo apt  install chromium-chromedriver --fix-missing
                ## wget https://chromedriver.storage.googleapis.com/108.0.5359.71/chromedriver_linux64.zip
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

                ## configure chrome browser to not load images and javascript
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
                #chrome_options.add_experimental_option(
                #    # this will disable image loading
                #    "prefs", {"profile.managed_default_content_settings.images": 2}
                #)

                driver = webdriver.Chrome('./chromedriver', options=options, chrome_options=chrome_options)
                driver.get(url)
                wait = WebDriverWait(driver, 30)
                wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
                #wait.until(EC.presence_of_element_located((By.ID,"__NEXT_DATA__")))
                time.sleep(20) #sleep for X sec
                mdresponse = driver.page_source
                driver.close()
                driver.quit()

                # find ./ -type f -name "*.md" -exec sed -i 's/The author //g' {} \;
                smarkdown = md(mdresponse, strip=['title', 'head', 'gtag', 'props', 'could not summarize', '<could not summarize>', 'In this video,', 'in this video,',
                    'In this YouTube video','The video', 'This video', 'According to this video,', 'This short video', 'This YouTube video is titled', 'The YouTube video', 'In this video,', ' In this short video,',
                    'The speaker in the video ', 'The speaker ', 'This YouTube video ', 'In the video, ', 'In the YouTube video ', 'The author ' ])
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