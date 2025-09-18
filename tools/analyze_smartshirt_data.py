#!/usr/bin/env python3
'''
analyze_smartshirt_data.py — Analyze and summarize smart shirt data.

This script creates easy-to-read summaries and statistics for your smart shirt data,
converting normalized values back to meaningful units.

Usage:
  python analyze_smartshirt_data.py [options]
'''

import numpy as np
import json
import os
import glob
import argparse

def load_signal_data(csv_path):
    """Load CSV data and metadata."""
    # Load CSV data
    data = np.loadtxt(csv_path, delimiter=',', skiprows=1)  # Skip header
    time_s = data[:, 0]
    ch1_values = data[:, 1]
    
    # Load metadata
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

def denormalize_blood_pressure(ch1_values):
    """Convert normalized blood pressure back to mmHg."""
    return (ch1_values + 1) / 2 * (200 - 80) + 80

def denormalize_activity(ch1_values):
    """Convert normalized activity back to activity level."""
    return (ch1_values + 1) / 2 * (100 - 0) + 0

def analyze_signal(csv_path, signal_name):
    """Analyze a signal and return summary statistics."""
    time_s, ch1_values, metadata = load_signal_data(csv_path)
    
    # Determine signal type and denormalize
    if 'heart_rate' in signal_name.lower() and 'quality' not in signal_name:
        original_values = denormalize_heart_rate(ch1_values)
        unit = "BPM"
        normal_range = "60-100 BPM (resting)"
    elif 'breathing_rate' in signal_name.lower() and 'quality' not in signal_name:
        original_values = denormalize_breathing_rate(ch1_values)
        unit = "breaths/min"
        normal_range = "12-20 breaths/min"
    elif 'acceleration' in signal_name.lower():
        original_values = denormalize_acceleration(ch1_values)
        unit = "g"
        normal_range = "±2g (normal movement)"
    elif 'systolic_pressure' in signal_name.lower() and 'adjusted' not in signal_name:
        original_values = denormalize_blood_pressure(ch1_values)
        unit = "mmHg"
        normal_range = "90-140 mmHg"
    elif 'activity' in signal_name.lower() and 'quality' not in signal_name:
        original_values = denormalize_activity(ch1_values)
        unit = "level"
        normal_range = "0-100 scale"
    else:
        original_values = ch1_values
        unit = "normalized"
        normal_range = "N/A"
    
    # Calculate statistics
    stats = {
        'signal_name': signal_name,
        'unit': unit,
        'normal_range': normal_range,
        'sample_rate_hz': metadata['samplerate_hz'],
        'duration_minutes': metadata['duration_s'] / 60,
        'samples': len(original_values),
        'min': original_values.min(),
        'max': original_values.max(),
        'mean': original_values.mean(),
        'std': original_values.std(),
        'median': np.median(original_values),
        'q25': np.percentile(original_values, 25),
        'q75': np.percentile(original_values, 75)
    }
    
    return stats

def create_subject_summary(subject_dir, subject_id, output_dir):
    """Create a summary for all signals of one subject."""
    print(f"\n📊 Analyzing Subject {subject_id}...")
    
    # Find all CSV files for this subject
    csv_files = glob.glob(os.path.join(subject_dir, "*.csv"))
    csv_files = sorted(csv_files)
    
    all_stats = []
    
    for csv_file in csv_files:
        filename = os.path.basename(csv_file)
        signal_name = filename.replace('.csv', '')
        
        try:
            stats = analyze_signal(csv_file, signal_name)
            all_stats.append(stats)
            
            # Print key information
            if 'heart_rate' in signal_name and 'quality' not in signal_name:
                print(f"  ❤️  Heart Rate: {stats['mean']:.1f} {stats['unit']} (range: {stats['min']:.1f}-{stats['max']:.1f})")
            elif 'breathing_rate' in signal_name and 'quality' not in signal_name:
                print(f"  🫁 Breathing Rate: {stats['mean']:.1f} {stats['unit']} (range: {stats['min']:.1f}-{stats['max']:.1f})")
            elif 'acceleration_X' in signal_name:
                print(f"  📱 Acceleration X: {stats['std']:.3f} {stats['unit']} std dev (movement intensity)")
            elif 'acceleration_Y' in signal_name:
                print(f"  📱 Acceleration Y: {stats['std']:.3f} {stats['unit']} std dev (movement intensity)")
            elif 'acceleration_Z' in signal_name:
                print(f"  📱 Acceleration Z: {stats['std']:.3f} {stats['unit']} std dev (movement intensity)")
            elif 'systolic_pressure' in signal_name and 'adjusted' not in signal_name:
                print(f"  🩸 Blood Pressure: {stats['mean']:.1f} {stats['unit']} (range: {stats['min']:.1f}-{stats['max']:.1f})")
            elif 'activity' in signal_name and 'quality' not in signal_name:
                print(f"  🏃 Activity Level: {stats['mean']:.1f} {stats['unit']} (range: {stats['min']:.1f}-{stats['max']:.1f})")
            
        except Exception as e:
            print(f"  ⚠ Error processing {filename}: {e}")
    
    # Save detailed summary to CSV
    if all_stats:
        summary_file = os.path.join(output_dir, f'{subject_id}_summary.csv')
        with open(summary_file, 'w') as f:
            # Write header
            f.write("Signal,Unit,Normal_Range,Sample_Rate_Hz,Duration_Min,Samples,Min,Max,Mean,Std,Median,Q25,Q75\n")
            
            # Write data
            for stats in all_stats:
                f.write(f"{stats['signal_name']},{stats['unit']},{stats['normal_range']},{stats['sample_rate_hz']},{stats['duration_minutes']:.1f},{stats['samples']},{stats['min']:.3f},{stats['max']:.3f},{stats['mean']:.3f},{stats['std']:.3f},{stats['median']:.3f},{stats['q25']:.3f},{stats['q75']:.3f}\n")
        
        print(f"  📄 Detailed summary saved: {summary_file}")
    
    return all_stats

def create_overall_summary(all_subject_stats, output_dir):
    """Create an overall summary across all subjects."""
    print(f"\n📈 Creating Overall Summary...")
    
    # Collect all heart rate data
    heart_rates = []
    breathing_rates = []
    activity_levels = []
    blood_pressures = []
    
    for subject_id, stats_list in all_subject_stats.items():
        for stats in stats_list:
            if 'heart_rate' in stats['signal_name'] and 'quality' not in stats['signal_name']:
                heart_rates.append({
                    'subject': subject_id,
                    'mean_hr': stats['mean'],
                    'min_hr': stats['min'],
                    'max_hr': stats['max']
                })
            elif 'breathing_rate' in stats['signal_name'] and 'quality' not in stats['signal_name']:
                breathing_rates.append({
                    'subject': subject_id,
                    'mean_br': stats['mean'],
                    'min_br': stats['min'],
                    'max_br': stats['max']
                })
            elif 'activity' in stats['signal_name'] and 'quality' not in stats['signal_name']:
                activity_levels.append({
                    'subject': subject_id,
                    'mean_activity': stats['mean'],
                    'min_activity': stats['min'],
                    'max_activity': stats['max']
                })
            elif 'systolic_pressure' in stats['signal_name'] and 'adjusted' not in stats['signal_name']:
                blood_pressures.append({
                    'subject': subject_id,
                    'mean_bp': stats['mean'],
                    'min_bp': stats['min'],
                    'max_bp': stats['max']
                })
    
    # Print overall statistics
    if heart_rates:
        hr_means = [hr['mean_hr'] for hr in heart_rates]
        print(f"\n❤️  HEART RATE SUMMARY ({len(heart_rates)} subjects):")
        print(f"   Average: {np.mean(hr_means):.1f} BPM")
        print(f"   Range: {np.min(hr_means):.1f} - {np.max(hr_means):.1f} BPM")
        print(f"   Std Dev: {np.std(hr_means):.1f} BPM")
    
    if breathing_rates:
        br_means = [br['mean_br'] for br in breathing_rates]
        print(f"\n🫁 BREATHING RATE SUMMARY ({len(breathing_rates)} subjects):")
        print(f"   Average: {np.mean(br_means):.1f} breaths/min")
        print(f"   Range: {np.min(br_means):.1f} - {np.max(br_means):.1f} breaths/min")
        print(f"   Std Dev: {np.std(br_means):.1f} breaths/min")
    
    if activity_levels:
        act_means = [act['mean_activity'] for act in activity_levels]
        print(f"\n🏃 ACTIVITY LEVEL SUMMARY ({len(activity_levels)} subjects):")
        print(f"   Average: {np.mean(act_means):.1f}")
        print(f"   Range: {np.min(act_means):.1f} - {np.max(act_means):.1f}")
        print(f"   Std Dev: {np.std(act_means):.1f}")
    
    if blood_pressures:
        bp_means = [bp['mean_bp'] for bp in blood_pressures]
        print(f"\n🩸 BLOOD PRESSURE SUMMARY ({len(blood_pressures)} subjects):")
        print(f"   Average: {np.mean(bp_means):.1f} mmHg")
        print(f"   Range: {np.min(bp_means):.1f} - {np.max(bp_means):.1f} mmHg")
        print(f"   Std Dev: {np.std(bp_means):.1f} mmHg")

def main():
    parser = argparse.ArgumentParser(description="Analyze and summarize smart shirt data.")
    parser.add_argument("--input-dir", default="data/processed_smartshirt_data",
                       help="Input directory containing processed CSV files")
    parser.add_argument("--output-dir", default="data/analysis_summaries",
                       help="Output directory for analysis summaries")
    parser.add_argument("--subjects", help="Comma-separated list of subject IDs to analyze (e.g., 001,002,003)")
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
    
    print(f"🔍 Analyzing {len(subject_dirs)} subjects...")
    print(f"📁 Output directory: {args.output_dir}")
    
    # Process each subject
    all_subject_stats = {}
    for subject_dir in subject_dirs:
        subject_id = os.path.basename(subject_dir).replace("hexoskin", "")
        stats = create_subject_summary(subject_dir, subject_id, args.output_dir)
        all_subject_stats[subject_id] = stats
    
    # Create overall summary
    create_overall_summary(all_subject_stats, args.output_dir)
    
    print(f"\n✅ Analysis complete!")
    print(f"📊 Summary files saved to: {args.output_dir}")
    print(f"📈 Each subject has a detailed CSV summary with:")
    print(f"   - Original units (BPM, breaths/min, g-forces, mmHg)")
    print(f"   - Statistical measures (mean, std, min, max, quartiles)")
    print(f"   - Normal ranges for comparison")
    print(f"   - Sample rates and durations")

if __name__ == "__main__":
    main()
