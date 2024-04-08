from Util.scripts.console import *
from pytube import YouTube
import os

def Download(link, output_folder):
    print_step("Download YouTube video ▶️")
    print_start("Starting downloader")
    
    # Exracting video link
    print_substep("Extracting video link")
    youtubeObject = YouTube(link)
    print_substep("Getting highest resolution")
    youtubeObject = youtubeObject.streams.get_highest_resolution()
    
    # Downloading video
    print_start("Downloading video")
    try:
        # Set the output path to the specified folder with the desired filename
        output_path = os.path.join(output_folder, "downloaded_video.mp4")
        youtubeObject.download(output_folder, filename="downloaded_video.mp4")
    except Exception as e:
        print(f"An error has occurred: {e}")
    print_finished("Download completed")
