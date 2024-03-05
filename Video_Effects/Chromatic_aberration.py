from moviepy.editor import VideoFileClip, clips_array
import numpy as np

def add_chromatic_aberration(clip, offset=2):
    """
    Applies a chromatic aberration effect to the clip.
    
    Parameters:
        clip (Clip): The input video clip.
        offset (int): The offset for the chromatic aberration effect.
        
    Returns:
        Clip: The modified clip with chromatic aberration effect.
    """
    # Define function for chromatic aberration
    def apply_chromatic_aberration(frame):
        # Splitting the RGB channels
        red, green, blue = frame[:,:,0], frame[:,:,1], frame[:,:,2]

        # Applying offset to each channel
        red_offset = np.roll(red, offset, axis=0)
        green_offset = np.roll(green, -offset, axis=0)
        blue_offset = np.roll(blue, offset, axis=0)

        # Combining the channels with offset
        final_frame = np.dstack((red_offset, green_offset, blue_offset))
        
        return final_frame

    # Apply chromatic aberration effect to each frame
    final_clip = clip.fl_image(apply_chromatic_aberration)

    return final_clip
