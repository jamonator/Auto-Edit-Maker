from Util.scripts.console import *
from Util.scripts.Video_downloader import *
from Util.scripts.Video_time_stamper import *
from Util.scripts.Music_time_stamper import *
import os
import random


print_step("Starting Auto Edit Maker 🎥")


# Set up values and settings
duration = 30

# Set up file/folder paths 
print_substep("Setting File and folder paths")
download_output = "Assembly/Download"
Music_folder = "Util\Music"

# Collect and download video link
link = input("Insert video link: ")
Download(link, download_output)

# Make Music time stamps if not done already
files = os.listdir(Music_folder)
random_audio_file = os.path.join(Music_folder, random.choice(files))
print("Random audio file selected:", random_audio_file)
Make_music_time_stamps(random_audio_file)



# Gather random video time stamps
video_path = r"C:\Users\jamo0\Auto_Edit_Maker\Assembly\Download\Downloaded_video.mp4"  # Specify the absolute path to your video file
output_file = "Util\data\Video_time_stamps\Time_stamps.csv"
quota = 70  # Number of timestamps to generate
timestamps = select_unique_timestamps(video_path, quota)
print("Selected Timestamps:", timestamps)

save_timestamps_to_csv(timestamps, output_file)
print(f"Timestamps saved to {output_file}")