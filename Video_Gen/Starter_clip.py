import os
from moviepy.editor import VideoFileClip, concatenate_videoclips
from Util.scripts.Time_converter import parse_timestamp

def extract_clip(input_video_path, start_time, end_time, output_path):
    """Extract specified clip from input video based on start and end times."""
    video_clip = VideoFileClip(input_video_path)
    extracted_clip = video_clip.subclip(start_time, end_time)
    extracted_clip.write_videofile(output_path, codec='libx264', audio_codec='aac', bitrate='5000k', fps=24)
    return extracted_clip

def make_starter_clip(start_timestamp, end_timestamp):
    # Input video path
    input_video_path = "Assembly\Download\downloaded_video.mp4"

    # Parse timestamps to seconds
    start_time = parse_timestamp(start_timestamp)
    end_time = parse_timestamp(end_timestamp)

    # Output path for extracted clip
    output_path = "extracted_clip_TEMP.mp4"

    # Extract and save the clip
    extracted_clip = extract_clip(input_video_path, start_time, end_time, output_path)

    # Path of the video to which the extracted clip will be added
    other_video_path = "video_with_music.mp4"

    # Load the other video
    other_video = VideoFileClip(other_video_path)

    # Concatenate the extracted clip with the other video
    final_clip = concatenate_videoclips([extracted_clip, other_video])

    # Output path for the final video
    output_video_path = "video_with_starter_clip.mp4"

    # Write the final video to the output path
    final_clip.write_videofile(output_video_path, codec='libx264', audio_codec='aac', bitrate='5000k', fps=24)

    print("Combining complete.")

    # Clean up by deleting the extracted clip
    os.remove(output_path)
    os.remove(other_video_path)
