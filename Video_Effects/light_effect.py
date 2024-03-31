from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx import all

def increase_brightness(clip, brightness_factor=1.6, bright_duration=0.1):
    # Apply brightness effect for the first 10% of the clip
    bright_duration = min(bright_duration, clip.duration * 0.1)
    processed_clip = clip.fx(all.colorx, brightness_factor).subclip(0, bright_duration)
    processed_clip = concatenate_videoclips([processed_clip, clip.subclip(bright_duration)])

    return processed_clip
