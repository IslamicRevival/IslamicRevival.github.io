from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import Formatter, WebVTTFormatter
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

from math import floor


class Obsidian30SecondSnippetsFormatter(Formatter):
    """Will format a transcript as a markdown file with headers for every 30 seconds block of text"""

    def format_transcript(self, transcript, **kwargs):
        """Format a single transcript"""
        blocks = []

        for sentence in transcript:
            # combine the sentences into 30 seconds blocks
            current_minute = floor(sentence["start"] / 30) + 1
            if current_minute > len(blocks):
                blocks.append("")
            blocks[-1] += " " + sentence["text"]

        blocks = [text.strip() for text in blocks]

        _return = ""
        for count, text in enumerate(blocks):
            # create header showing time position in format HH:MM:SS
            hours, total_seconds = divmod(count * 30, 3600)
            mins, sec = divmod(total_seconds, 60)
            header = f"# {str(hours).zfill(2)}:{str(mins).zfill(2)}:{str(sec).zfill(2)}"

            _return += f"{header}\n\n{text}\n\n"
        return _return

    def format_transcripts(self, transcripts, **kwargs):
        """Format several transcripts. Required to have this method"""
        return '\n\n\n'.join([self.format_transcript(transcript, **kwargs) for transcript in transcripts])


obsidian_formatter = Obsidian30SecondSnippetsFormatter()
webvtt_formatter = WebVTTFormatter()


def download_transcript(video_id: str, filename: str, format: str, return_raw=False):
    """Will find the best transcript for the video (selects manually over automatically created) and format it in the specified format
    :param return_raw: whether to return the formatted transcript as text or save it to file
    Todo: specify preferred language or get several"""
    transcript = None
    try:
        transcript = YouTubeTranscriptApi.list_transcripts(video_id).find_manually_created_transcript(["en", "de"]).fetch()
        print("Found manually created transcript")
        return transcript
    except NoTranscriptFound:
        pass
    except TranscriptsDisabled:
        print("Transcripts disabled for this video")
        return

    try:
        transcript = YouTubeTranscriptApi.list_transcripts(video_id).find_generated_transcript(["en", "de"]).fetch()
        print("Found automatically generated transcript")
        return transcript
    except NoTranscriptFound:
        pass
    print("No transcripts found")

    if not transcript:
        return False

    # format the transcript
    if format == "obsidian":
        formatted = obsidian_formatter.format_transcript(transcript)
    else:
        formatted = webvtt_formatter.format_transcript(transcript)
    if return_raw:
        return formatted

    # save the transcript to file
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(formatted)
    return True
