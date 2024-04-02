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
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
from moviepy.audio.io.AudioFileClip import AudioFileClip
import csv
import random
import warnings

from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx, AudioFileClip
import csv

def synchronize_video_with_music(video_path, audio_path, output_path, video_timestamps_file, music_timestamps_file, desired_video_length, effect_options, filter_option, shake_percentage=10):
    """Synchronize video with music based on given timestamps."""
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Load video timestamps
    with open(video_timestamps_file, 'r') as f:
        video_timestamps = [tuple(map(float, line.strip().split(','))) for line in f if line.strip()]

    # Load music timestamps
    with open(music_timestamps_file, 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # Skip header row
        music_timestamps = [tuple(map(float, row)) for row in csv_reader]

    # Ensure equal number of video and music timestamps
    min_len = min(len(video_timestamps), len(music_timestamps))
    video_timestamps = video_timestamps[:min_len]
    music_timestamps = music_timestamps[:min_len]

    clips = []
    total_duration = 0  # Total duration of video clips
    remaining_duration = desired_video_length  # Remaining duration to fulfill

    for i, ((start_video, end_video), (start_music, end_music)) in enumerate(zip(video_timestamps, music_timestamps)):
        # Calculate duration of video and music segments
        video_duration = end_video - start_video
        music_duration = end_music - start_music
        
        # Check for zero duration
        if video_duration == 0 or music_duration == 0:
            continue
        
        # Adjust video playback speed to fit music segment duration
        speed_factor = video_duration / music_duration
        
        # Check for zero factor
        if speed_factor == 0:
            continue

        clip = video.subclip(start_video, end_video).fx(vfx.speedx, speed_factor)


        # Determine which filters to add based on selected options
        if filter_option == "1":
            clip = add_enhanced_filter(clip)
        if filter_option == "2":
            clip = Add_sigma_filter(clip)
        if filter_option == "2":
            clip = add_sunrise_filter(clip)
        if filter_option == "4":
            clip = add_vhs_filter(clip)


        # Determine which effects to add based on selected options
        if is_effect_selected(6, effect_options):
            clip = add_zoom_effect(clip)
        if is_effect_selected(4, effect_options):
            clip = increase_brightness(clip)
        if is_effect_selected(5, effect_options):
            clip = Add_speed_effect(clip)

        # Add camera shake effect to clip if within the specified percentage
        if is_effect_selected(2, effect_options) and random.randint(1, 100) <= shake_percentage:
            clip = concatenate_videoclips([add_camera_shake_to_clip(clip)])

        # Add chromatic aberration effect to clip with a 30% chance
        if is_effect_selected(3, effect_options) and random.randint(1, 100) <= 30:
            clip = add_chromatic_aberration(clip)

        # Add Blink effect to clip with a 5% chance
        if is_effect_selected(1, effect_options) and random.randint(1, 100) <= 5:
            clip = add_blinking_effect(clip)

        # Calculate clip duration based on remaining duration
        clip_duration = min(clip.duration, remaining_duration)
        clip = clip.subclip(0, clip_duration)

        # Adjust remaining duration
        remaining_duration -= clip_duration

        clips.append(clip)
        total_duration += clip.duration  # Update total duration

        if remaining_duration <= 0:
            break

    # Concatenate clips and set audio
    final_clip = concatenate_videoclips(clips).set_audio(audio)

    # Set the final clip's duration to the desired video length
    final_clip = final_clip.set_duration(desired_video_length)

    # Write the resulting video with adjusted duration
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=video.fps, preset='ultrafast')


def is_effect_selected(effect_number, selected_options):
    return str(effect_number) in selected_options.split(',')
