from moviepy.editor import concatenate_videoclips
from moviepy.video.fx.speedx import speedx

def Add_speed_effect(clip):
    # Define the percentage of the clip duration to be sped up
    speed_up_percentage = 40

    # Calculate the duration for the fast part and the slow part
    total_duration = clip.duration
    speed_up_duration = total_duration * (speed_up_percentage / 100)
    slow_down_duration = total_duration - speed_up_duration

    # Calculate the speed factor for the speed up segment
    speed_up_factor = total_duration / (total_duration - speed_up_duration)

    # Apply speed changes to the speed up segment
    speed_up_clip = speedx(clip.subclip(0, speed_up_duration), factor=speed_up_factor)

    # Calculate the slow-down factor for the rest of the clip to fill the duration gap
    slow_down_factor = total_duration / (total_duration + slow_down_duration)

    # Apply speed changes to the slow down segment to compensate for the duration gap
    slow_down_clip = speedx(clip.subclip(speed_up_duration), factor=slow_down_factor)

    # Concatenate the speed up and slow down segments
    final_clip = concatenate_videoclips([speed_up_clip, slow_down_clip])

    # Trim the final clip to match the original duration exactly
    final_clip = final_clip.subclip(0, total_duration)

    return final_clip