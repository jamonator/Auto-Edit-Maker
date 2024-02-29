import librosa
import os
import datetime
import csv
from scipy.stats import lognorm, uniform
import IPython.display as ipd
import random

def make_music_time_stamps(input):
    # Load local audio file
    input_audio_file = input

    # Generate CSV file path based on input audio file name
    input_file_name = os.path.splitext(os.path.basename(input_audio_file))[0]
    csv_file = os.path.join('Util\data\Music_time_stamps', '{}.csv'.format(input_file_name))

    # Check if CSV file already exists
    if os.path.exists(csv_file):
        print("Already made:", csv_file)
        return

    try:
        # Load audio file and detect beats
        x, sr = librosa.load(input_audio_file)
        tempo, beat_times = librosa.beat.beat_track(x, sr=sr, start_bpm=80, units='time')

        # Introduce a random slow section
        random_start_index = random.randint(0, len(beat_times) - 2)
        random_end_index = random_start_index + random.randint(1, 5)  # Random duration of the slow part
        slow_factor = random.uniform(1.5, 3.0)  # Random slow factor

        # Adjust timestamps in the slow section
        for i in range(random_start_index, random_end_index + 1):
            beat_times[i] *= slow_factor

        # Write beat times to CSV file
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Start Time', 'End Time'])
            for start_time, end_time in zip(beat_times[:-1], beat_times[1:]):
                writer.writerow([start_time, end_time])

        # Complete message
        print("Beat times output to {}. \n Process complete.".format(csv_file))
    except Exception as e:
        print("Error:", e)
