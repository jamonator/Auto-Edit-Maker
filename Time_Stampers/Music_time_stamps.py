import librosa
import os
import datetime
import csv

def make_music_time_stamps(input):
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

    # Find beats
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    # Convert beat frames to time
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # Write beat times to CSV file
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Start Time', 'End Time'])
        for start_time, end_time in zip(beat_times[:-1], beat_times[1:]):
            writer.writerow([start_time, end_time])

    # Complete message
    print("Beat times output to {}. \n Process complete.".format(csv_file))