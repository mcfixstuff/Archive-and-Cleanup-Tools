import os
import tkinter as tk
from tkinter import filedialog

def select_folder():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Select Folder to Clean .pkf Files")

def format_bytes(num_bytes):
    mb = num_bytes / (1024 * 1024)
    if mb < 750:
        return f"{mb:.2f} MB"
    else:
        gb = mb / 1024
        return f"{gb:.2f} GB"

def delete_pkf_files(folder_path):
    deleted_files = []
    total_bytes_saved = 0

    for dirpath, _, filenames in os.walk(folder_path):
        for filename in filenames:
            if filename.lower().endswith(".pkf"):
                file_path = os.path.join(dirpath, filename)
                try:
                    file_size = os.path.getsize(file_path)
                    os.remove(file_path)
                    deleted_files.append(file_path)
                    total_bytes_saved += file_size
                    print(f"Deleted: {file_path} ({format_bytes(file_size)})")
                except Exception as e:
                    print(f"Error deleting {file_path}: {e}")

    print("\nSummary:")
    if deleted_files:
        print(f"Deleted {len(deleted_files)} .pkf file(s).")
        print(f"Total space saved: {format_bytes(total_bytes_saved)}")
    else:
        print("No .pkf files found.")

if __name__ == "__main__":
    folder = select_folder()
    if folder:
        delete_pkf_files(folder)
    else:
        print("No folder selected. Exiting.")
