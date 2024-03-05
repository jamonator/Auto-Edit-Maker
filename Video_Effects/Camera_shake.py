import random
import cv2
import numpy as np


def add_camera_shake_to_clip(clip, shake_intensity=10):
    """Apply camera shake effect to a video clip."""
    frame_width, frame_height = clip.size
    frame_count = int(clip.duration * clip.fps)

    shake_intensity = max(1, min(shake_intensity, 20))  # Limit shake intensity between 1 and 20

    frames_with_shake = []
    for _ in range(frame_count):
        frame = clip.get_frame(_ / clip.fps)

        # Randomly shift the frame
        dx = random.randint(-shake_intensity, shake_intensity)
        dy = random.randint(-shake_intensity, shake_intensity)
        translation_matrix = np.float32([[1, 0, dx], [0, 1, dy]])
        shifted_frame = cv2.warpAffine(frame, translation_matrix, (frame_width, frame_height))

        frames_with_shake.append(shifted_frame)

    # Function to return the frame at a given timestamp
    def make_frame(t):
        index = min(int(t * clip.fps), len(frames_with_shake) - 1)
        return frames_with_shake[index]

    # Create a new clip with the frames having the camera shake effect
    shaken_clip = clip.set_make_frame(make_frame)

    # Remove the audio from the shaken clip
    shaken_clip = shaken_clip.set_audio(None)

    return shaken_clip
