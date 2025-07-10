import os
import subprocess
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog

def format_bytes(num_bytes):
    mb = num_bytes / (1024 * 1024)
    if mb < 750:
        return f"{mb:.2f} MB"
    else:
        gb = mb / 1024
        return f"{gb:.2f} GB"

def convert_wav_to_flac_ffmpeg(wav_path):
    try:
        output_path = os.path.splitext(wav_path)[0] + ".flac"
        original_size = os.path.getsize(wav_path)

        # FFmpeg command
        cmd = [
            "ffmpeg",
            "-y",                      # Overwrite without asking
            "-i", wav_path,            # Input file
            "-sample_fmt", "s32",      # 24-bit output (as 32-bit signed)
            "-c:a", "flac",            # FLAC codec
            output_path
        ]

        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        compressed_size = os.path.getsize(output_path)
        os.remove(wav_path)  # Delete the original .wav

        space_saved = original_size - compressed_size
        return (wav_path, True, "", space_saved)
    except Exception as e:
        return (wav_path, False, str(e), 0)

def select_folder():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Select Folder with WAV Files")

def process_all_files(folder_path):
    wav_files = []
    for dirpath, _, filenames in os.walk(folder_path):
        for f in filenames:
            if f.lower().endswith(".wav"):
                wav_files.append(os.path.join(dirpath, f))

    results = []
    total_space_saved = 0

    for wav_path in tqdm(wav_files, desc="Converting", unit="file"):
        path, success, err, saved = convert_wav_to_flac_ffmpeg(wav_path)
        results.append((path, success, err))
        total_space_saved += saved

    for path, success, err in results:
        if not success:
            print(f"❌ Failed to convert {path}: {err}")

    print("\n✅ Conversion complete.")
    print(f"💾 You saved {format_bytes(total_space_saved)} by converting to FLAC.")

if __name__ == "__main__":
    folder = select_folder()
    if folder:
        process_all_files(folder)
    else:
        print("No folder selected.")
