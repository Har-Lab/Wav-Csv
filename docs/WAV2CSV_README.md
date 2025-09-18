# WAV to CSV Conversion Tools

This directory contains enhanced tools for converting WAV audio files to CSV format, specifically designed for processing smart shirt sensor data from the Human Activity Recognition (HAR) project.

## Overview

The smart shirt data contains various physiological and movement signals stored as WAV files. These tools convert them to CSV format for easier analysis and integration with other data processing pipelines.

## Files

- **`wav2csv.py`** - Single-file WAV to CSV converter (requires only numpy)
- **`batch_wav2csv.py`** - Batch processor for converting all WAV files
- **`WAV2CSV_README.md`** - This documentation file

## Installation Requirements

### Required Python Packages

The tools only require numpy, making installation simple and reliable:

```bash
pip install numpy
```

### Installation Issues and Solutions

If you encounter numpy installation problems, try these alternatives:

#### Option 1: Use Conda (Recommended)
```bash
# Install Anaconda or Miniconda first, then:
conda install numpy
```

#### Option 2: Use Pre-compiled Wheels
```bash
# Try installing from conda-forge or use older versions
pip install --only-binary=all numpy==1.24.3
```

#### Option 3: Use Alternative Package Managers
```bash
# Using pip with specific index
pip install -i https://pypi.org/simple/ numpy

# Or try using pip with --no-cache-dir
pip install --no-cache-dir numpy
```

## Usage

### Quick Start

```bash
# Install numpy
pip install numpy

# Convert a single file
python wav2csv.py input.wav

# Convert all WAV files in smart shirt data
python batch_wav2csv.py --normalize --verbose
```

### Single File Conversion

```bash
python wav2csv.py input.wav [output.csv] [--normalize] [--mono]
```

**Options:**
- `--normalize` - Normalize audio to [-1, 1] range
- `--mono` - Mix all channels to single mono channel

**Examples:**
```bash
# Basic conversion
python wav2csv.py data/raw_smartshirt_data/001hexoskin/acceleration_X.wav

# With normalization
python wav2csv.py data/raw_smartshirt_data/001hexoskin/heart_rate.wav --normalize

# Convert to mono
python wav2csv.py data/raw_smartshirt_data/001hexoskin/ECG_I.wav --mono
```

### Batch Processing

```bash
python batch_wav2csv.py [options]
```

**Options:**
- `--input-dir DIR` - Input directory (default: `data/raw_smartshirt_data`)
- `--output-dir DIR` - Output directory (default: `data/processed_smartshirt_data`)
- `--subjects LIST` - Process specific subjects (e.g., `--subjects 001,002,003`)
- `--normalize` - Normalize all audio data
- `--mono` - Mix all channels to mono
- `--verbose` - Show detailed processing
- `--dry-run` - Show what would be processed without converting
- `--resume` - Skip files that already exist

**Examples:**
```bash
# Convert all WAV files with normalization
python batch_wav2csv.py --normalize --verbose

# Process only specific subjects
python batch_wav2csv.py --subjects 001,002,003 --normalize

# Dry run to see what would be processed
python batch_wav2csv.py --dry-run --verbose

# Resume interrupted batch processing
python batch_wav2csv.py --resume --verbose
```

## Output Format

### CSV Structure

The converted CSV files contain:
- **Time_s** - Time in seconds (first column)
- **Ch1** - The actual sensor signal data (normalized between -1 and 1)

### What Ch1 Represents

**Ch1** contains the physiological and movement data from your smart shirt sensors:

- **Heart Rate** (`heart_rate.csv`): Heart rate in beats per minute (BPM)
  - Example: 70 BPM = normal resting heart rate
- **Breathing Rate** (`breathing_rate.csv`): Breathing rate in breaths per minute
  - Example: 12-20 BPM = normal breathing rate
- **Acceleration** (`acceleration_X.csv`, `acceleration_Y.csv`, `acceleration_Z.csv`): Movement in g-forces
  - Example: Small variations = normal movement, larger values = more intense activity
- **ECG Signals** (`ECG_I.csv`, `ECG_II.csv`, `ECG_III.csv`): Electrical heart activity
- **Blood Pressure** (`systolic_pressure.csv`): Blood pressure in mmHg
- **Activity Level** (`activity.csv`): Overall activity intensity
- **Step Cadence** (`cadence.csv`): Steps per minute
- **Ventilation** (`minute_ventilation.csv`, `tidal_volume.csv`): Breathing volume data

### Example Output

```csv
Time_s,Ch1
0,0.002136
1,0.002136
2,0.002136
3,0.002136
...
```

**Note**: The Ch1 values are normalized between -1 and 1. To get the original units (like BPM for heart rate), you need to reverse the normalization process based on the expected range for each signal type.

### Metadata Files

Each conversion creates a `.meta.json` file containing:
- File path and metadata
- Sample rate and duration
- Number of channels and samples
- File size information

## Smart Shirt Data Structure

The smart shirt data contains these WAV file types:

### Physiological Signals
- **heart_rate.wav** - Heart rate data
- **breathing_rate.wav** - Breathing rate data
- **respiration_abdominal.wav** - Abdominal respiration
- **respiration_thoracic.wav** - Thoracic respiration
- **minute_ventilation.wav** - Minute ventilation
- **tidal_volume.wav** - Tidal volume

### Movement Signals
- **acceleration_X.wav** - X-axis acceleration
- **acceleration_Y.wav** - Y-axis acceleration
- **acceleration_Z.wav** - Z-axis acceleration
- **activity.wav** - Activity level
- **cadence.wav** - Step cadence

### Cardiovascular Signals
- **ECG_I.wav** - ECG Lead I
- **ECG_II.wav** - ECG Lead II
- **ECG_III.wav** - ECG Lead III
- **systolic_pressure.wav** - Systolic blood pressure

### Quality and Derived Signals
- **heart_rate_quality.wav** - Heart rate quality metric
- **breathing_rate_quality.wav** - Breathing rate quality metric
- **energy_mifflin_keytel.wav** - Energy expenditure
- **systolic_pressure_adjusted.wav** - Adjusted blood pressure
- **minute_ventilation_adjusted.wav** - Adjusted minute ventilation
- **tidal_volume_adjusted.wav** - Adjusted tidal volume

## Performance Tips

### Memory Management
- Use `--chunk` parameter for large files to control memory usage
- Default chunk size (1,000,000 rows) works well for most files
- Reduce chunk size if you encounter memory issues

### File Size Optimization
- Use `--float-format %.7g` for smaller CSV files
- Use `--avg` to create downsampled versions for quick analysis
- Normalize data with `--normalize` for consistent scaling

### Parallel Processing
- Use `--threads` in batch processing for faster conversion
- Recommended: 2-4 threads depending on your system
- More threads may not always be faster due to I/O limitations

## Troubleshooting

### Common Issues

1. **"ModuleNotFoundError"** - Install required packages (see Installation section)
2. **"Permission denied"** - Check file permissions and close any programs using the files
3. **"Out of memory"** - Reduce `--chunk` size or process files individually
4. **"File not found"** - Check file paths and ensure WAV files exist

### File Format Issues

- The tools expect standard WAV files
- Some proprietary formats may not work
- Check file headers if conversion fails

### Performance Issues

- Large files (>1GB) may take several minutes to process
- Use `--progress` to monitor conversion progress
- Consider using `--avg` for initial analysis of large datasets

## Data Visualization and Analysis

### Easy-to-Read Summaries

Run the analysis script to create easy-to-read summaries with proper units:

```bash
python analyze_smartshirt_data.py [options]
```

This creates:
- **Individual subject summaries** in `data/analysis_summaries/`
- **Statistics in original units** (BPM, breaths/min, g-forces, mmHg)
- **Normal ranges for comparison**
- **Complete statistical measures** (mean, std, min, max, quartiles)

### Visualization Options

**Option 1: Use the Analysis Summaries (Recommended)**
- Text-based summaries with emojis and clear formatting
- CSV files with all statistics
- No additional dependencies required

**Option 1b: Create Text-Based Charts**
```bash
python create_simple_charts.py [options]
```
- ASCII charts showing data trends
- Histograms showing data distribution
- Works without any plotting libraries
- Creates text files with visual representations

**Option 2: Create Charts with Python**
```python
import pandas as pd
import matplotlib.pyplot as plt

# Load heart rate data
hr_data = pd.read_csv('data/processed_smartshirt_data/001hexoskin/heart_rate.csv')

# Create simple plot
plt.figure(figsize=(12, 6))
plt.plot(hr_data['Time_s'] / 60, hr_data['Ch1'] * 160 + 40)  # Convert to BPM
plt.title('Heart Rate Over Time')
plt.xlabel('Time (minutes)')
plt.ylabel('Heart Rate (BPM)')
plt.grid(True)
plt.show()
```

**Option 3: Use External Tools**
- Import CSV files into Excel, Google Sheets, or R
- Use online plotting tools like Plotly or Observable
- Load into Jupyter notebooks for interactive analysis

## Integration with HAR Analysis

The converted CSV files can be used with:

- **Pandas** for data manipulation and analysis
- **NumPy** for numerical computations
- **Matplotlib/Seaborn** for visualization (if installed)
- **Scikit-learn** for machine learning
- **Existing HAR analysis notebooks** in the `implementations/` directory

### Example Integration

```python
import pandas as pd
import numpy as np

# Load converted data
heart_rate = pd.read_csv('data/processed_smartshirt_data/001hexoskin/heart_rate.csv')
acceleration = pd.read_csv('data/processed_smartshirt_data/001hexoskin/acceleration_X.csv')

# Basic analysis
print(f"Heart rate range: {heart_rate['Ch1'].min():.2f} - {heart_rate['Ch1'].max():.2f}")
print(f"Acceleration mean: {acceleration['Ch1'].mean():.4f}")

# Time series analysis
time_diff = heart_rate['Time_s'].diff().mean()
print(f"Average sampling interval: {time_diff:.4f} seconds")
```

## License

This project is part of the LMU HAR Lab Human Activity Recognition research project. See the main project LICENSE file for details.
