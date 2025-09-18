import wave
import numpy as np
import pandas as pd
import sys

def wav_to_csv(wav_filename, csv_filename):
    # Open the WAV file
    with wave.open(wav_filename, 'r') as wav_file:
        # Extract parameters
        n_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        n_frames = wav_file.getnframes()
        
        # Read the raw audio data
        raw_data = wav_file.readframes(n_frames)
        
        # Convert to numpy array
        audio_data = np.frombuffer(raw_data, dtype=np.int16)
        
        # Reshape if stereo
        if n_channels > 1:
            audio_data = audio_data.reshape(-1, n_channels)
            audio_data = audio_data.mean(axis=1)  # Convert to mono by averaging channels
        
        # Calculate time values in seconds
        time_values = np.arange(0, len(audio_data)) / frame_rate
        
        # Resample to 1-second intervals by averaging
        time_intervals = np.arange(0, time_values[-1], 1)
        avg_values = [np.mean(audio_data[int(t * frame_rate):int((t + 1) * frame_rate)]) for t in time_intervals]
        
        # Create a DataFrame
        df = pd.DataFrame({'Time (s)': time_intervals, 'Breath Rate Signal': avg_values})
        
        # Print data to terminal
        print("Processed Data:")
        print(df.to_string(index=False))
        
        # Save to CSV
        df.to_csv(csv_filename, index=False)
        
    print(f"CSV file saved as {csv_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python wav_to_csv.py <input_wav> <output_csv>")
    else:
        wav_to_csv(sys.argv[1], sys.argv[2])
