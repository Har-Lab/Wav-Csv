#!/usr/bin/env python3
'''
create_simple_charts.py — Create simple text-based visualizations.

This script creates ASCII charts and text-based visualizations
that work without matplotlib or other plotting libraries.

Usage:
  python create_simple_charts.py [options]
'''

import numpy as np
import json
import os
import glob
import argparse

def load_signal_data(csv_path):
    """Load CSV data and metadata."""
    data = np.loadtxt(csv_path, delimiter=',', skiprows=1)
    time_s = data[:, 0]
    ch1_values = data[:, 1]
    
    meta_path = csv_path.replace('.csv', '.meta.json')
    with open(meta_path, 'r') as f:
        metadata = json.load(f)
    
    return time_s, ch1_values, metadata

def denormalize_heart_rate(ch1_values):
    """Convert normalized heart rate back to BPM."""
    return (ch1_values + 1) / 2 * (200 - 40) + 40

def denormalize_breathing_rate(ch1_values):
    """Convert normalized breathing rate back to breaths per minute."""
    return (ch1_values + 1) / 2 * (30 - 8) + 8

def denormalize_acceleration(ch1_values):
    """Convert normalized acceleration back to g-forces."""
    return (ch1_values + 1) / 2 * (20 - (-20)) + (-20)

def create_ascii_chart(values, title, width=60, height=20):
    """Create a simple ASCII chart."""
    if len(values) == 0:
        return f"{title}\nNo data available\n"
    
    # Normalize values to chart height
    min_val = np.min(values)
    max_val = np.max(values)
    if max_val == min_val:
        return f"{title}\nConstant value: {min_val:.3f}\n"
    
    # Sample data if too many points
    if len(values) > width:
        step = len(values) // width
        values = values[::step]
    
    # Scale to chart height
    scaled_values = ((values - min_val) / (max_val - min_val) * (height - 1)).astype(int)
    
    # Create chart
    chart = [[' ' for _ in range(width)] for _ in range(height)]
    
    for i, val in enumerate(scaled_values):
        if i < width:
            chart[height - 1 - val][i] = '*'
    
    # Add title and axis labels
    result = f"{title}\n"
    result += f"Min: {min_val:.3f}, Max: {max_val:.3f}, Mean: {np.mean(values):.3f}\n"
    result += "┌" + "─" * width + "┐\n"
    
    for row in chart:
        result += "│" + "".join(row) + "│\n"
    
    result += "└" + "─" * width + "┘\n"
    
    return result

def create_histogram(values, title, bins=20, width=60):
    """Create a simple ASCII histogram."""
    if len(values) == 0:
        return f"{title} Histogram\nNo data available\n"
    
    # Create histogram
    hist, bin_edges = np.histogram(values, bins=bins)
    max_count = np.max(hist)
    
    if max_count == 0:
        return f"{title} Histogram\nNo variation in data\n"
    
    result = f"{title} Histogram\n"
    result += f"Bins: {bins}, Max count: {max_count}\n"
    result += "┌" + "─" * width + "┐\n"
    
    for i in range(bins):
        count = hist[i]
        bar_length = int((count / max_count) * width)
        bar = "█" * bar_length + " " * (width - bar_length)
        bin_range = f"{bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}"
        result += f"│{bar}│ {bin_range} ({count})\n"
    
    result += "└" + "─" * width + "┘\n"
    
    return result

def create_subject_visualization(subject_dir, subject_id, output_dir):
    """Create visualizations for one subject."""
    print(f"\n📊 Creating visualizations for Subject {subject_id}...")
    
    csv_files = glob.glob(os.path.join(subject_dir, "*.csv"))
    csv_files = sorted(csv_files)
    
    visualization_content = f"""
{'='*80}
SUBJECT {subject_id} - SMART SHIRT DATA VISUALIZATION
{'='*80}

"""
    
    for csv_file in csv_files:
        filename = os.path.basename(csv_file)
        signal_name = filename.replace('.csv', '')
        
        try:
            time_s, ch1_values, metadata = load_signal_data(csv_file)
            
            # Determine signal type and denormalize
            if 'heart_rate' in signal_name and 'quality' not in signal_name:
                original_values = denormalize_heart_rate(ch1_values)
                unit = "BPM"
                title = f"❤️  HEART RATE ({unit})"
            elif 'breathing_rate' in signal_name and 'quality' not in signal_name:
                original_values = denormalize_breathing_rate(ch1_values)
                unit = "breaths/min"
                title = f"🫁 BREATHING RATE ({unit})"
            elif 'acceleration_X' in signal_name:
                original_values = denormalize_acceleration(ch1_values)
                unit = "g"
                title = f"📱 ACCELERATION X ({unit})"
            elif 'acceleration_Y' in signal_name:
                original_values = denormalize_acceleration(ch1_values)
                unit = "g"
                title = f"📱 ACCELERATION Y ({unit})"
            elif 'acceleration_Z' in signal_name:
                original_values = denormalize_acceleration(ch1_values)
                unit = "g"
                title = f"📱 ACCELERATION Z ({unit})"
            else:
                continue  # Skip other signals for now
            
            # Add to visualization
            visualization_content += f"\n{title}\n"
            visualization_content += f"Sample Rate: {metadata['samplerate_hz']} Hz, Duration: {metadata['duration_s']/60:.1f} min\n"
            visualization_content += create_ascii_chart(original_values, f"{title} - Time Series")
            visualization_content += create_histogram(original_values, f"{title}")
            visualization_content += "\n" + "-"*80 + "\n"
            
        except Exception as e:
            visualization_content += f"\n⚠ Error processing {filename}: {e}\n"
    
    # Save visualization
    output_file = os.path.join(output_dir, f'{subject_id}_visualization.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(visualization_content)
    
    print(f"  📄 Visualization saved: {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Create simple text-based visualizations.")
    parser.add_argument("--input-dir", default="data/processed_smartshirt_data",
                       help="Input directory containing processed CSV files")
    parser.add_argument("--output-dir", default="data/text_visualizations",
                       help="Output directory for text visualizations")
    parser.add_argument("--subjects", help="Comma-separated list of subject IDs to visualize")
    parser.add_argument("--verbose", action="store_true", help="Show detailed processing information")
    
    args = parser.parse_args()
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    # Find all subject directories
    subject_dirs = glob.glob(os.path.join(args.input_dir, "*hexoskin"))
    subject_dirs = sorted(subject_dirs)
    
    if not subject_dirs:
        print(f"ERROR: No subject directories found in {args.input_dir}")
        return
    
    # Filter by subjects if specified
    if args.subjects:
        subject_list = [s.strip() for s in args.subjects.split(",")]
        subject_dirs = [d for d in subject_dirs if os.path.basename(d).replace("hexoskin", "") in subject_list]
    
    print(f"📊 Creating text visualizations for {len(subject_dirs)} subjects...")
    print(f"📁 Output directory: {args.output_dir}")
    
    # Process each subject
    for subject_dir in subject_dirs:
        subject_id = os.path.basename(subject_dir).replace("hexoskin", "")
        create_subject_visualization(subject_dir, subject_id, args.output_dir)
    
    print(f"\n✅ Text visualizations complete!")
    print(f"📊 Visualization files saved to: {args.output_dir}")
    print(f"📈 Each file contains:")
    print(f"   - ASCII charts showing data trends")
    print(f"   - Histograms showing data distribution")
    print(f"   - Statistics in original units")
    print(f"   - Easy-to-read text format")

if __name__ == "__main__":
    main()
