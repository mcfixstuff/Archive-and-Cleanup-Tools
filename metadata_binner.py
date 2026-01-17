# requirements
# pip install tqdm pillow hachoir
import os
import shutil
from PIL import Image, ExifTags
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata
from tqdm import tqdm
import tkinter as tk
from tkinter import filedialog, messagebox
from collections import defaultdict
from datetime import datetime

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.dng'}
VIDEO_EXTENSIONS = {'.mp4', '.mov', '.avi', '.mkv', '.wmv', '.mts', '.m2ts', '.3gp'}

# This function captures the date taken and uses it to bin the photos
def get_image_date_taken(file_path):
    try:
        image = Image.open(file_path)
        exif = image._getexif()
        if not exif:
            return None
        for tag, value in exif.items():
            decoded = ExifTags.TAGS.get(tag, tag)
            if decoded == "DateTimeOriginal":
                return value.split()[0].replace(":", "-")
    except Exception:
        pass
    return None

# This checks for a year in the file name as a last ditch effort. (good for photos taken from Google Pixel devices)
import re
def get_year_from_filename(file_path):
    """
    Extract year from filenames like:
    PXL_20230817_123456789.jpg
    Screenshot_20240105_093012.png
    """
    filename = os.path.basename(file_path)

    patterns = [
        r'PXL_(\d{4})(\d{2})(\d{2})',
        r'Screenshot_(\d{4})(\d{2})(\d{2})'
    ]

    for pattern in patterns:
        match = re.search(pattern, filename)
        if match:
            year = int(match.group(1))
            # sanity check to avoid garbage years
            if 1990 <= year <= datetime.now().year + 1:
                return year

    return None
# This is if the file is a video.
def get_video_date_taken(file_path):
    try:
        parser = createParser(file_path)
        if not parser:
            return None
        with parser:
            metadata = extractMetadata(parser)
        if metadata:
            date_str = metadata.get('creation_date')
            if date_str:
                return str(date_str.date())
    except Exception:
        pass
    return None

# Get year from file
def get_year_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    date_taken = None
    if ext in IMAGE_EXTENSIONS:
        date_taken = get_image_date_taken(file_path)
    elif ext in VIDEO_EXTENSIONS:
        date_taken = get_video_date_taken(file_path)

    # Primary: EXIF / metadata date
    if date_taken:
        for fmt in ("%Y-%m-%d", "%Y:%m:%d"):
            try:
                return datetime.strptime(date_taken, fmt).year
            except ValueError:
                pass

    # Fallback: filename (Google Pixel format)
    filename_year = get_year_from_filename(file_path)
    if filename_year:
        return filename_year

    # Final fallback
    return None


# Move file to corresponding folder
def move_file_to_folder(file_path, dest_root, year):
    year_str = str(year) if year else "Unspecified Date"
    dest_folder = os.path.join(dest_root, year_str)
    os.makedirs(dest_folder, exist_ok=True)
    shutil.move(file_path, os.path.join(dest_folder, os.path.basename(file_path)))
    return year_str

# Select folder dialog
def select_folder():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Select Folder with Media Files")

def main():
    source_folder = select_folder()
    if not source_folder:
        print("No folder selected. Exiting.")
        return

    all_files = [os.path.join(source_folder, f) for f in os.listdir(source_folder)
                 if os.path.isfile(os.path.join(source_folder, f)) and
                 os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS.union(VIDEO_EXTENSIONS)]

    if not all_files:
        print("No supported image or video files found.")
        return

    count_by_year = defaultdict(int)
    print(f"Processing {len(all_files)} files...\n")

    for file_path in tqdm(all_files, desc="Organizing"):
        year = get_year_from_file(file_path)
        folder_name = move_file_to_folder(file_path, source_folder, year)
        count_by_year[folder_name] += 1

    print("\nDone! Summary:")
    for year_folder in sorted(count_by_year):
        print(f"{year_folder}: {count_by_year[year_folder]:,} files moved")

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()

