import numpy as np
from moviepy.video.fx import all as vfx

def Make_sigma_filter(frame):
    # Convert frame to float for arithmetic operations
    frame = frame.astype(float)
    
    # Define a simple sharpening kernel
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    
    # Apply the convolution with the kernel to sharpen the image
    sharpened_frame = np.zeros_like(frame)
    for i in range(3):  # Apply on each channel separately
        sharpened_frame[:, :, i] = np.clip(np.convolve(frame[:, :, i].flatten(), kernel.flatten(), mode='same').reshape(frame.shape[:2]), 0, 255)
    
    return sharpened_frame.astype(np.uint8)

def Add_sigma_filter(clip):
    # Apply sharpening filter to each frame
    filtered_clip = clip.fl_image(Make_sigma_filter)
    
    return filtered_clip
