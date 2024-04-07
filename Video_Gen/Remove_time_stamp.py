from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def time_to_seconds(time_str):
    """Converts time in format 'mm:ss' to seconds."""
    return sum(x * int(t) for x, t in zip([60, 1], time_str.split(":")))

def parse_timestamps(timestamp_str):
    """Parse the input timestamp string and return a list of timestamp ranges."""
    return [timestamp.strip() for timestamp in timestamp_str.split(',')]

def parse_timestamp_range(timestamp_range):
    """Parse a single timestamp range string and return the start and end timestamps."""
    return '-'.join([timestamp.strip() for timestamp in timestamp_range.split('-')])


def remove_timestamps(video_path, timestamp_list):
    # Load the original video
    video = VideoFileClip(video_path)

    # Initialize a list to store video clips without timestamps
    clips_without_timestamps = []

    # Initialize the start time as 0
    start_time = 0

    # Iterate over each timestamp range and remove the corresponding portion from the video
    for timestamp_range in timestamp_list:
        start_str, end_str = timestamp_range.split('-')
        start = time_to_seconds(start_str)
        end = time_to_seconds(end_str)

        # Add the portion of the video before the current timestamp range
        if start > start_time:
            clips_without_timestamps.append(video.subclip(start_time, start))

        # Update the start time for the next iteration
        start_time = end

    # Add the portion of the video after the last timestamp range
    if start_time < video.duration:
        clips_without_timestamps.append(video.subclip(start_time))

    # Concatenate all video clips without timestamps
    final_clip = concatenate_videoclips(clips_without_timestamps)

    # Construct the output path
    output_directory = os.path.dirname(video_path)
    output_filename = os.path.basename(video_path)
    output_filename_no_ext, ext = os.path.splitext(output_filename)
    output_path = os.path.join(output_directory, "output.mp4")

    # Write the final video without timestamps to the output path
    final_clip.write_videofile(output_path, codec='libx264')

    # Close the video file
    video.close()

    # Delete the original input video
    os.remove(video_path)

    # Rename the output video to match the input video's name
    os.rename(output_path, os.path.join(output_directory, output_filename))
