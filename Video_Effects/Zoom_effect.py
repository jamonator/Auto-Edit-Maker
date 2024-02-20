import math
from PIL import Image
import numpy as np


def add_zoom_effect(clip, target_zoom_ratio=0.2):
    total_duration = clip.duration

    def effect(get_frame, t):
        # Calculate zoom ratio based on time t within the clip's duration
        if t <= total_duration / 2:
            # Zoom in
            zoom_ratio = (target_zoom_ratio / (total_duration / 2)) * t
        else:
            # Zoom out
            zoom_ratio = target_zoom_ratio - ((target_zoom_ratio / (total_duration / 2)) * (t - (total_duration / 2)))

        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = [
            math.ceil(img.size[0] * (1 + zoom_ratio)),
            math.ceil(img.size[1] * (1 + zoom_ratio))
        ]

        # The new dimensions must be even.
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ]).resize(base_size, Image.LANCZOS)

        result = np.array(img)
        img.close()

        return result

    return clip.fl(effect)