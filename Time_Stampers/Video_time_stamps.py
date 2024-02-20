import random
import bisect


def select_unique_timestamps(video_path, quota, video_duration, beat_times):
    """Select unique timestamps based on beat intervals."""
    selected_timestamps = set()

    try:
        # Divide the video duration into segments to select beat intervals
        segment_duration = video_duration / quota

        for _ in range(quota):
            # Select a random segment within the video duration
            start_segment = random.uniform(0, video_duration - segment_duration)
            end_segment = start_segment + segment_duration

            # Select a beat interval within the segment
            start_beat_idx = bisect.bisect_left(beat_times, start_segment)
            end_beat_idx = bisect.bisect_right(beat_times, end_segment)

            # Check if there are beat intervals within the segment
            if start_beat_idx < end_beat_idx:
                start_time = beat_times[start_beat_idx]
                end_time = beat_times[end_beat_idx - 1]

                # Ensure selected timestamps are within video duration
                if end_time - start_time <= segment_duration:
                    selected_timestamps.add((start_time, end_time))
    finally:
        return sorted(selected_timestamps)