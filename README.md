# Archive-and-Cleanup-Tools
Tools I have made to help archive and clean up files. These are free for anyone to use. If they were helpful for me they might be helpful for you. 

# Bulk WAV to FLAC
Does exactly what you think it does but a little more. 

It uses ffmpeg to convert any wav file to flac. This results in about a 50% file size saving while still mantaining loseless compression in case you want to go back to the files at some point.

The whole purpose I created this was because I had about 2 terabytes of multitracks from band practice I felt I would never touch again but couldn't bring myself to delete it, so I figured if it was half the size I wouldn't mind holding on to it.

How it works: The program will launch a select folder window. After a folder is selected the program will look for wav files through every subfolder. One at a time, it will convert the file to FLAC, place it in the same spot and delete the wav file.

Prerequisites: FFmpeg installed to path. 

If you don't have ffmpeg installed, copy and paste/run the script in "script.txt" then paste this into the terminal/powershell.

$env:Path += ";C:\Users\[USER]\ffmpeg\ffmpeg-7.1.1-essentials_build\bin"

Note: replace [USER] with your username.

In that same terminal, run the .py file.

# PKF cleaner

Shouldn't require any extra setup like the former tool.

Super helpful for a drive full of Adobe Audition files you wont touch for a long long time.

The program will dig through every subfolder of the directory you choose, then find and delete every pkf file.

If you ever choose to reopen the Adobe Audition project at a later date, Audition will generate new pkf files. 

# Metadata Binner

This is a tool that will go through a folder with a bunch of files and bin them into year folders by their metadata.

This is useful for services like MyCloud auto backup that just dumps all your photos and videos into one folder.

Run the python script and it will pop open a window to choose a folder.

Open the folder of files you want to sort. This will not check subfolders.

Let it run.
