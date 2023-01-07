#!/usr/bin/env python3

import datetime
import logging
import os
import time

import requests
from markdownify import markdownify as md
import re
from pyyoutube import Api
from youtube_transcript_api import YouTubeTranscriptApi

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__file__)

API_KEY = os.getenv("API_KEY7")  # codespaces secrets
CHANNEL_ID = [
    "UC_SLXSHcCwK2RSZTXVL26SA",
    "UC0uyPbeJ56twBLoHUbwFKnA",
    "UC57cqHgR_IZEs3gx0nxyZ-g",
]  # bloggingtheology, docs, doc


def get_caption_markdown(video_id: str) -> list:
    """Get markdown list of captions for given video.

    Args:
        video_id: YouTube video id.

    Returns:
        List of markdown strings for each caption in the video.
    """
    captions = YouTubeTranscriptApi.get_transcript(video_id)
    return [
        "[{time}](https://youtu.be/{id}?t={seconds}) {text}\n".format(
            time=str(datetime.timedelta(seconds=int(c["start"]))),
            seconds=int(c["start"]),
            id=video_id,
            text=c["text"],
        )
        for c in captions
    ]


def get_preview_image(
    img_file_name: str, img_url: str, video_id: str, path: str
) -> Union[None, str]:
    """Save image to file and return file name.

    Args:
        img_file_name: Name to save the image file as.
        img_url: URL of image to download.
        video_id: YouTube video id.
        path: Path to save image to.

    Returns:
        File name of saved image. Returns None if image could not be fetched.
    """
    file_path = f"{path}/{img_file_name}"
    with open(file_path, "wb") as handle:
        headers = {
            "Content-Type": "application/json",
            "Referer": "*.[my-app].appspot.com/*",
        }
        response = requests.get(img_url, stream=True, headers=headers)

        if not response.ok:
            log.warning("Couldn't fetch preview: %s", response)
            return None

        for block in response.iter_content(1024):
            if not block:
                break
            handle.write(block)
        return file_path


def gen_markdown_page(
