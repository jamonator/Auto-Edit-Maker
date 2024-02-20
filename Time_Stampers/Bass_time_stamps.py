import librosa
import numpy as np
import os
import csv
from scipy.signal import find_peaks
import pandas as pd

def detect_bass(input_audio_file):
    # Set output
    input_file_name = os.path.splitext(os.path.basename(input_audio_file))[0]
    csv_file = os.path.join('Util\data\Music_time_stamps', '{}.csv'.format(input_file_name))

    # Check if CSV file already exists
    if os.path.exists(csv_file):
        print("Already made:", csv_file)
        return

    try:
        # Load the audio file
        y, sr = librosa.load(input_audio_file)

        # Compute the Short-Time Fourier Transform (STFT)
        D = np.abs(librosa.stft(y))

        # Define frequency bands
        bass_freq_range = (20, 30)  # Adjust as needed for your definition of "bass"

        # Find the indices corresponding to the bass frequency range
        bass_indices = librosa.fft_frequencies(sr=sr).searchsorted(bass_freq_range)

        # Sum the magnitudes within the bass frequency range
        bass_magnitudes = np.sum(D[bass_indices[0]:bass_indices[1], :], axis=0)

        # Normalize bass magnitudes
        bass_magnitudes_normalized = (bass_magnitudes - np.mean(bass_magnitudes)) / np.std(bass_magnitudes)

        # Find peaks in the bass magnitudes
        peak_indices, _ = find_peaks(bass_magnitudes_normalized, height=0.5, distance=50)

        # Get time stamps of bass peaks
        bass_timestamps = librosa.frames_to_time(peak_indices)

        # Calculate end times
        end_times = np.append(bass_timestamps[1:], bass_timestamps[-1] + (bass_timestamps[-1] - bass_timestamps[-2]))

        # Write timestamps to CSV file
        df = pd.DataFrame({'Start Time': bass_timestamps, 'End Time': end_times})
        df.to_csv(csv_file, index=False, float_format='%.15f')
    except Exception as e:
        print("Error:", e)