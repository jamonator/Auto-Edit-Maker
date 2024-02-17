from Util.scripts.console import *
from Util.scripts.Video_downloader import *
from Util.scripts.Video_time_stamper import *
from Util.scripts.Music_time_stamper import *
from Video_Gen.Video_maker import *
from Video_Gen.Add_VHS import *
import os
import random



print_step("Starting Auto Edit Maker 🎥")


# Set up values and settings
quota = 120

# Set up file/folder paths 
print_substep("Setting File and folder paths")
download_output = "Assembly/Download"
Music_folder = "Util\Music"
output_path = "video_with_music.mp4"

# Collect and download video link
link = input("Insert video link: ")
Download(link, download_output)

# Choose music at random
files = os.listdir(Music_folder)
random_audio_file = os.path.join(Music_folder, random.choice(files))
print_substep(f"Random audio file selected: {random_audio_file}")

# Make Video 
Make_video(quota, random_audio_file)
