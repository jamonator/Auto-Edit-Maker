import bisect

def make_timestamps(video_path, quota, video_duration, beat_times):
    """Select unique timestamps based on beat intervals."""
    selected_timestamps = set()

    try:
        # Divide the video duration into segments to select beat intervals
        segment_duration = video_duration / quota

        # Track the current beat index
        current_beat_idx = 0

        for _ in range(quota):
            # Get the start and end times for the current segment
            start_segment = _ * segment_duration
            end_segment = ( _ + 3 ) * segment_duration

            # Iterate over beat intervals within the segment
            while current_beat_idx < len(beat_times) and beat_times[current_beat_idx] < end_segment:
                start_beat = beat_times[current_beat_idx]
                end_beat = min(start_beat + segment_duration, end_segment)

                # Ensure selected timestamps are within video duration
                if end_beat - start_beat <= segment_duration:
                    selected_timestamps.add((start_beat, end_beat))

                current_beat_idx += 3

    finally:
        return sorted(selected_timestamps)
