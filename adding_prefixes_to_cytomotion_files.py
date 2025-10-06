import os
import sys
import re

def extract_tag_from_subfolder(subfolder_name):
    """
    Extract tag from subfolder name.
    Expected format: CPxxx_Dxx_Pxxx_yyy-Contr-Results
    Example: CP012_D33_P001_001-Contr-Results -> CP012_D33_P001_001
    """
    # Match pattern: CPxxx_Dxx_Pxxx_yyy-Contr-Results
    match = re.match(r"(CP\d+)_([D]\d+)_P(\d+)_(\d+)-Contr-Results", subfolder_name)
    if not match:
        print(f"Warning: Subfolder name '{subfolder_name}' doesn't match expected pattern")
        return None

    cp, dxx, plate_num, last_number = match.groups()
    tag = f"{cp}_{dxx}_P{plate_num.zfill(3)}_{last_number}"
    return tag

def prepend_tag_to_files(base_path):
    for subfolder in os.listdir(base_path):
        subfolder_path = os.path.join(base_path, subfolder)
        if not os.path.isdir(subfolder_path):
            continue

        tag = extract_tag_from_subfolder(subfolder)
        if not tag:
            continue

        for filename in os.listdir(subfolder_path):
            old_path = os.path.join(subfolder_path, filename)
            if not os.path.isfile(old_path):
                continue

            # Skip if file already has the tag
            if filename.startswith(tag):
                continue

            new_filename = f"{tag}_{filename}"
            new_path = os.path.join(subfolder_path, new_filename)

            if os.path.exists(new_path):
                print(f" Skipping {old_path}, target {new_path} already exists")
                continue

            print(f"Renaming {old_path} -> {new_path}")
            os.rename(old_path, new_path)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python prepend_tag.py <path_to_base_folder>")
        sys.exit(1)

    base_path = sys.argv[1]
    if not os.path.isdir(base_path):
        print(f" Error: {base_path} is not a valid directory")
        sys.exit(1)

    prepend_tag_to_files(base_path)