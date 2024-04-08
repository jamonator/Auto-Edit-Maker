def select_sequential_timestamps(video_duration, beat_times, song_duration):
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
    
    finally:
        return selected_timestamps