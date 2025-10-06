import os
import re
import sys
import shutil

def rename_videos(base_path):
    # Example: base_path = "CP011_20250609_D25/Plate_1"
    root_name = os.path.basename(os.path.dirname(base_path))  # e.g. CP011_20250609_D25
    plate_name = os.path.basename(base_path)  # e.g. Plate_1

    # Extract CP011 and D25
    match = re.match(r"(CP\d+)_\d{8}_(D\d+)", root_name)
    if not match:
        raise ValueError(f"Root folder name {root_name} not in expected format")
    prefix, day_code = match.groups()

    # Extract plate number
    plate_match = re.match(r"Plate_(\d+)", plate_name)
    if not plate_match:
        raise ValueError(f"Plate folder {plate_name} not in expected format")
    plate_number = int(plate_match.group(1))
    plate_str = f"P{plate_number:03d}"

    # Create output directory for renamed files
    renamed_base = os.path.join(os.path.dirname(base_path), f"{plate_name}_renamed")
    os.makedirs(renamed_base, exist_ok=True)

    # Process .mp4 files directly inside base_path
    for filename in os.listdir(base_path):
        old_path = os.path.join(base_path, filename)
        if not (os.path.isfile(old_path) and filename.lower().endswith(".mp4")):
            continue

        # Capture trailing index (_001, _002, etc.)
        index_match = re.search(r"_(\d{3})\.mp4$", filename)
        if not index_match:
            print(f"Skipping {filename} (no trailing index found)")
            continue
        index_str = index_match.group(1)

        new_filename = f"{prefix}_{day_code}_{plate_str}_{index_str}.mp4"
        new_path = os.path.join(renamed_base, new_filename)

        if os.path.exists(new_path):
            print(f"Skipping {old_path}, target {new_path} already exists")
            continue

        print(f"Copying {old_path} -> {new_path}")
        shutil.copy2(old_path, new_path)  # copy keeps original files

    # Return the renamed folder path so it can be used by validation/conversion
    return renamed_base


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python rename_videos.py <path_to_plate_folder>")
        sys.exit(1)

    base_path = sys.argv[1]
    if not os.path.isdir(base_path):
        print(f"Error: {base_path} is not a valid directory")
        sys.exit(1)

    renamed_folder = rename_videos(base_path)
    print(f"Renamed files stored in: {renamed_folder}")