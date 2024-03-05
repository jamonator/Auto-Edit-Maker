import numpy as np


def add_vhs_filter(clip):
    """Apply VHS filter effect to a video clip."""
    def vhs_filter(t):
        # Get the frame as a writable copy
        frame = np.copy(clip.get_frame(t))
        if isinstance(frame, list):
            frame = frame[0]

        # Add color distortions
        color_noise = np.random.normal(scale=30, size=frame.shape)
        color_noise[:, :, 0] = 0  # Set red channel to 0 to reduce red noise

        # Combine the original frame with color distortions
        frame = np.clip(frame + color_noise, 0, 255).astype(np.uint8)
        return frame

    return clip.fl(lambda gf, t: vhs_filter(t), apply_to=['mask'])
