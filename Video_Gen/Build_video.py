from Util.scripts.console import *
from Video_Effects.Camera_shake import add_camera_shake_to_clip
from Video_Filters.VHS_filter import add_vhs_filter
from Video_Effects.Zoom_effect import add_zoom_effect
from Video_Effects.Glitch_effect import add_chromatic_aberration
from Video_Effects.light_effect import increase_brightness
from Video_Effects.Blink_effect import add_blinking_effect
from Video_Effects.Speed_effect import Add_speed_effect
from Video_Filters.Enhanced_filter import add_enhanced_filter
from Video_Filters.Sigma_filter import Add_sigma_filter
from Video_Filters.Sunrise_filter import add_sunrise_filter
from Time_Stampers.Music_time_stamps import make_music_time_stamps
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx, AudioFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
import csv
import random
import os
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn

def synchronize_video_with_music(video_path, audio_path, output_path, video_timestamps_file, music_timestamps_file, desired_video_length, effect_options, filter_option, shake_percentage=10):
    print_step("Building Video 🔨🎥")
    while True:
        try:

            # Load video and song
            print_substep("Loading video and song")
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)

            # Load video timestamps
            print_substep("Loading video timestamps")
            with open(video_timestamps_file, 'r') as f:
                video_timestamps = [tuple(map(float, line.strip().split(','))) for line in f if line.strip()]

            # Load music timestamps
            print_substep("Loading music timestamps")
            with open(music_timestamps_file, 'r') as f:
                csv_reader = csv.reader(f)
                next(csv_reader)  # Skip header row
                music_timestamps = [tuple(map(float, row)) for row in csv_reader]

            # Ensure equal number of video and music timestamps
            print_substep("Ensure equal number of video and music timestamps")
            min_len = min(len(video_timestamps), len(music_timestamps))
            video_timestamps = video_timestamps[:min_len]
            music_timestamps = music_timestamps[:min_len]
            clips = []
            total_duration = 0  # Total duration of video clips
            remaining_duration = desired_video_length  # Remaining duration to fulfill


            # Initialize progress bar
            progress = Progress(
                "[progress.description]{task.description}",
                BarColumn(),
                "[progress.percentage]{task.completed}/{task.total}",
                TimeRemainingColumn(),
)

            # Create video 
            with progress:
                rounded_remaining_duration = int(remaining_duration)
                task = progress.add_task("[green]Creating video...", total=rounded_remaining_duration)
                for i, ((start_video, end_video), (start_music, end_music)) in enumerate(zip(video_timestamps, music_timestamps)):
                    # Create video 
                    print_start("Starting video creation")
                    
                    # Update progress description
                    progress.description = f"Processing segment {i+1}/{len(video_timestamps)}"
                    progress.update(task, advance=1)  # Update progress

                    # Calculate duration of video and music segments
                    print_substep("Calculate duration of video and music segments")
                    video_duration = end_video - start_video
                    music_duration = end_music - start_music

                    # Check for zero duration
                    print_substep("Checking for zero duration")
                    if video_duration == 0 or music_duration == 0:
                        continue
                    
                    # Adjust video playback speed to fit music segment duration
                    print_substep("Adjusting video playback speed to fit music segment duration")
                    speed_factor = video_duration / music_duration
                    
                    # Check for zero factor
                    print_substep("Checking for zero factor")
                    if speed_factor == 0:
                        continue
                    print_substep("Creating clip")
                    clip = video.subclip(start_video, end_video).fx(vfx.speedx, speed_factor)

                    # Determine which filters to add based on selected options
                    print_start("Adding filters:")
                    if filter_option == "1":
                        clip = add_enhanced_filter(clip)
                        print_substep("Added enhanced filter")
                    if filter_option == "2":
                        clip = Add_sigma_filter(clip)
                        print_substep("Added sigma filter")
                    if filter_option == "3":
                        clip = add_sunrise_filter(clip)
                        print_substep("Added sunrise filter")
                    if filter_option == "4":
                        clip = add_vhs_filter(clip)
                        print_substep("Added VHS filter")

                    # Determine which effects to add based on selected options
                    print_start("Adding effects:")
                    if is_effect_selected(6, effect_options):
                        clip = add_zoom_effect(clip)
                        print_substep("Added zoom effect")
                    if is_effect_selected(4, effect_options):
                        clip = increase_brightness(clip)
                        print_substep("Added increased brightness effect")
                    if is_effect_selected(5, effect_options):
                        clip = Add_speed_effect(clip)
                        print_substep("Added speed effect")

                    # Add camera shake effect to clip if within the specified percentage
                    if is_effect_selected(2, effect_options) and random.randint(1, 100) <= shake_percentage:
                        clip = concatenate_videoclips([add_camera_shake_to_clip(clip)])
                        print_substep("Added camera shake effect")

                    # Add chromatic aberration effect to clip with a 30% chance
                    if is_effect_selected(3, effect_options) and random.randint(1, 100) <= 30:
                        clip = add_chromatic_aberration(clip)
                        print_substep("Added chromatic aberration effect")

                    # Add Blink effect to clip with a 5% chance
                    if is_effect_selected(1, effect_options) and random.randint(1, 100) <= 5:
                        clip = add_blinking_effect(clip)
                        print_substep("Added blinking effect")

                    # Calculate clip duration based on remaining duration
                    print_substep("Calculate clip duration based on remaining duration")
                    clip_duration = min(clip.duration, remaining_duration)
                    clip = clip.subclip(0, clip_duration)

                    # Adjust remaining duration
                    print_substep("Adjusting remaining duration")
                    remaining_duration -= clip_duration

                    # Append clip to clips list
                    print_substep("Appending clip to clips list")
                    clips.append(clip)
                    total_duration += clip.duration  # Update total duration

                    if remaining_duration <= 0:
                        print_finished("Built Video")
                        break

            print_start("Writing final video")

            # Concatenate clips and set audio
            print_substep("Concatenate clips and set audio")
            final_clip = concatenate_videoclips(clips).set_audio(audio)

            # Set the final clip's duration to the desired video length
            print_substep("Setting the final clip's duration to the desired video length")
            final_clip = final_clip.set_duration(desired_video_length)

            # Write the resulting video with adjusted duration
            print_substep("Writing the resulting video with adjusted duration")
            final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=video.fps, preset='ultrafast')

            # Break out of the loop if execution is successful
            break

        except Exception as e:
            # Check if the error message matches the specified error
            if "t_start (0.00) should be smaller than the clip's duration" in str(e):
                # Delete the timestamp file
                if os.path.exists(music_timestamps_file):
                    os.remove(music_timestamps_file)
                # Run the make_music_time_stamps function
                make_music_time_stamps(audio_path)
            else:
                # Re-raise the exception if it's not the expected error
                raise e




def is_effect_selected(effect_number, selected_options):
    return str(effect_number) in selected_options.split(',')
