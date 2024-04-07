from Util.scripts.console import *
from Util.scripts.Video_downloader import * 
from Video_Gen.Video_maker import *
from Video_Gen.Starter_clip import *
from Video_Gen.Remove_time_stamp import *
from moviepy.editor import AudioFileClip
from Util.scripts.Time_converter import parse_timestamp
import os
import random

# Start timing
start_time = time.time()

print_step("Starting Auto Edit Maker 🎥")


########################## Set values ##########################

# Set up file/folder paths 
print_substep("Setting File and folder paths")
download_output = "Assembly/Download"
Music_folder = "Util/Music"
output_path = "Output.mp4"
video_path = next((os.path.join("Assembly/Download", file) for file in os.listdir("Assembly/Download") if file.endswith((".mp4", ".avi", ".mov", ".MP4", ".MOV"))), None)

# Skip questions and use defaults 
use_default_values = True    # True will skip asking / False will ask

# Choose if the script runs using the file curently in Assembly/Download or downloads a video from a link
link_or_file_default = "2"   # 1 is run from file / 2 is download video

# Choose wether you want to add a starter clip or not
starter_clip_default = "n"   # Yes or no

# Choose whether or not you want to cut parts from the input video 
cut_from_video_default = "n"

# Choose wether you want to set a default duration or not 
set_manual_duration_default = "Y"   # Yes or no 
duration_default = "0:50"   # The duration that will be used if Y is selected the format 0:00 

# Select what song selection type you want
song_choice_default = "2"   # 1 is select a song youself / 2 is randomly decide 
song_file_default = "Bando.mp3" # The song that will be used if 1 is selected 

# Choose wether the time stamps  are selected randomly or  Seqentialy
time_stamp_type_default = "3"   # 1 is random / 2 is sequential / 3 is random sequential time stamps

# Select effect options go look at Video_Gen\Synchronize.py to see the differnt options
effect_options_default = "1,2,3,4,5,6"   # List what effects you want

# Select a filter to add to the video go look at Video_Gen\Synchronize.py to see the differnt options
filter_option_default = "2" # enter what option number you want


########################## Skip asking ##########################

# Skip asking and just use default values 
if use_default_values == True:
    # Set values 
    set_time_stamp_type = time_stamp_type_default
    effect_options = effect_options_default
    filter_option = filter_option_default
    song_choice  = song_choice_default
    song_file = song_file_default
    start_clip_option = starter_clip_default

    # Collect and download video link
    if link_or_file_default == "1": 
        link = handle_input("Insert video link: ")
        Download(link, download_output)
    
    # Set video length 
    desired_video_length = parse_timestamp(duration_default)
    print_substep(f"desired video length set to: {desired_video_length} seconds")
    
    # Set the song to the default option
    if song_choice == "1":
        files = os.listdir(Music_folder)
        print_table(files)
        audio_file_choice = song_file
        random_audio_file = os.path.join(Music_folder, audio_file_choice)
        audio_file = AudioFileClip(random_audio_file)
        audio_duration = audio_file.duration

    # Set song to a random song
    if song_choice == "2":
        files = os.listdir(Music_folder)
        random_audio_file = os.path.join(Music_folder, random.choice(files))
        print_substep(f"Random audio file selected: {random_audio_file}")
        audio_file = AudioFileClip(random_audio_file)
        audio_duration = audio_file.duration

    if start_clip_option.lower() == "y":
        start_timestamp = handle_input("Enter start timestamp (e.g., 9:23): ")
        end_timestamp = handle_input("Enter end timestamp (e.g., 9:30): ")


########################## ASK USER INPUT ##########################
    
# Ask for values 
if use_default_values == False:
    # Ask for video link or file 
    print_table(["1: Download a youtube video ", "2: Use video file"])
    link_or_file = handle_input(f"Do you want to download a video link or run from file (default is {link_or_file_default}) 1/2: ", default=link_or_file_default)

    if link_or_file == "1": 
        # Collect and download video link
        link = handle_input("Insert video link: ")
        Download(link, download_output)

    if link_or_file == "2":
        # Give user instructions
        handle_input("Please drag and drop a file into the Assembly/Download folder then press enter:")

    # Continue with the rest of the code
    cut_from_video = handle_input(f"Do you want to cut parts of the raw input video out? (Default is {cut_from_video_default}) Y/n: ")
    if cut_from_video_default.lower() == "y":
        time_stamps_to_remove = handle_input("Enter the time stamps to remove (e.g 0:00-0:10, 2:50-3:00): ")
        timestamp_list = [parse_timestamp_range(timestamp) for timestamp in parse_timestamps(time_stamps_to_remove)]
        print(timestamp_list)
        remove_timestamps(video_path, timestamp_list)
  
    # Choose song for video
    print_table(["1: Select a song ", "2: Use random song"])
    song_choice = handle_input(f"Do you want to select a song or make it random (default is {song_choice_default}) 1/2: ", default=song_choice_default)

    if song_choice == "1":
        files = os.listdir(Music_folder)
        print_table(files)
        audio_file_choice = handle_input("Enter the file name (e.g Better Days.mp3): ")
        random_audio_file = os.path.join(Music_folder, audio_file_choice)
        audio_file = AudioFileClip(random_audio_file)
        audio_duration = audio_file.duration

    if song_choice == "2":
        files = os.listdir(Music_folder)
        random_audio_file = os.path.join(Music_folder, random.choice(files))
        print_substep(f"Random audio file selected: {random_audio_file}")
        audio_file = AudioFileClip(random_audio_file)
        audio_duration = audio_file.duration


    # Start and end timestamps input
    start_clip_option = handle_input(f"Do you want to add a starter clip (Default is {starter_clip_default}) Y/n: ", default=starter_clip_default)
    if start_clip_option.lower() == "y":
        start_timestamp = handle_input("Enter start timestamp (e.g., 9:23): ")
        end_timestamp = handle_input("Enter end timestamp (e.g., 9:30): ")
    else:
        print("No starter clip will be added.")
        start_timestamp = None
        end_timestamp = None

    # Set duration of final video
    duration = handle_input (f"Do you want a custom video lenght (Default is {set_manual_duration_default}) Y/n: ", default=set_manual_duration_default)
    if duration.lower() == "y":
        set_manual_duration = handle_input(f"Enter video lenght (Default is {duration_default}): ", default=duration_default)
        desired_video_length = parse_timestamp(set_manual_duration)
        print(f"desired video length set to: {desired_video_length} seconds")
    else:
        # Set up quota
        video_file = VideoFileClip(video_path)
        video_duration = video_file.duration

        # Adjust quota based on comparison and round to nearest whole number
        if audio_duration < video_duration:
            desired_video_length = round(audio_duration)
        else:
            desired_video_length = round(video_duration)

        print(f"desired video length set to: {desired_video_length} seconds")

    # Set Time stamper random or squential
    print_table(["Type 1: Random clip selection ", "Type 2: Sequential clip selection", "Type 3 Random sequental clip selection"])
    set_time_stamp_type = handle_input (f"Pick a clip selection type (Default is {time_stamp_type_default}): ", default=time_stamp_type_default)

    # Pick effects
    print_table(["1. Blink effect", "2. Camera shake", "3. Glitch effect", "4. Light effect", "5. Speed effect", "6. Zoom effect"])
    effect_options = handle_input(f"Pick effects (eg. 1,3,5) (Default is {effect_options_default}): ", default=effect_options_default)

    # Pick filter
    print_table(["1. Enhanced filter", "2. Sigma filter", "3. Sunrise filter", "4. VHS filter"])
    filter_option = handle_input(f"Pick video filter (Default is {filter_option_default}): ", default=filter_option_default)


########################## Start video creation ##########################
    

# Make Video 
Make_video(desired_video_length, random_audio_file, set_time_stamp_type, output_path, effect_options, filter_option)

# Starter clip
if start_clip_option.lower() == "y":
    make_starter_clip(video_path, output_path, start_timestamp, end_timestamp)

# End timing
end_time = time.time()
execution_time = end_time - start_time

# Convert execution time to a readable format if it exceeds 60 seconds
if execution_time > 60:
    minutes = int(execution_time // 60)
    seconds = int(execution_time % 60)
    print(f"Script executed in {minutes} minutes and {seconds} seconds.")
else:
    print(f"Script executed in {execution_time} seconds.")



# https://youtu.be/4Nm9hlac4js
