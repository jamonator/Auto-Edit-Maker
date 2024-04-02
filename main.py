    from Util.scripts.console import *
    from Util.scripts.Video_downloader import * 
    from Video_Gen.Video_maker import *
    from Video_Gen.Starter_clip import *
    from moviepy.editor import AudioFileClip
    from Util.scripts.Time_converter import parse_timestamp
    import os
    import random



    print_step("Starting Auto Edit Maker 🎥")

    ########################## Set values ##########################

    # Set up file/folder paths 
    print_substep("Setting File and folder paths")
    download_output = "Assembly/Download"
    Music_folder = "Util/Music"
    output_path = "Output.mp4"

    # Skip questions and use defaults 
    use_default_values = True    # True will skip asking / False will ask

    # Choose music at random
    files = os.listdir(Music_folder)
    random_audio_file = os.path.join(Music_folder, random.choice(files))
    print_substep(f"Random audio file selected: {random_audio_file}")
    # random_audio_file = "Util\Music\Better Days.mp3"
    audio_file = AudioFileClip(random_audio_file)
    audio_duration = audio_file.duration

    # default Options
    starter_clip_default = "n"
    start_clip_option = "n"
    set_manual_duration_default = "Y"
    duration_default = "0:50"
    time_stamp_type_default = "1"
    set_time_stamp_type = "1"
    link_or_file_default = "2"
    effect_options_default = "1,2,3,4,5,6"
    effect_options = "1,2,3,4,5,6"
    filter_option_default = "2"
    filter_option = "2"

    ########################## Skip asking ##########################

    # Skip asking and just use default values 
    if use_default_values == True:
        if link_or_file_default == "1": 
            # Collect and download video link
            link = handle_input("Insert video link: ")
            Download(link, download_output)
        
        # Set video length 
        desired_video_length = parse_timestamp(duration_default)
        print_substep(f"desired video length set to: {desired_video_length} seconds")


    ########################## ASK USER INPUT ##########################
        
    # Ask for values 
    if use_default_values == False:
        # Ask for video link or file 
        print_table(["1: Download a youtube video ", "2: Use video file"])
        link_or_file = handle_input("Do you want to download a video link or run from file (default is 1) 1/2: ", default=link_or_file_default)

        if link_or_file == "1": 
            # Collect and download video link
            link = handle_input("Insert video link: ")
            Download(link, download_output)

        if link_or_file == "2":
            # Give user instructions
            handle_input("Please drag and drop a file into the Assembly/Download folder then press enter:")

        # Start and end timestamps input
        start_clip_option = handle_input("Do you want to add a starter clip (Default is no) Y/n: ", default=starter_clip_default)
        if start_clip_option.lower() == "y":
            start_timestamp = handle_input("Enter start timestamp (e.g., 9:23): ")
            end_timestamp = handle_input("Enter end timestamp (e.g., 9:30): ")
        else:
            print("No starter clip will be added.")
            start_timestamp = None
            end_timestamp = None

        # Set duration of final video
        duration = handle_input ("Do you want a custom video lenght (Default is yes) Y/n: ", default=set_manual_duration_default)
        if duration.lower() == "y":
            set_manual_duration = handle_input("Enter video lenght (Default is 0:50): ", default=duration_default)
            desired_video_length = parse_timestamp(set_manual_duration)
            print(f"desired video length set to: {desired_video_length} seconds")
        else:
            # Set up quota
            video_path = next((os.path.join("Assembly/Download", file) for file in os.listdir("Assembly/Download") if file.endswith((".mp4", ".avi", ".mov"))), None)
            video_file = VideoFileClip(video_path)
            video_duration = video_file.duration

            # Adjust quota based on comparison and round to nearest whole number
            if audio_duration < video_duration:
                desired_video_length = round(audio_duration)
            else:
                desired_video_length = round(video_duration)

            print(f"desired video length set to: {desired_video_length} seconds")

        # Set Time stamper random or squential
        print_table(["Type 1: Random clip selection ", "Type 2: Sequential clip selection"])
        set_time_stamp_type = handle_input ("Do you want type 1 or type 2 (Default is 1): ", default=time_stamp_type_default)

        # Pick effects
        print_table(["1. Blink effect", "2. Camera shake", "3. Glitch effect", "4. Light effect", "5. Speed effect", "6. Zoom effect"])
        effect_options = handle_input("Pick effects (eg. 1,3,5) (Default is all): ", default=effect_options_default)

        # Pick filter
        print_table(["1. Enhanced filter", "2. Sigma filter", "3. Sunrise filter", "4. VHS filter"])
        filter_option = handle_input("Pick video filter (Default is 2): ", default=filter_option_default)

    ########################## Start video creation ##########################
        
    # Make Video 
    Make_video(desired_video_length,random_audio_file, set_time_stamp_type, output_path, effect_options, filter_option)

    # Starter clip
    if start_clip_option.lower() == "y":
        make_starter_clip(start_timestamp, end_timestamp)

    else:
        exit

    # https://youtu.be/4Nm9hlac4js
