import random

def select_random_sequential_timestamps(video_duration, beat_times, song_duration):
    """Select unique timestamps based on beat intervals."""
    selected_timestamps = []
    
    try:
        # Calculate the minimum gap between consecutive timestamps
        min_gap = song_duration / (len(beat_times) * 1.0)  # Adjust 0.5 to change density of timestamps
        
        for beat_time in beat_times:
            # Calculate the start time based on the beat time
            start_time = max(0, beat_time - min_gap / 2)
            
            # Calculate the end time ensuring it doesn't exceed video duration
            end_time = min(start_time + min_gap, video_duration)
            
            # Append the selected timestamp
            selected_timestamps.append((start_time, end_time))
            
            # Reduce the remaining song duration
            song_duration -= end_time - start_time
    
        # Group timestamps
        grouped_timestamps = []
        for i in range(0, len(selected_timestamps), 4):
            grouped_timestamps.append(selected_timestamps[i:i+4])
        
        # Shuffle the groups
        random.shuffle(grouped_timestamps)
        
        # Append shuffled groups to selected_timestamps
        appended_timestamps = []
        for group in grouped_timestamps:
            for timestamp in group:
                appended_timestamps.append(timestamp)
        
        return appended_timestamps

    finally:
        print("Done Making time stamps for video")