# TV Series Organizer

TV Series Organizer is a Python script designed to automate the process of organizing your TV series collections. It cleans and structures the directories of your TV series, providing a clean, consistent, and convenient file structure.

## Features

1. **Folder Renaming:** Renames episode folders to a standard format ("Show Name SXXEXX").
2. **File Relocation:** Moves any misplaced video (.mkv) and subtitle (.srt) files into their correct episode folders.
3. **Subtitle Handling:** If a "Subs" folder exists within an episode folder, the script copies the most recently modified subtitle file to the root of the episode folder and renames it to match the corresponding video file.
4. **File Cleaning:** Removes all files except for the video and subtitle files (.srt, .mkv, .mp4).
5. **Folder Removal:** Deletes the "Subs" folder after the subtitle files have been moved.

## Usage

```bash
python main.py
When prompted, enter the path to your TV series folder.
```

## Important Note

Always back up your data before running this script, as the changes it makes cannot be undone.

## Contributing

Contributions are more than welcome! Please fork the repository and create a Pull Request with your updates.

## License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.