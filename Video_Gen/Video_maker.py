from Video_Gen.Synchronize import synchronize_video_with_music
from Time_Stampers.Music_time_stamps import make_music_time_stamps
from Time_Stampers.Bass_time_stamps import detect_bass
from Time_Stampers.Video_time_stamps import select_unique_timestamps
from Time_Stampers.NOT_random_video_time_stamps import make_timestamps
import os
import csv
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

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
def Make_video(desired_video_length,random_audio_file):    
    try:
        # Set variables
        video_path = "Assembly/Download/downloaded_video.mp4"
        audio_path = random_audio_file
        video_timestamps_file = "Util/data/Video_time_stamps/Time_stamps.csv"
        audio_file_name = os.path.splitext(os.path.basename(audio_path))[0]
        music_timestamps_file = os.path.join('Util/data/Music_time_stamps', '{}.csv'.format(audio_file_name))
        output_path = "video_with_music.mp4"

        # Generate music timestamps
        make_music_time_stamps(audio_path)

        # Load beat times from CSV file
        beat_times = []
        with open(music_timestamps_file, 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                beat_times.append(float(row[0]))

        # Load video
        video = VideoFileClip(video_path)
        song = AudioFileClip(random_audio_file)

        # Set Durations 
        video_duration = video.duration
        song_duration = song.duration


        # Adjust video duration to match desired length
        if video.duration > desired_video_length:
            # Trim the video to the desired length
            video = video.subclip(0, desired_video_length)
        elif video.duration < desired_video_length:
            # Repeat the video to match the desired length
            times_to_repeat = int(desired_video_length / video.duration)
            video = concatenate_videoclips([video] * times_to_repeat)
            # Trim excess if needed
            video = video.subclip(0, desired_video_length)

        # Make time stamps for video
        video_timestamps = select_unique_timestamps(video_duration, beat_times, song_duration)

        # Write selected video timestamps to a file
        with open(video_timestamps_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(video_timestamps)

        # Synchronize video with music and add camera shake to 10% of clips
        synchronize_video_with_music(video_path, audio_path, output_path, video_timestamps_file, music_timestamps_file, desired_video_length, shake_percentage=10)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
