#!/usr/bin/env python3

import datetime
import logging
import os
import json
import re

import click
import requests

from py_youtube import Data ## doesn't need API key

import pyyoutube  ## Needs Google Data (YouTube v3 key)
from pyyoutube import Api

from youtube_transcript_api import YouTubeTranscriptApi

## sample run: ./yt2md.py -u https://www.youtube.com/watch?v=39Vep9aTNa4

API_KEY = "AIzaSyBdbQ-WPIkQkEad2EtRPfbRMiMURPxyqm8"  # Google Data (YouTube v3 key)
CHANNEL_ID = ['UC0uyPbeJ56twBLoHUbwFKnA']

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

def get_preview_image(img_url: str, video_id: str, path: str):
    img_file_name = os.path.join(path, video_id) + '.jpg'
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

    return None


def gen_markdown_page(video_id: str, title: str, description: str, path: str, date: datetime, captions: list):
    markdown = ""

    markdown += "# {title} ({date})\n\n".format(title=title, date=date)
    markdown += "![alt {title}]({video_id}.jpg \"{title}\")\n\n".format(title=title, video_id=video_id)
    markdown += "## Description\n\n"
    markdown += description.strip()
    markdown += "\n\n"
    markdown += "## Transcript\n\n"
    for c in captions:
        markdown += "[{time}](https://youtu.be/{id}?t={seconds}) {text}  \n".format(time=str(
            datetime.timedelta(seconds=int(c['start']))),
                                                                                    seconds=int(c['start']),
                                                                                    id=video_id,
                                                                                    text=c["text"])

    return markdown

def string_to_filename(filename, raw=False):
    """if raw, will delete all illegal characters. Else will replace '?' with '¿' and all others with '-'"""
    illegal_characters_in_file_names = r'"/\*?<>|:\' '

    if raw:
        return ''.join(c for c in filename if c not in illegal_characters_in_file_names)

    for x in [["?", "¿"]] + [[x, "_"] for x in illegal_characters_in_file_names.replace("?", "")]:
        filename = filename.replace(x[0], x[1])
        filename = filename.encode('ascii', errors='ignore').decode() # remove non-english
    return filename


@click.group()
@click.option('-v', '--verbosity', help='Verbosity', default=0, count=True)
def cli(verbosity: int):
    _configure_logging(verbosity)
    return 0

@cli.command()
#@click.option('-i', '--video_id', help='url of the youtube video')
@click.option('-d', '--path', help='dir to output the markdown and thumbnail', default="content/transcripts")
@click.option('-c', '--channel_id', help='get all vids in a channel', default="UC0uyPbeJ56twBLoHUbwFKnA")

def get_transcript_by_vid_id(video_id: str, path: str, channel_id: str):
    api = Api(api_key="AIzaSyABaeCa_GEW4ePYNfYwP9qtsHAMN8s8kxs")
    video_metadata = api.get_video_by_id(video_id=video_id).items[0]
    title = video_metadata.snippet.title
    preview_path = get_preview_image(img_url=video_metadata.snippet.thumbnails.default.url, video_id=video_id, path=path)

    # check if video was already downloaded
    if os.path.exists(preview_path):
            print("video was already downloaded because thumbnail already exists, skipping")
           # return

    description = video_metadata.snippet.description
    date = datetime.datetime.strptime(video_metadata.snippet.publishedAt, "%Y-%m-%dT%H:%M:%S%z")
    captions = YouTubeTranscriptApi.get_transcript(video_id)

    md_file_name = os.path.join(path, string_to_filename(title)) + '.md'
    with open(md_file_name, 'w') as handle:
            handle.write(
        gen_markdown_page(video_id=video_id,
                          title=title,
                          path=preview_path,
                          description=description,
                          date=date,
                          captions=captions))
    return None

#def main(channel_id="UC0uyPbeJ56twBLoHUbwFKnA"):
def main(channel_id="UC57cqHgR_IZEs3gx0nxyZ-g"):

    api = Api(api_key="AIzaSyABaeCa_GEW4ePYNfYwP9qtsHAMN8s8kxs")
    path="content/transcripts/"
    print ("\tFetch all the playlists")
    playlists_by_channel = api.get_playlists(channel_id=channel_id,count=None)
    print("\tFetch all the videos of the playlist")
    playlists_videos = []
    for playlist in playlists_by_channel.items:
        print("\t\tFetching videos IDs of playlist %s" %(playlist.id))
        playlists_videos.append(api.get_playlist_items(playlist_id=playlist.id,count=None))

    videos_ids = []
    for playlist in playlists_videos:
        for video in playlist.items:
            videos_ids.append(video.snippet.resourceId.videoId) 
    print("We gathered now %s videos, saving save to file" %(len(videos_ids)))
    with open("yt2md-channel_id_file",'w') as f:
        json.dump(videos_ids,f)
        
    print("Save %s channel videos transcripts" % (channel_id) )
    
    for video_id in videos_ids:
        print ("The video ID is %s" % (video_id))
        try:
            video_metadata = api.get_video_by_id(video_id=video_id).items[0]
            title = video_metadata.snippet.title
            preview_path = get_preview_image(img_url=video_metadata.snippet.thumbnails.default.url, video_id=video_id, path=path)

            # check if video was already downloaded
            if os.path.exists(preview_path):
                    print("video was already downloaded because thumbnail already exists, skipping")
                # return

            description = video_metadata.snippet.description
            date = datetime.datetime.strptime(video_metadata.snippet.publishedAt, "%Y-%m-%dT%H:%M:%S%z")
            captions = YouTubeTranscriptApi.get_transcript(video_id)

            md_file_name = os.path.join(path, string_to_filename(title)) + '.md'
            with open(md_file_name, 'w') as handle:
                    handle.write(
                gen_markdown_page(video_id=video_id,
                                title=title,
                                path=preview_path,
                                description=description,
                                date=date,
                                captions=captions))
        except Exception as e:
            print(e)

    print("Finish main")
    

if __name__ == '__main__':
    #get_transcript()
    main()