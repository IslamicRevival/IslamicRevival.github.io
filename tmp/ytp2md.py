#!/usr/bin/env python3
import logging
from pathlib import Path

# my Imports 
from youtube_transcript_api import YouTubeTranscriptApi
import requests
from markdownify import markdownify as md
import re

from pyyoutube import Api


#def main(channel_id="UC0uyPbeJ56twBLoHUbwFKnA"):
def main(channel_id="UC57cqHgR_IZEs3gx0nxyZ-g"):
    #api = Api(api_key="AIzaSyABaeCa_GEW4ePYNfYwP9qtsHAMN8s8kxs")
    api = Api(api_key="AIzaSyBdbQ-WPIkQkEad2EtRPfbRMiMURPxyqm8")  # Google Data (YouTube v3 key)
    channel_id = "UC57cqHgR_IZEs3gx0nxyZ-g"

    videos_ids = []
    limit = 2
    count = 1
    try:
        print('Starting Fetching the Data for Channel:', channel_id)
        response = api.search(channel_id=channel_id, limit=limit, count=count)
        next_page_token = response.nextPageToken
        while next_page_token:
            for res in response.items:
                if res.id.videoId:
                    videos_ids.append(res.id.videoId)
                    print(res.id.videoId)

            next_page_token = response.nextPageToken
            response = api.search(
                channel_id=channel_id,
                limit=limit,
                count=count,
                page_token=next_page_token
            )
    except Exception as e:
        print('Error Getting Data:', e)
    video_ids= ['cRawmTCJeh0']
    print(videos_ids)
    
    
    for video_id in video_ids:
        print ("The video ID is %s" % (video_id))
        try:
            url = (f"https://www.summarize.tech/www.youtube.com/watch?v={video_id}")
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
            response = requests.get(url, headers=headers)
            #print(response.content)
            markdown = md(response.content, strip=['title', 'head', 'gtag', 'props', 'could not summarize', '<could not summarize>'])
            markdown = re.sub(r'\{\"props.*\"', '', markdown)
            markdown = re.sub(r'See more\* ','', markdown)
            markdown = re.sub(r'summary for:.*summarize.tech.*Summary','## Summary', markdown)
            markdown = re.sub(r'summarize.tech ','', markdown)
            markdown = re.sub(r'<could not summarize>','', markdown)
            markdown = re.sub(r'Summarize another video','', markdown)
            markdown = re.sub(r'.*gtag.*','',markdown)
            markdown = re.sub(r'.*dataLayer.*','',markdown)
            markdown = re.sub(r'.==.*','',markdown)
            print(markdown)

            #urllib.request.urlretrieve(url, video_id+'.html')
            print(url)

            # transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)#,languages=['en']
            # video_transcripts = None
            # for transcript in transcript_list:
            #     # the Transcript object provides metadata properties
            #     print()
            #     print("Video id : ", transcript.video_id)
            #     print("\tis_generated: %s, is_translatable: %s" %(transcript.is_generated,transcript.is_translatable))
            #     # if transcript.language_code == 'en' and transcript.is_generated is False:
            #     #     actual_transcript = transcript.fetch()
            #     #     video_transcripts = actual_transcript
            
        except Exception as e:
            print(e)

    print("Finish main")

   #https://www.summarize.tech/www.youtube.com/watch?v=cRawmTCJeh0 

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
    
    
    
    
    
    
    