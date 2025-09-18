#!/usr/bin/env python3
'''
batch_wav2csv.py — Batch WAV to CSV converter.

This script processes all WAV files in the smart shirt data directories,
converting them to CSV format using only numpy.

Usage:
  python batch_wav2csv.py [options]

Options:
  --input-dir DIR       Input directory containing hexoskin folders (default: data/raw_smartshirt_data)
  --output-dir DIR      Output directory for CSV files (default: data/processed_smartshirt_data)
  --subjects LIST       Comma-separated list of subject IDs to process (default: all)
  --normalize           Normalize audio data to [-1, 1] range
  --mono                Mix all channels to mono
  --dry-run             Show what would be processed without actually converting
  --resume              Skip files that already exist in output directory
  --verbose             Show detailed processing information
'''

import argparse
import os
import sys
import glob
import subprocess
from pathlib import Path
from typing import List, Dict
import json
import time


def find_hexoskin_directories(input_dir: str) -> List[str]:
    """Find all hexoskin directories in the input directory."""
    pattern = os.path.join(input_dir, "*hexoskin")
    dirs = glob.glob(pattern)
    return sorted(dirs)


def get_wav_files(hexoskin_dir: str) -> List[str]:
    """Get all WAV files in a hexoskin directory."""
    pattern = os.path.join(hexoskin_dir, "*.wav")
    wav_files = glob.glob(pattern)
    return sorted(wav_files)


def get_subject_id(hexoskin_dir: str) -> str:
    """Extract subject ID from hexoskin directory name."""
    return os.path.basename(hexoskin_dir).replace("hexoskin", "")


def create_output_structure(output_dir: str, subject_id: str) -> str:
    """Create output directory structure for a subject."""
    subject_output_dir = os.path.join(output_dir, f"{subject_id:0>3}hexoskin")
    os.makedirs(subject_output_dir, exist_ok=True)
    return subject_output_dir


def convert_wav_to_csv(wav_file: str, output_dir: str, args) -> tuple:
    """Convert a single WAV file to CSV using the minimal converter."""
    try:
        # Determine output filename
        wav_basename = os.path.splitext(os.path.basename(wav_file))[0]
        output_file = os.path.join(output_dir, f"{wav_basename}.csv")
        
        # Check if file already exists and resume is enabled
        if args.resume and os.path.exists(output_file):
            return wav_file, True, "Skipped (already exists)"
        
        # Build command
        cmd = [sys.executable, "wav2csv.py", wav_file, output_file]
        
        if args.normalize:
            cmd.append("--normalize")
        
        if args.mono:
            cmd.append("--mono")
        
        # Run conversion
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            return wav_file, True, "Success"
        else:
            return wav_file, False, f"Error: {result.stderr.strip()}"
    
    except subprocess.TimeoutExpired:
        return wav_file, False, "Timeout"
    except Exception as e:
        return wav_file, False, f"Exception: {str(e)}"


def process_subject(hexoskin_dir: str, output_dir: str, args) -> Dict:
    """Process all WAV files for a single subject."""
    subject_id = get_subject_id(hexoskin_dir)
    subject_output_dir = create_output_structure(output_dir, subject_id)
    
    wav_files = get_wav_files(hexoskin_dir)
    
    if not wav_files:
        return {
            "subject_id": subject_id,
            "hexoskin_dir": hexoskin_dir,
            "wav_files": [],
            "results": [],
            "summary": {"total": 0, "success": 0, "failed": 0}
        }
    
    results = []
    
    if args.verbose:
        print(f"Processing subject {subject_id} ({len(wav_files)} WAV files)...")
    
    for wav_file in wav_files:
        if args.dry_run:
            results.append({
                "wav_file": wav_file,
                "success": True,
                "message": "Would process"
            })
        else:
            wav_file, success, message = convert_wav_to_csv(wav_file, subject_output_dir, args)
            results.append({
                "wav_file": wav_file,
                "success": success,
                "message": message
            })
            
            if args.verbose:
                status = "✓" if success else "✗"
                print(f"  {status} {os.path.basename(wav_file)}: {message}")
    
    # Calculate summary
    total = len(results)
    success = sum(1 for r in results if r["success"])
    failed = total - success
    
    return {
        "subject_id": subject_id,
        "hexoskin_dir": hexoskin_dir,
        "wav_files": wav_files,
        "results": results,
        "summary": {"total": total, "success": success, "failed": failed}
    }


def print_summary(all_results: List[Dict]):
    """Print processing summary."""
    total_subjects = len(all_results)
    total_files = sum(r["summary"]["total"] for r in all_results)
    total_success = sum(r["summary"]["success"] for r in all_results)
    total_failed = sum(r["summary"]["failed"] for r in all_results)
    
    print("\n" + "="*60)
    print("BATCH PROCESSING SUMMARY")
    print("="*60)
    print(f"Subjects processed: {total_subjects}")
    print(f"Total WAV files: {total_files}")
    print(f"Successfully converted: {total_success}")
    print(f"Failed conversions: {total_failed}")
    print(f"Success rate: {total_success/total_files*100:.1f}%" if total_files > 0 else "N/A")
    
    # Show failed files
    failed_files = []
    for result in all_results:
        for file_result in result["results"]:
            if not file_result["success"]:
                failed_files.append({
                    "subject": result["subject_id"],
                    "file": os.path.basename(file_result["wav_file"]),
                    "error": file_result["message"]
                })
    
    if failed_files:
        print(f"\nFailed files ({len(failed_files)}):")
        for ff in failed_files:
            print(f"  {ff['subject']}: {ff['file']} - {ff['error']}")
    
    print("="*60)


def main():
    ap = argparse.ArgumentParser(description="Batch convert WAV files to CSV.")
    ap.add_argument("--input-dir", default="data/raw_smartshirt_data", 
                   help="Input directory containing hexoskin folders")
    ap.add_argument("--output-dir", default="data/processed_smartshirt_data",
                   help="Output directory for CSV files")
    ap.add_argument("--subjects", help="Comma-separated list of subject IDs to process (e.g., 001,002,003)")
    ap.add_argument("--normalize", action="store_true", help="Normalize audio data to [-1, 1] range")
    ap.add_argument("--mono", action="store_true", help="Mix all channels to mono")
    ap.add_argument("--verbose", action="store_true", help="Show detailed processing information")
    ap.add_argument("--dry-run", action="store_true", help="Show what would be processed without converting")
    ap.add_argument("--resume", action="store_true", help="Skip files that already exist")
    
    args = ap.parse_args()
    
    # Validate input directory
    if not os.path.exists(args.input_dir):
        print(f"ERROR: Input directory not found: {args.input_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Find hexoskin directories
    hexoskin_dirs = find_hexoskin_directories(args.input_dir)
    
    if not hexoskin_dirs:
        print(f"ERROR: No hexoskin directories found in {args.input_dir}", file=sys.stderr)
        sys.exit(1)
    
    # Filter by subjects if specified
    if args.subjects:
        subject_list = [s.strip() for s in args.subjects.split(",")]
        hexoskin_dirs = [d for d in hexoskin_dirs if get_subject_id(d) in subject_list]
        
        if not hexoskin_dirs:
            print(f"ERROR: No matching subjects found for: {args.subjects}", file=sys.stderr)
            sys.exit(1)
    
    # Create output directory
    os.makedirs(args.output_dir, exist_ok=True)
    
    print(f"Found {len(hexoskin_dirs)} hexoskin directories")
    print(f"Input directory: {args.input_dir}")
    print(f"Output directory: {args.output_dir}")
    
    if args.dry_run:
        print("DRY RUN MODE - No files will be converted")
    
    # Process all subjects
    all_results = []
    start_time = time.time()
    
    for hexoskin_dir in hexoskin_dirs:
        result = process_subject(hexoskin_dir, args.output_dir, args)
        all_results.append(result)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    # Print summary
    print_summary(all_results)
    print(f"Total processing time: {processing_time:.1f} seconds")
    
    # Save detailed results
    results_file = os.path.join(args.output_dir, "batch_conversion_results.json")
    with open(results_file, "w") as f:
        json.dump({
            "args": vars(args),
            "processing_time_seconds": processing_time,
            "results": all_results
        }, f, indent=2)
    print(f"Detailed results saved to: {results_file}")


if __name__ == "__main__":
    main()
