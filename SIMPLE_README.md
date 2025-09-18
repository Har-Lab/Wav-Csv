# Smart Shirt Data Analysis - Complete Guide

## What This Project Is

This project contains **smart shirt sensor data** from 14 participants who wore Hexoskin smart shirts while performing various activities. The data has been converted from WAV audio files to easy-to-read CSV files for analysis.

## What You Get

### 📊 **Three Types of Data:**

1. **Smart Shirt Data** - Physiological and movement sensors (heart rate, breathing, acceleration, etc.)
2. **Accelerometer Data** - Movement sensors on waist, wrist, and ankle during activities  
3. **Biometric Data** - Physical measurements of each participant (height, weight, age, etc.)

### 🎯 **Activities Performed:**
- Walking on sidewalk (natural pace)
- Walking upstairs
- Walking downstairs  
- Walking on treadmill (2.5 mph)
- Jogging on treadmill (5.5 mph)

## Quick Start (3 Simple Steps)

### Step 1: Convert Data (Already Done!)
```bash
# This has already been completed - all WAV files converted to CSV
python tools/batch_wav2csv.py --normalize --verbose
```

### Step 2: Create Easy-to-Read Summaries
```bash
# Generate statistics in original units (BPM, g-forces, etc.)
python tools/analyze_smartshirt_data.py --verbose
```

### Step 3: Create Visual Charts
```bash
# Create ASCII charts and histograms
python tools/create_simple_charts.py --verbose
```

## Understanding Your Data

### 📁 **File Structure:**
```
data/
├── processed_smartshirt_data/     # ✅ Converted CSV files (ready to use)
│   ├── 001hexoskin/              # Subject 1 data
│   │   ├── heart_rate.csv        # Heart rate data
│   │   ├── heart_rate.meta.json  # Metadata (sample rate, duration, etc.)
│   │   ├── breathing_rate.csv    # Breathing rate data
│   │   ├── acceleration_X.csv    # Movement in X direction
│   │   ├── acceleration_Y.csv    # Movement in Y direction
│   │   ├── acceleration_Z.csv    # Movement in Z direction
│   │   └── ... (21 total files per subject)
│   ├── 002hexoskin/              # Subject 2 data
│   └── ... (14 subjects total)
├── raw_smartshirt_data/          # ⚠️ Original WAV files (still there)
├── labeled_activity_data/        # Accelerometer data with activity labels
└── biometrics/                   # Physical measurements of participants
```

### 🔬 **What Each Smart Shirt File Contains:**

| File Name | What It Measures | Normal Range | Units |
|-----------|------------------|--------------|-------|
| `heart_rate.csv` | Heart beats per minute | 60-100 BPM (resting) | BPM |
| `breathing_rate.csv` | Breaths per minute | 12-20 breaths/min | breaths/min |
| `acceleration_X.csv` | Movement in X direction | ±2g (normal movement) | g-forces |
| `acceleration_Y.csv` | Movement in Y direction | ±2g (normal movement) | g-forces |
| `acceleration_Z.csv` | Movement in Z direction | ±2g (normal movement) | g-forces |
| `ECG_I.csv` | Electrical heart activity (Lead I) | Variable | mV |
| `ECG_II.csv` | Electrical heart activity (Lead II) | Variable | mV |
| `ECG_III.csv` | Electrical heart activity (Lead III) | Variable | mV |
| `systolic_pressure.csv` | Blood pressure | 90-140 mmHg | mmHg |
| `activity.csv` | Overall activity level | 0-100 scale | level |
| `cadence.csv` | Steps per minute | Variable | steps/min |
| `minute_ventilation.csv` | Breathing volume per minute | Variable | L/min |
| `tidal_volume.csv` | Volume per breath | Variable | mL |
| `respiration_abdominal.csv` | Abdominal breathing | Variable | mm |
| `respiration_thoracic.csv` | Chest breathing | Variable | mm |
| `energy_mifflin_keytel.csv` | Energy expenditure | Variable | kcal/day |

### 📈 **Why Multiple Files Per Reading?**

Each measurement type has **multiple versions** because:

1. **Raw vs Adjusted**: Some files have `_adjusted` versions that are corrected for artifacts
2. **Quality Metrics**: Files ending in `_quality` show how reliable each measurement is
3. **Different Sensors**: ECG has 3 leads (I, II, III) for complete heart monitoring
4. **Multiple Axes**: Acceleration is measured in 3 directions (X, Y, Z) for complete movement tracking

**Example**: For heart rate, you get:
- `heart_rate.csv` - The actual heart rate values
- `heart_rate_quality.csv` - How reliable each measurement is (0-1 scale)

## How to Use the Data

### 📊 **CSV File Format:**
Each CSV file has two columns:
- `Time_s` - Time in seconds (0, 1, 2, 3...)
- `Ch1` - The sensor data (normalized between -1 and 1)

### 🔢 **Converting to Real Units:**
The data is normalized, but the analysis tools automatically convert it back:
- **Heart Rate**: `(Ch1 + 1) / 2 * (200 - 40) + 40` = BPM
- **Breathing Rate**: `(Ch1 + 1) / 2 * (30 - 8) + 8` = breaths/min
- **Acceleration**: `(Ch1 + 1) / 2 * (20 - (-20)) + (-20)` = g-forces

### 📱 **Sample Data:**
```csv
Time_s,Ch1
0,0.00213623
1,0.00213623
2,0.00213623
...
```

## Available Tools

| Tool | What It Does | When to Use |
|------|-------------|-------------|
| `wav2csv.py` | Convert single WAV file to CSV | If you have new WAV files |
| `batch_wav2csv.py` | Convert all WAV files at once | Initial data processing |
| `analyze_smartshirt_data.py` | Create easy-to-read summaries | Get overview of all data |
| `create_simple_charts.py` | Make ASCII charts | Visualize data trends |

## Example Results

After running the analysis tools, you'll see results like:
- **Heart Rate**: ~120 BPM (active during recording)
- **Breathing Rate**: ~19 breaths/min (normal range)
- **Movement**: Good variation in acceleration data
- **Blood Pressure**: ~140 mmHg (slightly elevated)

## Integration with Other Data

### 🔗 **Combining with Accelerometer Data:**
The smart shirt data can be combined with the accelerometer data in `data/labeled_activity_data/` to correlate physiological responses with specific activities.

### 📊 **Using in Analysis:**
The data works with:
- **Pandas** for data manipulation
- **NumPy** for numerical computations  
- **Matplotlib/Seaborn** for visualization
- **Scikit-learn** for machine learning
- **Jupyter notebooks** for interactive analysis

## What's Next?

1. **Explore the data**: Look at files in `data/processed_smartshirt_data/`
2. **Run analysis**: Use the tools to create summaries and charts
3. **Combine datasets**: Merge smart shirt data with accelerometer and biometric data
4. **Create visualizations**: Use the existing notebooks as starting points
5. **Research**: Use the data for your human activity recognition research!

## Need Help?

- **Full documentation**: See `docs/WAV2CSV_README.md`
- **Quick reference**: See `docs/QUICK_START.md`
- **Analysis examples**: Check the notebooks in `implementations/`

---

## Summary

✅ **WAV files are converted to CSV** - All 294 WAV files (21 per subject × 14 subjects) have been successfully converted  
✅ **WAV files still exist** - Original files preserved in `data/raw_smartshirt_data/`  
✅ **Multiple files per reading** - Each measurement has raw, adjusted, and quality versions for complete analysis  
✅ **Ready to use** - All data is in CSV format with metadata for easy analysis  

*This project contains comprehensive smart shirt sensor data from 14 participants performing 5 different activities, with tools to analyze and visualize the physiological and movement data.*