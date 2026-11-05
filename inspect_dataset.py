# inspect_dataset.py
# Purpose: Inspect all CSV files in dataset/ and examine the evidence/ directory
# to verify column names, data formats, row counts, and file types without making assumptions.

import csv
import os
import glob
from pathlib import Path

DATASET_DIR = Path("dataset")

def inspect_csv_files(dataset_path: Path):
    """
    Reads every CSV file in the dataset directory, prints its total row count,
    exact header columns, and up to 5 sample rows.
    """
    csv_files = sorted(dataset_path.glob("*.csv"))
    print(f"=== Found {len(csv_files)} CSV files in {dataset_path} ===\n")
    
    for file_path in csv_files:
        print("=" * 80)
        print(f"FILE: {file_path.name}")
        print("=" * 80)
        
        with open(file_path, mode="r", encoding="utf-8", errors="replace") as f:
            reader = csv.reader(f)
            try:
                headers = next(reader)
            except StopIteration:
                print("  [EMPTY FILE]\n")
                continue
                
            print(f"Columns ({len(headers)}): {headers}\n")
            
            sample_rows = []
            total_rows = 0
            for row in reader:
                total_rows += 1
                if len(sample_rows) < 5:
                    sample_rows.append(row)
                    
            print(f"Total Data Rows: {total_rows}")
            print("First 5 Sample Rows:")
            for i, row in enumerate(sample_rows, 1):
                # Print nicely formatted
                row_dict = dict(zip(headers, row))
                print(f"  Row {i}: {row_dict}")
            print("\n")

def inspect_evidence_directory(evidence_path: Path):
    """
    Recursively inspects dataset/evidence/ to summarize subdirectories,
    file counts, extensions, and sample file names.
    """
    print("=" * 80)
    print(f"EVIDENCE DIRECTORY: {evidence_path}")
    print("=" * 80)
    
    if not evidence_path.exists():
        print("  [Evidence directory does not exist]\n")
        return
        
    all_files = [p for p in evidence_path.rglob("*") if p.is_file()]
    print(f"Total Evidence Files: {len(all_files)}\n")
    
    # Categorize by parent subfolder and extension
    categories = {}
    for p in all_files:
        rel = p.relative_to(evidence_path)
        subfolder = rel.parts[0] if len(rel.parts) > 1 else "."
        ext = p.suffix.lower() if p.suffix else "[no extension]"
        
        key = (subfolder, ext)
        if key not in categories:
            categories[key] = []
        categories[key].append(p)
        
    print(f"{'Subfolder':<20} | {'Extension':<15} | {'Count':<8} | Sample Files")
    print("-" * 80)
    for (subfolder, ext), files in sorted(categories.items()):
        samples = ", ".join([f.name for f in files[:3]])
        if len(files) > 3:
            samples += f", ... (+{len(files)-3} more)"
        print(f"{subfolder:<20} | {ext:<15} | {len(files):<8} | {samples}")
    print("\n")

if __name__ == "__main__":
    inspect_csv_files(DATASET_DIR)
    inspect_evidence_directory(DATASET_DIR / "evidence")
