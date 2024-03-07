from Video_Effects.Camera_shake import add_camera_shake_to_clip
from Video_Effects.VHS_filter import add_vhs_filter
from Video_Effects.Zoom_effect import add_zoom_effect
from Video_Effects.Chromatic_aberration import add_chromatic_aberration
from Video_Effects.light_effect import increase_brightness
from Video_Effects.Blink_effect import add_blinking_effect_to_clip
from moviepy.editor import VideoFileClip, concatenate_videoclips, vfx
from moviepy.audio.io.AudioFileClip import AudioFileClip
import csv
import random
import warnings

def synchronize_video_with_music(video_path, audio_path, output_path, video_timestamps_file, music_timestamps_file, shake_percentage=10):
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

        # Apply VHS filter effect
        clip = add_vhs_filter(clip)

        # Check if adding zoom effect
        if clip.duration >= 0.1:
            print("[*] Clip longer than 0.1, adding zoom")
            clip = add_zoom_effect(clip.subclip(t_start=0), target_zoom_ratio=0.2, zoom_duration_ratio=0.1)
            clip = increase_brightness(clip)

        clip = clip.set_start(start_music) 

        # Add camera shake effect to clip if within the specified percentage
        if random.randint(1, 100) <= shake_percentage:
            clip = concatenate_videoclips([add_camera_shake_to_clip(clip)])

        # Add chromatic aberration effect to clip with a 10% random chance
        if random.randint(1, 100) <= 40:
            clip = add_chromatic_aberration(clip)

        # Add Blinking effect at random
        # if random.randint(1, 100) <= 20:
        #     clip = add_blinking_effect_to_clip(clip)

            
        clips.append(clip)
        total_duration += clip.duration  # Update total duration

    # Randomize the sequence of video clips
    # random.shuffle(clips)

    final_clip = concatenate_videoclips(clips)
    final_clip = final_clip.set_audio(audio)

    # Set the final clip's duration to the total duration
    final_clip = final_clip.set_duration(total_duration)

    # Write the resulting video with adjusted duration
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # Ignore the warning related to FFMPEG_VideoReader
        final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=video.fps, preset='ultrafast')


