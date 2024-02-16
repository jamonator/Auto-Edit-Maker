import csv
from moviepy.editor import VideoFileClip
import random
import os

def get_random_timestamp(video_duration):
    """Generate a random timestamp within the video duration."""
    start_second = random.randint(0, int(video_duration) - 1)  # Select a random start second
    end_second = min(start_second + 1, int(video_duration))  # Ensure the end second is within video duration
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

def save_timestamps_to_csv(timestamps, output_file):
    """Save the selected timestamps to a CSV file."""
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(timestamps)

# Gather random video time stamps
video_path = r"C:\Users\jamo0\Auto_Edit_Maker\Assembly\Download\Downloaded_video.mp4"  # Specify the absolute path to your video file
output_file = r"C:\Users\jamo0\Auto_Edit_Maker\Util\data\Video_time_stamps\Time_stamps.csv"
quota = 10  # Number of timestamps to generate
timestamps = select_unique_timestamps(video_path, quota)
print("Selected Timestamps:", timestamps)

# Save timestamps to CSV
save_timestamps_to_csv(timestamps, output_file)
print(f"Timestamps saved to {output_file}")

