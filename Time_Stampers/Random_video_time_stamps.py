import random

def select_random_timestamps(video_duration, beat_times, song_duration):
    """Select unique timestamps based on beat intervals."""
    selected_timestamps = []
    
    try:
        # Calculate the minimum gap between consecutive timestamps
        min_gap = song_duration / (len(beat_times) * 1.0)  # Adjust 0.5 to change density of timestamps
        
        while song_duration > 0:
            # Select a random start time within the range of video duration minus the minimum gap
            start_time = random.uniform(0, video_duration - min_gap)
            
            # Calculate the end time ensuring it doesn't exceed video duration
            end_time = min(start_time + min_gap, video_duration)
            
            # Check if the time gap between selected and existing timestamps is greater than the minimum gap
            if not any(abs(start_time - t[1]) < min_gap for t in selected_timestamps):
                # Append the selected timestamp
                selected_timestamps.append((start_time, end_time))
                song_duration -= end_time - start_time
    
    finally:
        return selected_timestamps