! pip install pytube
! pip install unidecode

import re
import os
from pytube import YouTube
from pytube.exceptions import RegexMatchError, VideoUnavailable, PytubeError
from unidecode import unidecode

# This function is used to check if the given YouTube URL is valid.
def is_valid_youtube_url(url):
    # Regular expression to match YouTube URLs with or without "si" query parameter
    regex = r'^https?://(www\.)?youtu\.?be(\.com)?/[\w-]+(\?si=[\w-]+)?$'
    return re.match(regex, url) is not None

# This function is used to download audio from a YouTube video.
def download_song(url):
    if not is_valid_youtube_url(url):
        print("Invalid YouTube URL.")
        return

    try:
        video = YouTube(url)  # Initialize a YouTube object with the given URL.
        streams = video.streams.filter(only_audio=True).order_by('abr').desc()

        if not streams:
            print("No suitable audio streams found.")
            return
    except (RegexMatchError, VideoUnavailable, PytubeError) as e:
        print(f"Error while fetching video: {str(e)}")
        return

    stream = streams.first()  # Select the audio stream with the highest quality.
    video_title = unidecode(video.title)  # Convert the video title to ASCII to avoid character issues.
    audio_filename = f"{video_title}.mp3"  # Create an audio file name with the video title.

    try:
        stream.download(output_path=".", filename=audio_filename)  # Download the audio to the current directory with the appropriate name.
        print(f"Highest quality audio ({audio_filename}) successfully downloaded.")
    except Exception as e:
        print(f"Error while downloading audio: {str(e)}")

if __name__ == "__main__":
    url = input("Enter the YouTube video URL: ")
    download_song(url)  # Call the download_song function to download audio from the provided URL.
