import os
import sys
from rename_videos_mp4 import rename_videos
from cytomotion_preprocess_validation import validate_files
from convert_mp4_to_uncompressed_avi_2 import convert_all_mp4_to_avi

# -------------------------------
# Import or define your three functions
# -------------------------------
# 1. rename_videos(base_path) -> outputs renamed files in a folder
# 2. validate_files(path) -> the validation function we wrote
# 3. convert_mp4_to_avi(path) -> converts all mp4s in path to avi

def main(base_path):
    print("=== WORKFLOW START ===")
    
    # Step 1: Rename MP4s
    print("STEP 1: Renaming MP4s - START")
    renamed_path = rename_videos(base_path)  # Should return the folder with renamed files
    print("STEP 1: Renaming MP4s - COMPLETED\n")
    
    # Step 2: Validate renamed files
    print("STEP 2: Validation - START")
    validate_files(renamed_path)
    print("STEP 2: Validation - COMPLETED\n")
    
    # Step 3: Convert MP4 to AVI
    print("STEP 3: MP4 → AVI Conversion - START")
    convert_all_mp4_to_avi(renamed_path)
    print("STEP 3: MP4 → AVI Conversion - COMPLETED\n")
    
    print("=== WORKFLOW COMPLETED ===")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main_workflow.py <path_to_folder>")
        sys.exit(1)

    base_path = sys.argv[1]
    if not os.path.isdir(base_path):
        print(f"Error: {base_path} is not a valid directory")
        sys.exit(1)

    main(base_path)








