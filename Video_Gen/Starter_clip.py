from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

def extract_segment(video_path, start_time, end_time):
    clip = VideoFileClip(video_path)
    segment = clip.subclip(start_time, end_time)
    return segment

def concatenate_videos(video1_path, video2_path):
    video1 = VideoFileClip(video1_path)
    video2 = VideoFileClip(video2_path)
    final_clip = concatenate_videoclips([video1, video2])
    return final_clip

def make_starter_clip(source_video_path, segment_video_path, start_time, end_time):
    # Extract segment from source video
    segment = extract_segment(source_video_path, start_time, end_time)

    # Load the second video
    video2 = VideoFileClip(segment_video_path)

    # Concatenate segment with the start of the second video
    final_clip = concatenate_videoclips([segment, video2])

    # Define temporary output video path
    temp_output_path = segment_video_path + "TEMP.mp4"

    # Write the final concatenated video to temporary output file
    final_clip.write_videofile(temp_output_path, codec='libx264')

    # Close clips to release resources
    segment.close()
    video2.close()
    final_clip.close()

    # Delete the original segment video file
    os.remove(segment_video_path)

    # Rename temporary output video file to original segment video file name
    os.rename(temp_output_path, segment_video_path)

    print("Video concatenation completed successfully.")
