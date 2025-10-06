import os
import sys
import pandas as pd

# Define the new headers
NEW_HEADERS = [
    "Contraction Duration (10% of baseline)",
    "Time to peak (ms)",
    "Relaxation time (ms)",
    "90-90 transient (ms)",
    "50-50 transient (ms)",
    "10-10 transient (ms)",
    "baseline value (a.u)",
    "Peak amplitude (a.u)",
    "Contraction amplitude (a.u)",
    "Peak to peak time (ms)"
]

def update_csv_file(file_path):
    try:
        df = pd.read_csv(file_path, header=None)
        
        # Insert headers as the first row
        df_with_headers = pd.DataFrame([NEW_HEADERS])
        df = pd.concat([df_with_headers, df], ignore_index=True)

        df.to_csv(file_path, index=False, header=False)
        print(f"[✓] Updated: {file_path}")
    except Exception as e:
        print(f"[!] Failed to process {file_path}: {e}")

def process_directory(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(subdir, file)
                update_csv_file(file_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_csv_headers.py /path/to/root_directory")
        sys.exit(1)

    root_directory = sys.argv[1]
    if not os.path.exists(root_directory):
        print(f"Error: Directory '{root_directory}' not found.")
        sys.exit(1)

    process_directory(root_directory)
