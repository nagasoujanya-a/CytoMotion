import os
import sys
import pandas as pd
import numpy as np

def compute_stats_for_col(values):
    n = len(values)
    mean = values.mean()
    std = values.std()
    median = values.median()
    ci_95 = 1.96 * std / np.sqrt(n) if n > 1 else np.nan
    cv = (std / mean) * 100 if mean != 0 else np.nan
    return {
        "Mean": mean, "Std": std, "Median": median,
        "95% CI": ci_95, "CV%": cv, "Count": n
    }

def generate_summary_table(base_dir, headers):
    summary_rows = []

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.lower().endswith('.csv'):
                file_path = os.path.join(root, file)
                subdir_name = os.path.basename(root)

                # --- Extract Slices, Frame Rate from Log_file.txt ---
                slices = np.nan
                frame_rate = np.nan
                log_path = os.path.join(root, "Log_file.txt")
                if os.path.isfile(log_path):
                    try:
                        with open(log_path, 'r') as log_file:
                            for line in log_file:
                                line = line.strip()
                                if line.startswith("Slices"):
                                    parts = line.split(":")
                                    if len(parts) == 2:
                                        slices = int(parts[1].strip())
                                elif line.startswith("recordedFramerate"):
                                    parts = line.split(":")
                                    if len(parts) == 2:
                                        frame_rate = float(parts[1].strip())
                    except Exception as e:
                        print(f" Error reading Log_file.txt from {log_path}: {e}")

                # --- Read CSV and set headers ---
                try:
                    df = pd.read_csv(file_path, header=None)
                    df.columns = headers
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")
                    continue

                # --- Skip first row for computation ---
                df_data = df.iloc[1:].reset_index(drop=True)

                # Convert duration to seconds
                duration_ms = slices / frame_rate if slices and frame_rate else np.nan
                duration_s = duration_ms / 1.0 if pd.notna(duration_ms) else np.nan

                try:
                    # Extract and convert columns safely
                    def safe_float(col):
                        return pd.to_numeric(df_data[col], errors="coerce").dropna()

                    cd_values = safe_float("Contraction Duration [10% baseline] (ms)")
                    ppt_values = safe_float("Peak to Peak Interval (ms)")
                    ttp_values = safe_float("Time to Peak (ms)")
                    rt_values = safe_float("Relaxation Time (ms)")
                    ca_values = safe_float("Contraction Amplitude (a.u.)")
                    t90_values = safe_float("90-90 Transient (ms)")
                    t50_values = safe_float("50-50 Transient (ms)")
                    t10_values = safe_float("10-10 Transient (ms)")
                    baseline_values = safe_float("Baseline Value (a.u.)")
                    peak_amp_values = safe_float("Peak Amplitude (a.u.)")

                    # --- Handle Peak to Peak edge case (starting from second row) ---
                    if not ppt_values.empty:
                        if len(ppt_values) == 1 and ppt_values.iloc[0] == 0:
                            ppt_values = pd.Series(dtype=float)
                        elif ppt_values.iloc[0] == 0:
                            ppt_values = ppt_values.iloc[1:]

                    # --- Compute statistics ---
                    stats = {
                        "CD": compute_stats_for_col(cd_values),
                        "PPT": compute_stats_for_col(ppt_values),
                        "TTP": compute_stats_for_col(ttp_values),
                        "RT": compute_stats_for_col(rt_values),
                        "CA": compute_stats_for_col(ca_values),
                        "T90": compute_stats_for_col(t90_values),
                        "T50": compute_stats_for_col(t50_values),
                        "T10": compute_stats_for_col(t10_values),
                        "Baseline": compute_stats_for_col(baseline_values),
                        "PeakAmp": compute_stats_for_col(peak_amp_values)
                    }

                    # --- Heart Beat (BPM) ---
                    bpm = np.nan
                    if stats["PPT"]["Mean"] and not np.isnan(stats["PPT"]["Mean"]) and stats["PPT"]["Mean"] != 0:
                        bpm = 60000 / stats["PPT"]["Mean"]
                    bpm_rounded = int(round(bpm)) if pd.notna(bpm) else np.nan

                    # --- Estimated BPM from log ---
                    estimated_bpm = np.nan
                    if pd.notna(duration_s) and duration_s > 0 and stats["CD"]["Count"] > 0:
                        est = (stats["CD"]["Count"] / duration_s) * 60
                        estimated_bpm = int(round(est)) if pd.notna(est) else np.nan

                    # --- Combine all into one row ---
                    summary_row = {
                        "File Name": subdir_name,
                        "Slices": slices,
                        "Video Time (s)": duration_s,
                        "No of Peaks": stats["CD"]["Count"],
                        "Heart Beat (BPM)": bpm_rounded,
                        "Estimated BPM (from log)": estimated_bpm
                    }

                    # Flatten all metric stats
                    for metric, values in stats.items():
                        prefix = metric
                        for key, val in values.items():
                            summary_row[f"{prefix} {key}"] = round(val, 3) if pd.notna(val) else np.nan

                    summary_rows.append(summary_row)

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    # --- Save summary ---
    summary_df = pd.DataFrame(summary_rows)
    output_path = os.path.join(base_dir, "summary-final-updated.csv")
    summary_df.to_csv(output_path, index=False)
    print(f"\n summary-final-updated.csv saved at: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_summary_final.py <base_directory>")
        sys.exit(1)

    base_dir = sys.argv[1]
    if not os.path.isdir(base_dir):
        print(f"Error: '{base_dir}' is not a valid directory.")
        sys.exit(1)

    headers = [
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

    generate_summary_table(base_dir, headers)