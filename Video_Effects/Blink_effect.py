from moviepy.editor import VideoFileClip, concatenate_videoclips, ColorClip

def add_blinking_effect_to_clip(clip, d_on=0.1, d_off=0.1):
    """Apply blinking effect to a video clip."""
    def black_clip(duration, fps):
        return ColorClip(size=(clip.size[0], clip.size[1]), color=(0, 0, 0), duration=duration).set_fps(fps)

    blinking_clips = []
    t = 0
    while t < clip.duration:
        blinking_clips.append(clip.subclip(t, t + d_on))
        blinking_clips.append(black_clip(d_off, clip.fps))
        t += d_on + d_off

    blinking_clip = concatenate_videoclips(blinking_clips)
    blinking_clip = blinking_clip.set_audio(clip.audio)

    return blinking_clip
