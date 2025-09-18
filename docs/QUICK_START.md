# Quick Start Guide - Smart Shirt Data

## 🚀 Get Started in 3 Steps

### 1. Convert WAV Files to CSV
```bash
# Convert all smart shirt data (one command!)
python tools/batch_wav2csv.py --normalize --verbose
```

### 2. Create Easy-to-Read Summaries
```bash
# Generate statistics in original units (BPM, g-forces, etc.)
python tools/analyze_smartshirt_data.py --verbose
```

### 3. Create Visualizations
```bash
# Create ASCII charts and histograms
python tools/create_simple_charts.py --verbose
```

## 📊 What You Get

### Data Files
- **`data/processed_smartshirt_data/`** - All CSV files with sensor data
- **`data/analysis_summaries/`** - Statistics in original units
- **`data/text_visualizations/`** - ASCII charts and histograms

### Key Insights
- **Heart Rate**: ~120 BPM (active during recording)
- **Breathing Rate**: ~19 breaths/min (normal range)
- **Movement**: Good variation in acceleration data
- **Blood Pressure**: ~140 mmHg (slightly elevated)

## 🔧 Tools Available

| Tool | Purpose | Usage |
|------|---------|-------|
| `wav2csv.py` | Convert single WAV file | `python tools/wav2csv.py input.wav` |
| `batch_wav2csv.py` | Convert all WAV files | `python tools/batch_wav2csv.py` |
| `analyze_smartshirt_data.py` | Create summaries | `python tools/analyze_smartshirt_data.py` |
| `create_simple_charts.py` | Create ASCII charts | `python tools/create_simple_charts.py` |

## 📈 Data Types

- **Heart Rate**: Beats per minute (BPM)
- **Breathing Rate**: Breaths per minute
- **Acceleration**: Movement in g-forces (X, Y, Z axes)
- **ECG**: Electrical heart activity
- **Blood Pressure**: Pressure in mmHg
- **Activity**: Activity level (0-100 scale)

## 🎯 Next Steps

1. **Load data in Python**: Use pandas to read CSV files
2. **Combine with accelerometer data**: Merge with `data/labeled_activity_data/`
3. **Analyze patterns**: Use your existing HAR analysis notebooks
4. **Create custom visualizations**: Use matplotlib or other plotting tools

## 📚 Full Documentation

See [WAV2CSV_README.md](WAV2CSV_README.md) for complete documentation.
