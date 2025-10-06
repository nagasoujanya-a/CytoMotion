import sys
import os

# Import functions
from update_csv_file_headers_2 import process_directory  
from generate_summary_file import generate_summary_table  
from adding_prefixes_to_cytomotion_files import prepend_tag_to_files

# Headers list
HEADERS = [
    "Contraction Duration [10% baseline] (ms)",
    "Time to Peak (ms)",
    "Relaxation Time (ms)",
    "90-90 Transient (ms)",
    "50-50 Transient (ms)",
    "10-10 Transient (ms)",
    "Baseline Value (a.u.)",
    "Peak Amplitude (a.u.)",
    "Contraction Amplitude (a.u.)",
    "Peak to Peak Interval (ms)"
]

def check_file_count(base_dir, expected_count=96, log_file="ERR_FILE_COUNT.log"):
    """
    Check that each subfolder in base_dir has the expected number of files.
    If not, write an error log.
    """
    errors = []

    for subfolder in os.listdir(base_dir):
        subfolder_path = os.path.join(base_dir, subfolder)
        if not os.path.isdir(subfolder_path):
            continue

        # Count only files
        num_files = len([f for f in os.listdir(subfolder_path) if os.path.isfile(os.path.join(subfolder_path, f))])
        if num_files != expected_count:
            errors.append(f" Subfolder '{subfolder}' has {num_files} files (expected {expected_count})")

    if errors:
        with open(log_file, "w") as f:
            for line in errors:
                f.write(line + "\n")
        print(f" File count errors found. See {log_file}")
    else:
        print(f" All subfolders have {expected_count} files.")


def main(base_dir):
    if not os.path.isdir(base_dir):
        print(f"Error: '{base_dir}' is not a valid directory.")
        sys.exit(1)

    print("STEP 1: Adding headers to CSV files - START")
    process_directory(base_dir)
    print("STEP 1: Adding headers - COMPLETED\n")

    print("STEP 2: Generating summary CSV - START")
    generate_summary_table(base_dir, HEADERS)
    print("STEP 2: Summary generation - COMPLETED\n")

    print("STEP 3: Adding prefixes to cytomotion output files - START")
    prepend_tag_to_files(base_dir)
    print("STEP 3: Adding prefixes to cytomotion output files - COMPLETED\n")

    print("STEP 4: Checking file counts in subfolders - START")
    check_file_count(base_dir)
    print("STEP 4: File count check - COMPLETED\n")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main_script.py <base_directory>")
        sys.exit(1)

    base_directory = sys.argv[1]
    main(base_directory)