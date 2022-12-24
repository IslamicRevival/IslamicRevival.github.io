#!/usr/bin/env python3
import click
import logging
from pathlib import Path

# my Imports 
from youtube_transcript_api import YouTubeTranscriptApi
import urllib.parse as urlparse
import json
import traceback
import os
import re

from pyyoutube import Api


@click.command()
@click.option('-c','--channel-id')
#def main(channel_id="UC0uyPbeJ56twBLoHUbwFKnA"):
def main(channel_id="UC57cqHgR_IZEs3gx0nxyZ-g"):
    #api = Api(api_key="AIzaSyABaeCa_GEW4ePYNfYwP9qtsHAMN8s8kxs")
    api = Api(api_key="AIzaSyBdbQ-WPIkQkEad2EtRPfbRMiMURPxyqm8")  # Google Data (YouTube v3 key)
    channel_id = "UC57cqHgR_IZEs3gx0nxyZ-g"

    print ("\tFetch all the playlists")
    playlists_by_channel = api.get_playlists(channel_id=channel_id,count=None)
    print("\tFetch all the videos of the playlist")
    # playlists_videos = []
    # for playlist in playlists_by_channel.items:
    #     print("\t\tFetching videos IDs of playlist %s" %(playlist.id))
    #     playlists_videos.append(api.get_playlist_items(playlist_id=playlist.id,count=None))

    # videos_ids = []
    # for playlist in playlists_videos:
    #     for video in playlist.items:
    #         videos_ids.append(video.snippet.resourceId.videoId) 
    # print("We gathered now %s videos, saving save to file" %(len(videos_ids)))
    # with open("channel_id_file",'w') as f:
    #     json.dump(videos_ids,f)

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
    print(videos_ids)
    
    print("Save %s channel videos transcripts" % (channel_id) )
    
    for video_id in videos_ids:
        print ("The video ID is %s" % (video_id))
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)#,languages=['en']
            #transcript_list = [transcript for transcript in transcript_list\
            #                   if bool(re.match(transcript.language,"[en]*"))]
            video_transcripts = None
            for transcript in transcript_list:
                # the Transcript object provides metadata properties
                print("Video id : ", transcript.video_id)
                print("\tlanguage : %s , language code : %s" %(transcript.language,transcript.language_code))
                print("\tis_generated: %s, is_translatable: %s" %(transcript.is_generated,transcript.is_translatable))
                if transcript.language_code == 'en' and transcript.is_generated is False:
                    actual_transcript = transcript.fetch()
                    video_transcripts = actual_transcript
            
        except Exception as e:
            print(e)

    print("Finish main")
    

if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
    
    
    
    
    
    
    