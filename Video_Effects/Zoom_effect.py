import math
from PIL import Image
import numpy as np

def add_zoom_effect(clip, target_zoom_ratio=0.2, zoom_duration_ratio=0.1):
    total_duration = clip.duration
    zoom_duration = total_duration * zoom_duration_ratio
    zoom_in_duration = zoom_duration / 2  # Zoom in and out each take half of the zoom duration

    def effect(get_frame, t):
        # Ensure t_start is within the valid range
        t_start = max(0, min(t, total_duration - zoom_duration))

        if t_start <= zoom_in_duration:
            # Calculate zoom ratio for zoom in phase
            zoom_ratio = (target_zoom_ratio / zoom_in_duration) * t_start
        elif t_start <= zoom_duration:
            # Calculate zoom ratio for zoom out phase
            t_out = t_start - zoom_in_duration
            zoom_ratio = target_zoom_ratio - ((target_zoom_ratio / zoom_in_duration) * t_out)
        else:
            # No zoom after the initial zoom effect
            zoom_ratio = 0

        img = Image.fromarray(get_frame(t_start))
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