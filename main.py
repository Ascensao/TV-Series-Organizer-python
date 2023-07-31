import os
import shutil
import glob
import re

# 1. Ask the user the path of the folder of the tv series to work on
folder_path = input("Please enter the path of the TV series folder: ")

# 2. Rename all folders
for dirpath, dirnames, filenames in os.walk(folder_path):
    for dirname in dirnames:
        # Keep the part before and including EXX (where XX are digits)
        match = re.match(r"(.*E\d{2})", dirname)
        if match:
            new_name = match.group(1)
            os.rename(os.path.join(dirpath, dirname), os.path.join(dirpath, new_name))

# 3. Open each folder representing each episode
for dirpath, dirnames, filenames in os.walk(folder_path):
    for dirname in dirnames:
        episode_folder = os.path.join(dirpath, dirname)
        sub_folder = os.path.join(episode_folder, "Subs")
        
        # a. If folder "Subs" exists, copy the .srt file to the root folder of that episode
        #    and rename the sub file equal to the .mkv or .mp4 file but leaving the extension.
        if os.path.exists(sub_folder):
            srt_files = glob.glob(os.path.join(sub_folder, "*.srt"))
            video_files = glob.glob(os.path.join(episode_folder, "*.mkv")) + \
                          glob.glob(os.path.join(episode_folder, "*.mp4"))
            if srt_files and video_files:
                video_file_name = os.path.splitext(os.path.basename(video_files[0]))[0]
                shutil.copy(srt_files[0], os.path.join(episode_folder, video_file_name + ".srt"))
        
        # b. Remove all files except .srt, .mkv or .mp4.
        for root, dirs, files in os.walk(episode_folder):
            for file in files:
                if not (file.endswith(".srt") or file.endswith(".mkv") or file.endswith(".mp4")):
                    os.remove(os.path.join(root, file))
        
        # c. Remove "Subs" folder if exists.
        if os.path.exists(sub_folder):
            shutil.rmtree(sub_folder)
