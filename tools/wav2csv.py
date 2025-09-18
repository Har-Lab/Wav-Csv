#!/usr/bin/env python3
'''
wav2csv.py — WAV → CSV converter with minimal dependencies.

This version only requires numpy, making it simple and reliable to use.

Usage:
  python wav2csv.py input.wav [output.csv] [--normalize] [--mono]
'''

import sys
import os
import json
import wave
import struct
from pathlib import Path

try:
    import numpy as np
except ImportError:
    print("ERROR: numpy is required but not installed.")
    print("Please install with: pip install numpy")
    sys.exit(1)


def read_wav_file(filename):
    """Read WAV file using built-in wave module."""
    try:
        with wave.open(filename, 'rb') as wav_file:
            # Get WAV file parameters
            n_channels = wav_file.getnchannels()
            sample_width = wav_file.getsampwidth()
            framerate = wav_file.getframerate()
            n_frames = wav_file.getnframes()
            
            # Read audio data
            frames = wav_file.readframes(n_frames)
            
            # Convert bytes to numpy array based on sample width
            if sample_width == 1:
                # 8-bit unsigned
                dtype = np.uint8
                data = np.frombuffer(frames, dtype=dtype)
                # Convert to signed
                data = data.astype(np.int16) - 128
            elif sample_width == 2:
                # 16-bit signed
                dtype = np.int16
                data = np.frombuffer(frames, dtype=dtype)
            elif sample_width == 4:
                # 32-bit signed
                dtype = np.int32
                data = np.frombuffer(frames, dtype=dtype)
            else:
                raise ValueError(f"Unsupported sample width: {sample_width}")
            
            # Reshape for multi-channel audio
            if n_channels > 1:
                data = data.reshape(-1, n_channels)
            
            return framerate, data, {
                'n_channels': n_channels,
                'sample_width': sample_width,
                'framerate': framerate,
                'n_frames': n_frames,
                'duration': n_frames / framerate
            }
    
    except Exception as e:
        raise Exception(f"Error reading WAV file: {e}")


def normalize_audio(arr):
    """Normalize audio data to [-1, 1] float32 range."""
    if np.issubdtype(arr.dtype, np.floating):
        out = arr.astype(np.float32)
        return np.clip(out, -1.0, 1.0)
    
    if np.issubdtype(arr.dtype, np.integer):
        info = np.iinfo(arr.dtype)
        denom = float(max(abs(info.min), info.max))
        return (arr.astype(np.float32) / denom).astype(np.float32)
    
    return arr.astype(np.float32)


def mix_to_mono(x):
    """Convert multi-channel audio to mono by averaging channels."""
    if x.ndim == 1:
        return x
    return x.mean(axis=1)


def write_csv_minimal(data, sr, output_path, normalize=False, mix_mono=False):
    """Write audio data to CSV file using minimal numpy operations."""
    print(f"Processing: {output_path}")
    
    # Process data
    x = data
    if normalize:
        print("Normalizing audio data...")
        x = normalize_audio(np.asarray(data))
    
    if mix_mono:
        print("Converting to mono...")
        x = mix_to_mono(x)
    
    # Create time array
    n_samples = x.shape[0]
    time_array = np.arange(n_samples, dtype=np.float64) / float(sr)
    
    # Prepare data for CSV
    if x.ndim == 1:
        # Mono audio
        csv_data = np.column_stack((time_array, x))
        header = "Time_s,Ch1"
    else:
        # Multi-channel audio
        csv_data = np.column_stack((time_array, x))
        n_channels = x.shape[1]
        header = "Time_s," + ",".join([f"Ch{i+1}" for i in range(n_channels)])
    
    # Write CSV file
    print(f"Writing {n_samples} samples to {output_path}...")
    np.savetxt(output_path, csv_data, delimiter=',', header=header, 
               comments='', fmt='%.7g')
    
    print(f"Saved: {output_path}")
    
    # Create metadata
    meta = {
        "input_file": os.path.abspath(sys.argv[1]),
        "output_file": os.path.abspath(output_path),
        "samplerate_hz": sr,
        "samples": n_samples,
        "channels": 1 if x.ndim == 1 else x.shape[1],
        "duration_s": n_samples / float(sr),
        "dtype": str(x.dtype),
        "normalized": normalize,
        "mixed_to_mono": mix_mono
    }
    
    meta_path = Path(output_path).with_suffix('.meta.json')
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
    print(f"Metadata: {meta_path}")
    
    return meta


def main():
    if len(sys.argv) < 2:
        print("Usage: python wav2csv.py input.wav [output.csv] [--normalize] [--mono]")
        print("Options:")
        print("  --normalize  Normalize audio to [-1, 1] range")
        print("  --mono       Mix all channels to mono")
        print("\nNote: This version only requires numpy (no scipy or pandas needed)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    # Parse options
    normalize = '--normalize' in sys.argv
    mix_mono = '--mono' in sys.argv
    
    # Determine output file
    if len(sys.argv) >= 3 and not sys.argv[2].startswith('--'):
        output_file = sys.argv[2]
    else:
        output_file = Path(input_file).with_suffix('.csv')
    
    # Check input file
    if not os.path.exists(input_file):
        print(f"ERROR: File not found: {input_file}")
        sys.exit(1)
    
    try:
        # Read WAV file
        print(f"Reading: {input_file}")
        sr, data, wav_info = read_wav_file(input_file)
        
        # Print file info
        n_samples = data.shape[0]
        n_channels = 1 if data.ndim == 1 else data.shape[1]
        duration = n_samples / float(sr)
        file_size = os.path.getsize(input_file) / (1024 * 1024)
        
        print(f"Sample rate: {sr} Hz")
        print(f"Samples: {n_samples:,}")
        print(f"Channels: {n_channels}")
        print(f"Duration: {duration:.2f} seconds")
        print(f"File size: {file_size:.2f} MB")
        print(f"Data type: {data.dtype}")
        print(f"Sample width: {wav_info['sample_width']} bytes")
        
        # Convert to CSV
        meta = write_csv_minimal(data, sr, output_file, normalize, mix_mono)
        
        print("Conversion completed successfully!")
        
    except Exception as e:
        print(f"ERROR: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
