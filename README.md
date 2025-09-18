# Human Activity Recognition Dataset: Multi-Modal Sensor Data

## Overview

This repository contains a comprehensive multi-modal dataset for human activity recognition research, featuring physiological and movement data from 14 participants performing standardized activities. The dataset combines smart shirt sensor data (Hexoskin), triaxial accelerometer data, and participant biometric measurements.

## Dataset Components

### 1. Smart Shirt Physiological Data (Hexoskin)
- **Participants**: 14 subjects (001-014)
- **Sample Rate**: 1 Hz
- **Duration**: ~36 minutes per subject
- **Format**: WAV files converted to CSV with metadata

**Sensor Types**:
- **Cardiovascular**: Heart rate, ECG (3-lead), systolic blood pressure
- **Respiratory**: Breathing rate, minute ventilation, tidal volume, abdominal/thoracic respiration
- **Movement**: 3-axis acceleration, activity level, step cadence
- **Metabolic**: Energy expenditure (Mifflin-St Jeor equation)
- **Quality Metrics**: Signal quality indicators for heart rate and breathing rate

### 2. Accelerometer Data
- **Participants**: 41 subjects (001-041)
- **Sample Rate**: 100 Hz
- **Sensor Placement**: Waist, wrist, ankle
- **Activities**: 5 standardized activities with labels

**Activities**:
- `walk_sidewalk`: Natural pace walking
- `walk_upstairs`: Ascending stairs
- `walk_downstairs`: Descending stairs
- `walk_treadmill`: Treadmill walking (2.5 mph)
- `jog_treadmill`: Treadmill jogging (5.5 mph)

### 3. Biometric Data
- **Participants**: 41 subjects
- **Measurements**: 18 quantitative and qualitative variables
- **Variables**: Demographics, anthropometrics, injury history, dominance

## Data Structure

```
data/
├── processed_smartshirt_data/     # Converted CSV files (14 subjects)
│   ├── 001hexoskin/              # Subject 1 data
│   │   ├── heart_rate.csv        # Time series data
│   │   ├── heart_rate.meta.json  # Metadata (sample rate, duration)
│   │   └── ... (21 sensor types × 2 files each)
├── raw_smartshirt_data/          # Original WAV files
├── labeled_activity_data/        # Accelerometer data with activity labels
└── biometrics/                   # Participant characteristics
```

## Data Processing Tools

### WAV to CSV Conversion
- **`wav2csv.py`**: Single file converter with minimal dependencies (numpy only)
- **`batch_wav2csv.py`**: Batch processing with progress tracking and error handling
- **Output**: CSV files with time series data and JSON metadata

### Analysis Tools
- **`analyze_smartshirt_data.py`**: Statistical summaries with denormalization to original units
- **`create_simple_charts.py`**: ASCII visualizations for data exploration

### Research Implementation
- **`har_backend.py`**: Data aggregation and windowing functions for time series analysis
- **Jupyter Notebooks**: Gait analysis, biometric analysis, and shapelet extraction

## Data Format

### Smart Shirt CSV Files
```csv
Time_s,Ch1
0,0.00213623
1,0.00213623
...
```
- **Time_s**: Time in seconds
- **Ch1**: Normalized sensor data (-1 to 1 range)
- **Metadata**: Sample rate, duration, normalization status

### Accelerometer Data
```csv
time,wrist_x,wrist_y,wrist_z,wrist_vm,ankle_x,ankle_y,ankle_z,ankle_vm,waist_x,waist_y,waist_z,waist_vm,person,activity
2023-02-17 11:42:00.000,0.129,-0.156,1.066,1.0850497684438258,-1.047,-0.008,-0.078,1.0499319025536846,-0.156,-1.02,-0.027,1.0322136406771614,001,walk_sidewalk
```
- **Raw acceleration**: X, Y, Z axes for each sensor location
- **Vector magnitude**: Computed magnitude (vm) for each sensor
- **Labels**: Person ID and activity type

## How to Use

### Prerequisites
```bash
# Install required dependencies
pip install numpy pandas matplotlib seaborn scikit-learn
```

### Data Access
The dataset is ready for immediate use. All WAV files have been converted to CSV format with metadata.

### Basic Data Loading
```python
import pandas as pd
import numpy as np

# Load smart shirt data
heart_rate = pd.read_csv('data/processed_smartshirt_data/001hexoskin/heart_rate.csv')

# Load accelerometer data
accel_data = pd.read_csv('data/labeled_activity_data/001_labeled.csv')

# Load biometric data
biometrics = pd.read_csv('data/biometrics/biometrics.csv')
```

### Data Analysis Tools

#### Statistical Summaries
```bash
# Generate comprehensive statistics for all subjects
python tools/analyze_smartshirt_data.py --verbose

# Analyze specific subjects
python tools/analyze_smartshirt_data.py --subjects 001,002,003 --verbose
```

#### Visualization
```bash
# Create ASCII charts and histograms
python tools/create_simple_charts.py --verbose

# Generate visualizations for specific subjects
python tools/create_simple_charts.py --subjects 001,002 --verbose
```

### Research Workflows

#### Human Activity Recognition
```python
# Combine accelerometer and physiological data
from implementations.src.har.har_backend import compilers

# Aggregate all accelerometer data
data = compilers['aggregate'](directory='data/labeled_activity_data/')

# Extract sliding windows for classification
windowed_data, labels = compilers['slide'](data, window=100, step=10)
```

#### Gait Analysis
```python
# Use the provided gait analysis notebook
# implementations/gait_analysis.ipynb

# Extract gait cycles using peak detection
from implementations.src.har.har_backend import compilers
data = compilers['aggregate'](directory='data/labeled_activity_data/')
walking_data = data[data.activity == 'walk_sidewalk']
```

#### Multi-modal Data Fusion
```python
# Load and synchronize different data types
import pandas as pd

# Load smart shirt data (1 Hz)
physio_data = pd.read_csv('data/processed_smartshirt_data/001hexoskin/heart_rate.csv')

# Load accelerometer data (100 Hz)
accel_data = pd.read_csv('data/labeled_activity_data/001_labeled.csv')

# Resample to common time base
physio_resampled = physio_data.set_index('Time_s').resample('0.01S').interpolate()
```

### Data Conversion (If Needed)
```bash
# Convert additional WAV files (if you have new data)
python tools/wav2csv.py input.wav output.csv --normalize

# Batch convert multiple files
python tools/batch_wav2csv.py --input-dir path/to/wav/files --output-dir path/to/csv/files
```

### Custom Analysis
```python
# Denormalize smart shirt data to original units
def denormalize_heart_rate(normalized_values):
    return (normalized_values + 1) / 2 * (200 - 40) + 40

# Load and denormalize
hr_data = pd.read_csv('data/processed_smartshirt_data/001hexoskin/heart_rate.csv')
hr_bpm = denormalize_heart_rate(hr_data['Ch1'])
```

### Research Applications
- **Human Activity Recognition**: Combine accelerometer and physiological data for improved classification
- **Gait Analysis**: Use shapelet extraction for biomechanical pattern recognition
- **Biometric Correlation**: Analyze relationships between physical characteristics and movement patterns
- **Multi-modal Fusion**: Integrate physiological and movement signals for comprehensive health monitoring

## Technical Specifications

### Smart Shirt Data
- **Total Files**: 294 WAV files (21 sensors × 14 subjects)
- **Conversion Status**: 100% successful (verified in `batch_conversion_results.json`)
- **Data Integrity**: Original WAV files preserved alongside converted CSV files
- **Quality Control**: Each measurement includes quality metrics

### Accelerometer Data
- **Total Subjects**: 41 participants
- **Data Points**: ~65,000 samples per subject per activity
- **Coordinate System**: Standardized triaxial accelerometer data
- **Preprocessing**: Vector magnitude computation included

### Biometric Data
- **Variables**: 18 demographic and anthropometric measurements
- **Missing Data**: Documented in dataset
- **Normalization**: Shoe sizes normalized to US men's sizes

## Research Applications

This dataset supports research in:
- **Activity Recognition**: Multi-modal sensor fusion
- **Gait Analysis**: Biomechanical pattern recognition
- **Physiological Monitoring**: Real-time health assessment
- **Biometric Analysis**: Individual characteristic correlation
- **Time Series Analysis**: Shapelet and subsequence extraction

## Dependencies

- **Python 3.7+**
- **NumPy**: For numerical computations
- **Pandas**: For data manipulation (analysis tools)
- **Matplotlib/Seaborn**: For visualization (optional)

---

**Dataset Status**: Complete and ready for research use. All data has been processed and validated for consistency and quality.