import os
import random
import datetime
import csv
import librosa
import numpy as np
from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.editor import vfx
import cv2


def add_camera_shake_to_clip(clip, shake_intensity=10):
    """Apply camera shake effect to a video clip."""
    frame_width, frame_height = clip.size
    frame_count = int(clip.duration * clip.fps)

    shake_intensity = max(1, min(shake_intensity, 20))  # Limit shake intensity between 1 and 20

    frames_with_shake = []
    for _ in range(frame_count):
        frame = clip.get_frame(_ / clip.fps)

        # Randomly shift the frame
        dx = random.randint(-shake_intensity, shake_intensity)
        dy = random.randint(-shake_intensity, shake_intensity)
        translation_matrix = np.float32([[1, 0, dx], [0, 1, dy]])
        shifted_frame = cv2.warpAffine(frame, translation_matrix, (frame_width, frame_height))

        frames_with_shake.append(shifted_frame)

    return [clip.set_audio(None).set_make_frame(lambda t: frames_with_shake[min(int(t * clip.fps), len(frames_with_shake) - 1)])]


def make_music_time_stamps(input):
    # Load local audio file
    input_audio_file = input
    y, sr = librosa.load(input_audio_file)

    # Generate CSV file path based on input audio file name
    input_file_name = os.path.splitext(os.path.basename(input_audio_file))[0]
    csv_file = os.path.join('Util\data\Music_time_stamps', '{}.csv'.format(input_file_name))

    # Check if CSV file already exists
    if os.path.exists(csv_file):
        print("Already made:", csv_file)
        return

    # Get file duration in seconds
    duration = librosa.get_duration(y=y, sr=sr)

    # Print duration to console
    print("File duration(s): ", str(datetime.timedelta(seconds=duration)))

    # Find beats
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    # Convert beat frames to time
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # Write beat times to CSV file
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Start Time', 'End Time'])
        for start_time, end_time in zip(beat_times[:-1], beat_times[1:]):
            writer.writerow([start_time, end_time])

    # Complete message
    print("Beat times output to {}. \n Process complete.".format(csv_file))


def select_unique_timestamps(video_path, quota, video_duration):
    """Select unique timestamps based on beat intervals."""
    selected_timestamps = set()

    try:
        while len(selected_timestamps) < quota:
            # Randomly select a beat interval
            start_beat_idx = random.randint(0, len(beat_times) - 2)
            end_beat_idx = random.randint(start_beat_idx + 1, min(start_beat_idx + 10, len(beat_times) - 1))
            start_time = beat_times[start_beat_idx]
            end_time = beat_times[end_beat_idx]
            selected_timestamps.add((start_time, end_time))
    finally:
        return sorted(selected_timestamps)


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
    for i, ((start_video, end_video), (start_music, end_music)) in enumerate(zip(video_timestamps, music_timestamps)):
        # Calculate duration of video and music segments
        video_duration = end_video - start_video

        # Adjust video playback speed to fit music segment duration
        music_duration = end_music - start_music
        speed_factor = video_duration / music_duration

        clip = video.subclip(start_video, end_video).fx(vfx.speedx, speed_factor)
        clip = clip.set_start(start_music)

        # Add camera shake effect to clip if within the specified percentage
        if random.randint(1, 100) <= shake_percentage:
            clip = concatenate_videoclips(add_camera_shake_to_clip(clip))

        clips.append(clip)

    # Randomize the sequence of video clips
    random.shuffle(clips)

    final_clip = concatenate_videoclips(clips)
    final_clip = final_clip.set_audio(audio)
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')


# Example usage:
video_path = "Assembly\Download\downloaded_video.mp4"
audio_path = "Util\Music\Frizk - ALL MY FELLAS (Lyrics).mp3"
video_timestamps_file = "Util\data\Video_time_stamps\Time_stamps.csv"
music_timestamps_file = "Util\data\Music_time_stamps\Frizk - ALL MY FELLAS (Lyrics).csv"
output_path = "video_with_music.mp4"

# Generate music timestamps
make_music_time_stamps(audio_path)

# Load beat times from CSV file
beat_times = []
with open(music_timestamps_file, 'r') as f:
    csv_reader = csv.reader(f)
    next(csv_reader)  # Skip header row
    for row in csv_reader:
        beat_times.append(float(row[0]))

# Generate and select unique video timestamps based on beat intervals
quota = 120
video = VideoFileClip(video_path)
video_duration = video.duration
video_timestamps = select_unique_timestamps(video_path, quota, video_duration)

# Write selected video timestamps to a file
with open(video_timestamps_file, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(video_timestamps)

# Synchronize video with music and add camera shake to 10% of clips
synchronize_video_with_music(video_path, audio_path, output_path, video_timestamps_file, music_timestamps_file, shake_percentage=10)
