# YouTube Video Downloader (Python)

Simple Python 3 script to download full YouTube videos (video + audio) and merge them into a single `.mp4` file.  

The script is Windows 11 ready and handles file names safely, avoiding issues with spaces and special characters. Temporary files are stored in a `tmp` folder during download and automatically removed after merging.

---

## Features

- Downloads highest quality video and audio streams.
- Merges video and audio using `ffmpeg`.
- Safe file names: replaces special characters with underscores and removes duplicates.
- Default download folder: `E:\Video\YouTube`
- Temporary files saved in `tmp` subfolder and cleaned up automatically.
- Logs progress in the console.

---

## Requirements

- Python 3.10+
- [`pytubefix`](https://github.com/JuanBindez/pytubefix)
- [`ffmpeg`](https://www.gyan.dev/ffmpeg/builds/) installed and added to `PATH`

---

## Installation

1. Install Python 3.10+ from [python.org](https://www.python.org/downloads/windows/) and ensure it is added to `PATH`.

2. Install dependencies:

```bash
pip install pytubefix
```

3. Install `ffmpeg` for Windows:

- Download from [https://www.gyan.dev/ffmpeg/builds/](https://www.gyan.dev/ffmpeg/builds/)
- Extract to a folder, e.g., `C:\ffmpeg\`
- Add `C:\ffmpeg\bin` to the system `PATH`
- Verify with:

```powershell
ffmpeg -version
```

---

## Usage

Run the script from PowerShell or CMD:

```powershell
python download_youtube.py <YouTube_URL> [Output_Folder]
```

- `<YouTube_URL>` — required, the URL of the YouTube video.
- `[Output_Folder]` — optional, default is `E:\Video\YouTube`.

Example:

```powershell
python download_youtube.py "https://www.youtube.com/watch?v=o6rBK0BqL2w"
```

Or specify a different folder:

```powershell
python download_youtube.py "https://www.youtube.com/watch?v=o6rBK0BqL2w" "D:\MyVideos"
```

---

## How it works

1. Initializes the YouTube video object.
2. Downloads the highest resolution video-only stream and the best audio-only stream to a temporary `tmp` folder.
3. Merges video and audio into a single `.mp4` file in the output folder using `ffmpeg`.
4. Deletes all temporary files and removes the `tmp` folder.

---

## License

This project is open-source and available under the MIT License. Feel free to use and modify it as needed.
