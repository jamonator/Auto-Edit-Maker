from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.audio.io.AudioFileClip import AudioFileClip
import os
import random
import librosa
import numpy as np
import datetime
import csv
import librosa
import numpy as np
import datetime
import os
import csv
from moviepy.editor import VideoFileClip, vfx
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




def Make_music_time_stamps(input):
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

    # Find peaks
    onset_env = librosa.onset.onset_strength(y=y, sr=sr,
                                            hop_length=512,
                                            aggregate=np.median)
    peaks = librosa.util.peak_pick(onset_env, pre_max=20, post_max=20, pre_avg=200, post_avg=200, delta=5, wait=10)  # Adjust parameters for less sensitivity

    # Print number of timestamps detected
    num_timestamps = len(peaks)
    print("Number of timestamps detected:", num_timestamps)

    # Create output directory if it doesn't exist
    output_dir = 'Util\data\Music_time_stamps'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write peak times to CSV file
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        prev_peak_time = 0
        for peak_idx, peak_time in enumerate(librosa.frames_to_time(peaks, sr=sr)):
            start_time = prev_peak_time
            end_time = peak_time
            writer.writerow([start_time, end_time])
            prev_peak_time = peak_time

    # Complete message
    print("Peak times output to {}. \n Process complete.".format(csv_file))


def get_random_timestamp(video_duration):
    """Generate a random timestamp within the video duration."""
    start_second = random.uniform(0, video_duration - 1)  # Select a random start second
    end_second = min(start_second + 1, video_duration)  # Ensure the end second is within video duration
    return start_second, end_second

def select_unique_timestamps(video_path, quota):
    """Select unique random 1-second timestamps until the quota is filled."""
    video = VideoFileClip(video_path)
    video_duration = video.duration
    selected_timestamps = set()

    try:
        while len(selected_timestamps) < quota:
            start_second, end_second = get_random_timestamp(video_duration)
            selected_timestamps.add((start_second, end_second))
    finally:
        video.close()

    return sorted(selected_timestamps)

def synchronize_video_with_music(video_path, audio_path, output_path, video_timestamps_file, music_timestamps_file, shake_percentage=10):
    """Synchronize video with music based on given timestamps."""
    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)
    
    # Load video timestamps
    with open(video_timestamps_file, 'r') as f:
        video_timestamps = [tuple(map(float, line.strip().split(','))) for line in f if line.strip()]
    
    # Load music timestamps, skipping the header row
    with open(music_timestamps_file, 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # Skip header row
        music_timestamps = [float(row[0]) for row in csv_reader]
    
    # Ensure equal number of video and music timestamps
    min_len = min(len(video_timestamps), len(music_timestamps))
    video_timestamps = video_timestamps[:min_len]
    music_timestamps = music_timestamps[:min_len]
    
    # Shuffle the list of video timestamps
    random.shuffle(video_timestamps)
    
    clips = []
    for i, ((start_video, end_video), start_music) in enumerate(zip(video_timestamps, music_timestamps)):
        # Calculate duration of video and music segments
        video_duration = end_video - start_video
        music_duration = start_music - (music_timestamps[i - 1] if i > 0 else 0)  # Duration between music timestamps
        
        # Adjust video playback speed to fit music segment duration
        speed_factor = video_duration / music_duration
        clip = video.subclip(start_video, end_video).fx(vfx.speedx, speed_factor)
        clip = clip.set_start(start_music)
        
        # Add camera shake effect to clip if within the specified percentage
        if random.randint(1, 100) <= shake_percentage:
            clip = concatenate_videoclips(add_camera_shake_to_clip(clip))
        
        clips.append(clip)
    
    final_clip = concatenate_videoclips(clips)
    final_clip = final_clip.set_audio(audio)
    final_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

# Example usage:
video_path = "Assembly\Download\downloaded_video.mp4"
audio_path = "Util\Music\For_my_Pros.mp3"
video_timestamps_file = "Util\data\Video_time_stamps\Time_stamps.csv"
music_timestamps_file = "Util\data\Music_time_stamps\For_my_Pros.csv"
output_path = "video_with_music.mp4"

# Generate and select unique video timestamps
quota = 70
video_timestamps = select_unique_timestamps(video_path, quota)

# Write selected video timestamps to a file
with open(video_timestamps_file, 'w') as f:
    writer = csv.writer(f)
    writer.writerows(video_timestamps)

# Generate music timestamps
Make_music_time_stamps(audio_path)

# Synchronize video with music and add camera shake to 10% of clips
synchronize_video_with_music(video_path, audio_path, output_path, video_timestamps_file, music_timestamps_file, shake_percentage=10)
