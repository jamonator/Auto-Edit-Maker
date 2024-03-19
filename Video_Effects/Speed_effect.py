from moviepy.editor import VideoFileClip, concatenate_videoclips
from moviepy.video.fx.speedx import speedx

def Add_speed_effect(clip):
    # Set speed parameters
    speed_up_percentage = 40  # Speed up for 10% of the duration
    
    # Calculate the duration for the fast part and the slow part
    total_duration = clip.duration
    fast_duration = total_duration * (speed_up_percentage / 100)
    slow_duration = total_duration - fast_duration

    # Split the clip into two segments: fast and slow
    fast_clip = clip.subclip(0, fast_duration)
    slow_clip = clip.subclip(fast_duration, total_duration)

    # Calculate the speed factors for the fast and slow segments
    fast_speed_factor = 0.9  # Increase speed by 50% for the fast segment
    slow_speed_factor = 0.7  # Decrease speed by 50% for the slow segment

    # Apply speed changes to the segments
    fast_clip = speedx(fast_clip, factor=fast_speed_factor)
    slow_clip = speedx(slow_clip, factor=slow_speed_factor)

    # Concatenate the two segments
    final_clip = concatenate_videoclips([fast_clip, slow_clip])

    return final_clip