from moviepy.editor import VideoFileClip
from moviepy.video.fx import all
import numpy as np

def apply_filter(get_frame, t):
    frame = get_frame(t)
    # Make a copy of the frame to avoid read-only error
    modified_frame = frame.copy().astype(float)  # Convert to float
    # Increase blue and red channels, reduce green channel
    modified_frame[:, :, 0] *= 1.1  # Increase blue
    modified_frame[:, :, 1] *= 0.9  # Reduce green
    modified_frame[:, :, 2] *= 1.1  # Increase red
    # Clip values to stay within [0, 255] range
    modified_frame = np.clip(modified_frame, 0, 255)
    return modified_frame.astype(np.uint8)  # Convert back to uint8

def add_sunrise_filter(clip):
    # Load the video clip
    video_clip = clip
    
    # Apply the filter
    filtered_clip = video_clip.fl(apply_filter)

    # Increase brightness 
    filtered_clip = filtered_clip.fx(all.colorx, 1.3)
    
    return filtered_clip
