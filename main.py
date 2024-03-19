from Util.scripts.console import *
from Util.scripts.Video_downloader import * 
from Video_Gen.Video_maker import *
from Video_Gen.Starter_clip import *
from moviepy.editor import AudioFileClip
from Util.scripts.Time_converter import parse_timestamp
import os
import random



print_step("Starting Auto Edit Maker 🎥")


# Set up file/folder paths 
print_substep("Setting File and folder paths")
download_output = "Assembly/Download"
Music_folder = "Util\Music"
output_path = "video_with_music.mp4"

# Set up quota
video_path = "Assembly/Download/downloaded_video.mp4"
video_file = VideoFileClip(video_path)
video_duration = video_file.duration

# Choose music at random
files = os.listdir(Music_folder)
random_audio_file = os.path.join(Music_folder, random.choice(files))
print_substep(f"Random audio file selected: {random_audio_file}")
# random_audio_file = "Util\Music\Chanel Cologne.mp3"
audio_file = AudioFileClip(random_audio_file)
audio_duration = audio_file.duration

# Collect and download video link
link = input("Insert video link: ")
Download(link, download_output)

# Start and end timestamps input
start_clip_option = input("Do you want to add a starter clip Y/n: ")
if start_clip_option.lower() == "y":
    start_timestamp = input("Enter start timestamp (e.g., 9:23): ")
    end_timestamp = input("Enter end timestamp (e.g., 9:30): ")
else:
    print("No starter clip will be added.")
    start_timestamp = None
    end_timestamp = None

# Set duration of final video
duration = input ("Do you want a custom video lenght Y/n: ")
if duration.lower() == "y":
    set_manual_duration = input("Enter video lenght (e.g., 0:25): ")
    desired_video_length = parse_timestamp(set_manual_duration)
    print(f"desired video length set to: {desired_video_length} seconds")
else:
    # Adjust quota based on comparison and round to nearest whole number
    if audio_duration < video_duration:
        desired_video_length = round(audio_duration)
    else:
        desired_video_length = round(video_duration)

    print(f"desired video length set to: {desired_video_length} seconds")



# Make Video 
Make_video(desired_video_length,random_audio_file)

# Starter clip
if start_clip_option.lower() == "y":
    make_starter_clip(start_timestamp, end_timestamp)

else:
    exit

# https://youtu.be/9PwmWaOYgyw
