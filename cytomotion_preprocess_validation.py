import os
import re
import sys

COUNTER_FILE = "run_counter.txt"
FINAL_LOG = "Validation_log.log"

def get_run_number():
    """Get and increment run counter."""
    if os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "r") as f:
            n = int(f.read().strip())
    else:
        n = 0
    n += 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(n))
    return n

def write_log(run_number, suffix, messages):
    """Write messages to a numbered error log file."""
    filename = f"ERR_{run_number}_{suffix}.log"
    with open(filename, "w", encoding="utf-8") as f:
        for msg in messages:
            f.write(msg + "\n")
    print(f"❌ Wrote log: {filename}")

def validate_files(path):
    print("PRE_START")
    run_number = get_run_number()
    log_messages = [f"Validation Run: {run_number}", f"Folder: {path}", ""]

    # Collect all mp4 files
    files = [
        os.path.join(path, f)
        for f in os.listdir(path)
        if f.lower().endswith(".mp4") and os.path.isfile(os.path.join(path, f))
    ]

    all_passed = True

    # --- Check 1: Name consistency ---
    pattern = re.compile(r"^(CP\d+)_D\d+_P\d{3}_\d{3}\.mp4$")
    inconsistent = [os.path.basename(f) for f in files if not pattern.match(os.path.basename(f))]
    if inconsistent:
        log_messages.append("Name consistency: FAILED")
        log_messages.append("Inconsistent filenames:")
        log_messages.extend(inconsistent)
        write_log(run_number, "PRE_FILE_INCONSISTENT", ["Inconsistent filenames:"] + inconsistent)
        all_passed = False
    else:
        log_messages.append("Name consistency: PASSED")

    # --- Check 2: File count ---
    if len(files) == 96:
        log_messages.append("File count (96): PASSED")
    else:
        log_messages.append(f"File count: FAILED (found {len(files)} instead of 96)")
        write_log(run_number, "PRE_FILE_COUNT", [f"File count mismatch: found {len(files)} instead of 96"])
        all_passed = False

    # --- Check 3: Uniqueness ---
    seen = set()
    duplicates = []
    for f in files:
        name = os.path.basename(f)
        if name in seen:
            duplicates.append(name)
        else:
            seen.add(name)

    if duplicates:
        log_messages.append("Filename uniqueness: FAILED")
        log_messages.append("Duplicate filenames:")
        log_messages.extend(duplicates)
        write_log(run_number, "PRE_FILE_DUPLICATES", ["Duplicate filenames:"] + duplicates)
        all_passed = False
    else:
        log_messages.append("Filename uniqueness: PASSED")

    # --- Write final log (UTF-8) ---
    with open(FINAL_LOG, "a", encoding="utf-8") as f:
        f.write("\n".join(log_messages))
        f.write("\n" + "="*50 + "\n")  # Separator for next run

    print("PRE_COMPLETED")
    if all_passed:
        print("OK")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python validate_videos.py <path>")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.isdir(path):
        print(f"Error: {path} is not a valid directory")
        sys.exit(1)

    validate_files(path)