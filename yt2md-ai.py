#!/usr/bin/env python3

import datetime
import logging
import os
import time

import re

from markdownify import markdownify as md
from pyyoutube import Api ## Needs Google Data (YouTube v3 key)
from youtube_transcript_api import YouTubeTranscriptApi

import requests

API_KEY = os.getenv('API_KEY2') ## codespaces secrets 1-12
channel_ids_input = ["UC0uyPbeJ56twBLoHUbwFKnA", "UC57cqHgR_IZEs3gx0nxyZ-g", 'UCo5TlU2TZWVDsAlGI94QCoA', "UCeZBhrU8xHcik0ZgtDwjsdA", "UCHDFNoOk8WOXtHo8DIc8efQ", "UC_SLXSHcCwK2RSZTXVL26SA"]  ## thought_adv, sapience, hijab, bloggingtheology, docs, doc

logging.basicConfig(level=15, format='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()

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
        headers = {'Content-Type': 'application/json','Referer': '*.my-app.appspot.com/*'}
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
    markdown += f"<iframe loading='lazy' allow='autoplay' src='https://www.youtube.com/embed/{video_id}'></iframe>"
    markdown += "\n\n## Description\n\n"
    markdown += description.strip()
    markdown += "\n\n"
    markdown += smarkdown.strip()
    markdown += "\n\n"
    markdown += "<details><summary><h2>Full transcript with timestamps: CLICK TO EXPAND</h2></summary>\n\n"
    for c in captions:
        #markdown += f"[{datetime.timedelta(seconds=int(c['start']))}](https://youtu.be/{video_id}?t={int(c['start'])}) {c['text']}  \n"
        markdown += f'<a onclick="modifyYTiframeseektime('
        markdown += f"'{int(c['start'])}')"
        markdown += f'">'
        markdown += f"{datetime.timedelta(seconds=int(c['start']))} {c['text']}</a>\n"
    markdown += "</details>"
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
    illegal_characters_in_file_names = r'"/\*?<>|:_\' \#.~!'

    if raw:
        return ''.join(c for c in filename if c not in illegal_characters_in_file_names)

    for x in [["?", "¿"]] + [[x, "_"] for x in illegal_characters_in_file_names.replace("?", "")]:
        filename = filename.replace(x[0], x[1])
        filename = filename.encode('ascii', errors='ignore').decode() # remove non-english
    return filename

def yt_time(duration="P1W2DT6H21M32S"):
    """
    Converts YouTube duration (ISO 8061)
    into Seconds

    see http://en.wikipedia.org/wiki/ISO_8601#Durations
    """
    ISO_8601 = re.compile(
        'P'   # designates a period
        '(?:(?P<years>\d+)Y)?'   # years
        '(?:(?P<months>\d+)M)?'  # months
        '(?:(?P<weeks>\d+)W)?'   # weeks
        '(?:(?P<days>\d+)D)?'    # days
        '(?:T' # time part must begin with a T
        '(?:(?P<hours>\d+)H)?'   # hours
        '(?:(?P<minutes>\d+)M)?' # minutes
        '(?:(?P<seconds>\d+)S)?' # seconds
        ')?')   # end of time part
    # Convert regex matches into a short list of time units
    units = list(ISO_8601.match(duration).groups()[-3:])
    # Put list in ascending order & remove 'None' types
    units = list(reversed([int(x) if x != None else 0 for x in units]))
    # Do the maths
    return sum([x*60**units.index(x) for x in units])

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
        elif channel_id =='UCHDFNoOk8WOXtHo8DIc8efQ':
            path="content/hijab/"
        elif channel_id =='UCeZBhrU8xHcik0ZgtDwjsdA':
            path='content/sapience/'
        elif channel_id == 'UCo5TlU2TZWVDsAlGI94QCoA':
            path='content/thought_adventure'
        else:
            path="content/massari/"

        videos_ids = []
        limit = 10
        count = 25
        length = 600 ## only interested in vids > 10minutes
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
                    page_token=next_page_token,
                    order="date"
                )
        except Exception as exception:
            logger.warn(f'Error getting vids for channel: {exception}', exc_info=True)
        vid_count = len(videos_ids)
        logger.info(f"Gathered {vid_count} videos for {channel_id} now pulling metadata for each video")
        #videos_ids= ['37K1mPnMIeE'] ## enter single video_id here if overridding full list for testing
        ## search for vids missing AI summary: grep -riL "AI" *.md

        for video_id in videos_ids:
            try:
                video_metadata = api.get_video_by_id(video_id=video_id).items[0]
                title = video_metadata.snippet.title
                duration = video_metadata.contentDetails.duration
                if yt_time(duration) < length:
                    logging.info(f"SKIPPING: short video: {duration} {title}")
                    continue

                # check if video was already downloaded
                md_file_name = os.path.join(path, string_to_filename(title)) + '.md'
                if os.path.exists(md_file_name):
                    logging.info(f"SKIPPING: MD file file {video_id} {title} md already downloaded")
                    continue

                #img_file_name = os.path.join(path, video_id) + '.jpg'
                #if os.path.exists(img_file_name):
                #    print(f"IMG FOR {video_id} img already downloaded, skipping. ", end="")
                #    continue
            
                #preview_path = get_preview_image(img_file_name=img_file_name, img_url=video_metadata.snippet.thumbnails.default.url, video_id=video_id, path=path) 
                preview_path = 'tmp/'
                logging.info(f"\n\nVideo ID is {video_id} with title {title}")
                description = video_metadata.snippet.description
                date = datetime.datetime.strptime(video_metadata.snippet.publishedAt, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
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
                wait = WebDriverWait(driver, 50)
                #wait.until(EC.presence_of_element_located((By.TAG_NAME,"h1")))
                wait.until(EC.presence_of_element_located((By.ID,"__NEXT_DATA__")))
                time.sleep(20) #sleep for X sec
                mdresponse = driver.page_source
                driver.close()
                driver.quit()
                # grep -rL "AI" *.md|xargs rm -f ##find and rm missing AI
                # find ./ -type f -name "*.md" -exec sed -i 's/loading='lazy'\/loading='lazy' allow='autoplay' /g' {} \;
                # find . -type f -name "*.md" -exec sed -ie 's/<\/details>\([^ ]*\)$//g' {} \; 
                # find . -type f -name "*.md" -exec sed -i "s/\[\([^]]*\)\](https.*t=\([0-9]*\))\s*-\s*\[\([^]]*\)\](https.*t=\([0-9]*\))/<a onclick=\"modifyYTiframeseektime('\2')\">\1<\/a> - <a onclick=\"modifyYTiframeseektime('\4')\">\3<\/a>/g" {} \;
                # find . -type f -name "*.md" -exec sed -i "s/\[\(.*\)\](https.*t=\([0-9]*\))/<a onclick=\"modifyYTiframeseektime('\2')\">\1<\/a>/g" {} \; # TODO do s/r in python of this

                smarkdown = md(mdresponse, strip=['title', 'head', 'gtag', 'props', 'could not summarize', '<could not summarize>', 'js', 'config'])
                # list of AI NLP words to remove
                words_to_remove = ['title', 'head', 'gtag', 'props', 'could not summarize', '<could not summarize>', 'In this video,', 'in this video,',
                                    'In this YouTube video','The video', 'This video', 'According to this video,', 'This short video', 'This YouTube video is titled', 'The YouTube video', 'In this video,', ' In this short video,',
                                    'The speaker in the video ', 'The speaker ', 'This YouTube video ', 'In the video, ', 'In the YouTube video ', 'The author ', 'The main points of this video are that ', 'The narrator of this video ',
                                    ' The video ', ' In this YouTube video, ', 'In this video, ', 'summarize.tech ', 'Summarize another video', '[Music]']

                # remove each word from the string
                for word in words_to_remove:
                    smarkdown = smarkdown.replace(word, "")

                smarkdown = re.sub(r'\* of this video ', ' ', smarkdown)
                smarkdown = re.sub(r'\*\s+discusses ', ' Discusses ', smarkdown)
                smarkdown = re.sub(r'\{\"props.*\"', '', smarkdown)
                smarkdown = re.sub(r'See more\* ','', smarkdown)
                smarkdown = re.sub(r'summary for:.*summarize.tech.*Summary','## Summary', smarkdown)
                smarkdown = re.sub(r'.*gtag.*','', smarkdown)
                smarkdown = re.sub(r'.*new Date.*','', smarkdown)
                smarkdown = re.sub(r'.*config\', \'G-.*','', smarkdown)
                smarkdown = re.sub(r'.*dataLayer.*','', smarkdown)
                smarkdown = re.sub(r'.==.*','', smarkdown)
                smarkdown = re.sub(r"\[([^]]*)\]\(https.*t=([0-9]*)\)\s*-\s*\[([^]]*)\]\(https.*t=([0-9]*)\)", r'<a onclick="modifyYTiframeseektime(\2)">\1</a> - <a onclick="modifyYTiframeseektime(\4)">\3</a>\n', smarkdown)
                smarkdown = re.sub(r"\[(.*)\]\(https.*t=([0-9]*)\)", r'<a onclick="modifyYTiframeseektime(\2)">\1</a>\n', smarkdown)
                smarkdown = re.sub(r'\[(.*)\]<','\1', smarkdown)
                smarkdown = re.sub(r'This is an AI generated summary. There may be inaccuracies', '\n\n<span style="color:red; font-size:125%">This summary is AI generated - there may be inaccuracies</span>', smarkdown)
                if not "AI generated" in smarkdown:
                    logging.warn("SKIPPING: no summary markdown generated")
                    continue
                logging.info(smarkdown)

                with open(md_file_name, 'w') as handle:
                        handle.write(
                    gen_markdown_page(video_id=video_id,
                                    title=title,
                                    path=preview_path,
                                    smarkdown=smarkdown,
                                    description=description,
                                    date=date,
                                    captions=captions))
            except Exception as exception:
                logging.warn(exception, exc_info=True)
        print(f"Finished processing videos and md for {channel_id}")
    

if __name__ == '__main__':
    #get_transcript()
    main()
