"""
TODO: create json file with all information, then seperate class that converts json to md. that way, files can be updated / recreated in a new format later, and analyzed (machine-readable)
"""

from os.path import join as joinpath
from datetime import datetime as datetime2
import sys
import requests
import os
import ffmpeg
import pytube
from math import ceil
from constants import *
import shutil
from captions import download_transcript
from utils import string_to_filename

# URL of the video to be downloaded

url = "https://www.youtube.com/watch?v=39Vep9aTNa4"


def select_streams(video):
    """Return the video stream that best matches mime type and resolution preferences with matching audio stream"""
    # Select preferred maximum resolution based on video length (2160, 1440, 1080, 720, 480, 360, 240, 144)
    target_resolution_depth = 1 if 400 > video.length else 2 if 1000 > video.length else 3

    # find streams in best resolution and format
    print(video.streams)
    streams_by_mime_type = [[x for x in video.streams.filter(mime_type="video/webm", progressive=False)],
                            [x for x in video.streams.filter(mime_type="video/mp4") if x.video_codec[:3] == "avc" and x.is_progressive == False]]
    stream = None
    while not stream:
        target_resolution = resolution_levels[target_resolution_depth]
        resolution = f"{target_resolution}p"
        print(f"Searching for streams in {resolution}")
        for streams in streams_by_mime_type:
            streams = [s for s in streams if s.resolution == resolution]
            if streams:
                print("Best stream: ", streams[0])
                stream = streams[0]
                audio_mime_type = stream.mime_type.replace("video", "audio")
                video_file_extension = stream.mime_type.replace("video/", "")
                break

        target_resolution_depth += 1
    audio_stream = video.streams.filter(mime_type=audio_mime_type).order_by("bitrate").desc()[0]
    print("Audio stream: ", audio_stream)
    return stream, audio_stream, video_file_extension


class YoutubeDownloader:
    def __init__(self):
        self.target_folder_for_md = r"Main/"
        self.target_folder_for_attachments = r"Main/attachments"
        self.obsidian_template = obsidian_template
        self.output_attachments_folder = r"tmpoutput/"
        self.temp_folder = None

    def cd tm(self, video_link):
        """try downloading the video. if it doesn't finish, clean up the temp folder"""
        try:
            self._get(video_link)
        except:
            print("cleanup")
            self.clean_up_temp()

    def _get(self, video_link):
        # Initialize video information
        video = pytube.YouTube(video_link)
        print(video.title)
        channel_name = pytube.Channel(video.channel_url).channel_name
        publish_date = video.publish_date.strftime("%Y-%m-%d")
        self.target_folder_for_attachments = joinpath(r"Main/attachments", publish_date)

        # check if video was already downloaded
        if os.path.exists(joinpath(self.target_folder_for_md, f'🎞 {string_to_filename(f"{video.title} ({channel_name})")} (YouTube).md')):
            print("video already downloaded, skipping")
            return

        video_stream, audio_stream, video_file_extension = select_streams(video)

        # Initialize folders
        self.temp_folder = joinpath(".cache", video.video_id)
        self.temp_folder_audio = self.temp_folder + "/audio/"

        os.makedirs(self.temp_folder, exist_ok=True)
        os.makedirs(self.temp_folder_audio, exist_ok=True)
        os.makedirs(self.target_folder_for_attachments, exist_ok=True)

        # Determine filenames and -paths
        filenames = {}
        filenames["base"] = string_to_filename(f"{publish_date} {video.title} ({video.video_id})")
        filenames["base truncated"] = string_to_filename(f"{publish_date} {video.title[:50]} ({video.video_id})")

        filenames["video file"] = f'{filenames["base"]}.{video_file_extension}'
        filenames["thumbnail"] = filenames["base"] + ".jpg"
        filenames["captions vtt"] = filenames["base"] + ".vtt"
        filenames["captions md"] = filenames["base"] + " - Transcript.md"
        filenames["comments md"] = string_to_filename(video.video_id) + " - Comments.md"  # speculative

        filepath = {}
        filepath["captions vtt"] = joinpath(self.temp_folder, filenames["captions vtt"])
        filepath["captions md"] = joinpath(self.output_attachments_folder, filenames["captions md"])
        filepath["video file"] = joinpath(self.output_attachments_folder, filenames["video file"])
        filepath["thumbnail"] = joinpath(self.output_attachments_folder, filenames["thumbnail"])
        filepath["main md"] = joinpath(self.target_folder_for_md, f'🎞 {filenames["base"]} (YouTube).md')

        # Download transcripts

        captions = download_transcript(video.video_id, filepath["captions md"], "obsidian", return_raw=True)
        captions_success = download_transcript(video.video_id, filepath["captions vtt"], "webvtt")

        # Download streams and generate output video with ffmpeg
        print("downloading streams")
        if captions_success:
            caption_track = ffmpeg.input(filepath["captions vtt"])
            print(caption_track)
        saved_video = ffmpeg.input(video_stream.download(output_path=self.temp_folder))
        saved_audio = ffmpeg.input(audio_stream.download(output_path=self.temp_folder_audio))
        if video_file_extension == "webm":
            if captions_success:
                out = ffmpeg.output(saved_video, saved_audio, caption_track, filepath["video file"], vcodec='copy',
                                    acodec='copy').run()
            else:
                out = ffmpeg.output(saved_video, saved_audio, filepath["video file"], vcodec='copy',
                                    acodec='copy').run()
        else:
            out = ffmpeg.output(saved_video, saved_audio, filepath["video file"], vcodec='copy', acodec='copy').run()
        print(out)

        # Download thumbnail
        print("downloading thumbnail")
        with open(filepath["thumbnail"], "wb+") as file:
            try:
                file.write(requests.get(video.thumbnail_url).content)
            except Exception as e:
                print("Error downloading thumbnail", e)

        # Fill out template
        template = obsidian_template
        for x in [["%title", video.title], ["%channel_id", video.channel_id], ["%youtube_link", video.watch_url], ["%description", video.description.replace("~~", "--")], ["%view_count", str(video.views)],
                  ["%downloaded_date", datetime2.now().strftime("%Y-%m-%d")], ["%video_file", filenames["video file"]], ["%thumbnail", filenames["thumbnail"]], ["%transcript", captions], ["%comments", filenames["comments md"]]]:
            template = template.replace(x[0], str(x[1]))

        # Write filled out template to md file
        if os.path.isfile(filepath["main md"]):
            print("Zieldatei existiert bereits, abgebrochen")
        else:
            with open(filepath["main md"], "w+", encoding="utf-8") as file:
                file.write(template)

        # Move files from 'output' folder to attachments folder
        for f in ["thumbnail", "video file"]:
            target_path = joinpath(self.target_folder_for_attachments, filenames[f])
            if os.path.isfile(target_path):
                print(target_path, "existiert bereits, wird nicht überschrieben.")
                continue
            shutil.move(filepath[f], target_path)
        self.clean_up_temp()

    def clean_up_temp(self):
        """Delete all temporary files and cache files"""
        for file in os.listdir(self.output_attachments_folder):
            os.remove(joinpath(self.output_attachments_folder, file))
        if self.temp_folder:
            shutil.rmtree(self.temp_folder)


y = YoutubeDownloader()
y.get(url)
