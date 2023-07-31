import os
import shutil
import glob
import re

# 1. Ask the user the path of the TV series folder
folder_path = input("Please enter the path of the TV series folder: ")

# 2. Rename all folders and move misplaced files
for dirpath, dirnames, filenames in os.walk(folder_path):
    for dirname in dirnames:
        # Keep the part before and including EXX (where XX are digits), ignoring case
        match = re.match(r"(.*E\d{2})", dirname, re.IGNORECASE)
        if match:
            new_name = match.group(1).title()  # standardize the folder names to title case
            os.rename(os.path.join(dirpath, dirname), os.path.join(dirpath, new_name))

# Move .mkv files from root to episode-specific folders
root_files = os.listdir(folder_path)
for filename in root_files:
    if filename.lower().endswith(".mkv"):
        match = re.match(r"(.*S\d{2}E\d{2})", filename, re.IGNORECASE)
        if match:
            new_name = match.group(1).title()
            new_dir = os.path.join(folder_path, new_name)
            if not os.path.exists(new_dir):
                os.makedirs(new_dir)
            shutil.move(os.path.join(folder_path, filename), os.path.join(new_dir, filename))

# 3. Handle each episode folder
for dirpath, dirnames, filenames in os.walk(folder_path):
    for dirname in dirnames:
        episode_folder = os.path.join(dirpath, dirname)
        subs_folder = os.path.join(episode_folder, "Subs")

        # a. If "Subs" folder exists in the episode directory, move the .srt file to the episode folder root
        #    and rename the .srt file to match the .mkv or .mp4 file
        if os.path.exists(subs_folder):
            video_files = glob.glob(os.path.join(episode_folder, "*.mkv")) + \
                          glob.glob(os.path.join(episode_folder, "*.mp4"))
            if video_files:
                video_file_name = os.path.splitext(os.path.basename(video_files[0]))[0]
                video_match = re.match(r"(.*S\d{2}E\d{2})", video_file_name, re.IGNORECASE)
                if video_match:
                    video_SE = video_match.group(1)
                    srt_files = glob.glob(os.path.join(subs_folder, "*"+video_SE+"*.srt"))
                    if srt_files:
                        srt_file = srt_files[0]  # Choose the first .srt file that matches the pattern
                        shutil.move(srt_file, os.path.join(episode_folder, video_file_name + ".srt"))

            # Remove the "Subs" folder
            shutil.rmtree(subs_folder)

        # b. Remove all files except .srt, .mkv, or .mp4
        for root, dirs, files in os.walk(episode_folder):
            for file in files:
                if not (file.lower().endswith(".srt") or file.lower().endswith(".mkv") or file.lower().endswith(".mp4")):
                    os.remove(os.path.join(root, file))

# Remove remaining .srt files in the root folder
for item in os.listdir(folder_path):
    item_path = os.path.join(folder_path, item)
    if os.path.isfile(item_path) and item.lower().endswith(".srt"):
        os.remove(item_path)

# Remove all empty directories
for dirpath, dirnames, filenames in os.walk(folder_path):
    for dirname in dirnames:
        dir_fullpath = os.path.join(dirpath, dirname)
        if not os.listdir(dir_fullpath):  # check if directory is empty
            os.rmdir(dir_fullpath)
