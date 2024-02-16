import librosa
import numpy as np
import datetime
import os
import csv
from moviepy.editor import VideoFileClip


def Make_music_time_stamps(input):
    # Load local audio file
    input_audio_file = input
    y, sr = librosa.load(input_audio_file)

    # Generate CSV file path based on input audio file name
    input_file_name = os.path.splitext(os.path.basename(input_audio_file))[0]
    csv_file = os.path.join('Util\data\Music_time_stamps', '{}.csv'.format(input_file_name))

    # Check if CSV file already exists
    if os.path.exists(csv_file):
        print("Already made:", csv_file)
        return

    # Get file duration in seconds
    duration = librosa.get_duration(y=y, sr=sr)

    # Print duration to console
    print("File duration(s): ", str(datetime.timedelta(seconds=duration)))

    # Find peaks
    onset_env = librosa.onset.onset_strength(y=y, sr=sr,
                                            hop_length=512,
                                            aggregate=np.median)
    peaks = librosa.util.peak_pick(onset_env, pre_max=20, post_max=20, pre_avg=200, post_avg=200, delta=0.7, wait=10)  # Adjust parameters for less sensitivity

    # Print number of timestamps detected
    num_timestamps = len(peaks)
    print("Number of timestamps detected:", num_timestamps)

    # Create output directory if it doesn't exist
    output_dir = 'Util\data\Music_time_stamps'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Write peak times to CSV file
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        prev_peak_time = 0
        for peak_idx, peak_time in enumerate(librosa.frames_to_time(peaks, sr=sr)):
            start_time = prev_peak_time
            end_time = peak_time
            writer.writerow([start_time, end_time])
            prev_peak_time = peak_time

    # Complete message
    print("Peak times output to {}. \n Process complete.".format(csv_file))

# Example usage:
input_audio_file = 'Util\Music\Everywhere I Go - (Police Guy Elevator Dancing Edit).mp3'
Make_music_time_stamps(input_audio_file)
