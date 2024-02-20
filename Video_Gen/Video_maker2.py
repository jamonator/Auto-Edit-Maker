from Video_Gen.Synchronize import synchronize_video_with_music
from Time_Stampers.Music_time_stamps import make_music_time_stamps
from Time_Stampers.Bass_time_stamps import detect_bass
from Time_Stampers.Video_time_stamps import select_unique_timestamps
import os
import csv
from moviepy.editor import VideoFileClip


def memoize(func):
    cache = {}

    def memoized_func(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result

    return memoized_func
@memoize

def Make_video(quota, random_audio_file):    

    # Set variables:
    video_path = "Assembly\Download\downloaded_video.mp4"
    audio_path = random_audio_file
    video_timestamps_file = "Util\data\Video_time_stamps\Time_stamps.csv"
    audio_file_name = os.path.splitext(os.path.basename(audio_path))[0]
    music_timestamps_file = os.path.join('Util\data\Music_time_stamps', '{}.csv'.format(audio_file_name))
    output_path = "video_with_music.mp4"

    # Generate music timestamps
    make_music_time_stamps(audio_path)
    # detect_bass(audio_path)

    # Load beat times from CSV file
    beat_times = []
    with open(music_timestamps_file, 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # Skip header row
        for row in csv_reader:
            beat_times.append(float(row[0]))

    # Generate and select unique video timestamps based on beat intervals
    video = VideoFileClip(video_path)
    video_duration = video.duration
    video_timestamps = select_unique_timestamps(video_path, quota, video_duration, beat_times)

    # Write selected video timestamps to a file
    with open(video_timestamps_file, 'w') as f:
        writer = csv.writer(f)
        writer.writerows(video_timestamps)

    # Synchronize video with music and add camera shake to 10% of clips
    synchronize_video_with_music(video_path, audio_path, output_path, video_timestamps_file, music_timestamps_file, shake_percentage=10)

