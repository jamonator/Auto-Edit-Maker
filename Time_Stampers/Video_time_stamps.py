import random
import bisect


def select_unique_timestamps(video_duration, beat_times, quota):
    """Select unique timestamps based on beat intervals."""
    selected_timestamps = set()
    total_duration = 0
    
    try:
        while len(selected_timestamps) < quota and total_duration < video_duration:
            # Select a random timestamp
            start_time = random.choice(beat_times)
            
            # Calculate the end time based on the segment duration
            segment_duration = random.uniform(0.1, 1.0)  # Adjust the range as needed
            end_time = start_time + segment_duration
            
            # Check if the end time is within the video duration
            if end_time <= video_duration:
                selected_timestamps.add((start_time, end_time))
                total_duration += segment_duration
    finally:
        return sorted(selected_timestamps)
