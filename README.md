# YouTube Downloader (dyt)

A minimal YouTube downloader powered by `yt-dlp`. Features video quality and language audio track selection and trimming.

## Installation Guide

To use this downloader, you will need a few system-level dependencies installed and available on your system `PATH`.

### 1. System Dependencies

* **[Python](https://www.python.org/downloads/)** (3.8+)
* **[FFmpeg](https://ffmpeg.org/download.html)**: Required for merging audio/video and native trimming.
* **[Deno](https://deno.land/)**: A fast JavaScript runtime used by `yt-dlp` to quickly execute YouTube's cipher algorithms.

**Important:** Verify your installations by opening a terminal and running `python --version`, `ffmpeg -version`, and `deno --version`.

### 2. Project Setup

1. **Clone the repository:**
```bash
git clone https://github.com/antonzhakov/dyt.git
cd dyt
```

2. **Create and activate a virtual environment:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

3. **Install Python dependencies:**
```powershell
pip install -r requirements.txt
```

*(Note: If you want to use the `dyt` command from anywhere on your computer, you must add the `dyt` project directory to your Windows System `PATH`. You can do this instantly by running this command in PowerShell while inside the `dyt` folder:)*
```powershell
[Environment]::SetEnvironmentVariable("PATH", $Env:PATH + ";$PWD", [EnvironmentVariableTarget]::User)
```

*(After running this command, you will need to restart your terminal for the changes to take effect.)*

## Usage
You can launch the downloader using the global `dyt` command. It features a hybrid interface: you can use the interactive wizard, or bypass it entirely using command-line flags.
### 1. Configuration & Utilities
- **Set default download folder:** `dyt folder "C:\Path\To\Downloads"`
- **View current download folder:** `dyt folder`
- **Inspect video metadata:** `dyt info <url>`
### 2. Interactive Wizard
If you just provide a URL, the script will fetch the metadata and pause to ask you exactly how you want to download it (quality, audio language, trimming, custom title).
```powershell
dyt "https://youtube.com/watch?v=dQw4w9WgXcQ"
```
### 3. Fast / Silent Mode (Flags)
You can skip the interactive wizard by providing your preferences as flags. Add the `--defaults` (or `-d`) flag to tell the script to silently use default values for any flags you *didn't* specify (e.g. no trim, original title, best quality).
**Available Flags:**
- `-a`, `--audio`: Download audio only (converts to MP3 by default).
- `-n`, `--native`: Keep native audio format (skip MP3 conversion).
- `-q`, `--quality`: Max video height (e.g., `1080`, `720`).
- `-l`, `--lang`: Audio language code (e.g., `en`, `ru`).
- `-s`, `--start`: Start time (seconds or `MM:SS`).
- `-e`, `--end`: End time (seconds or `MM:SS`).
- `-t`, `--title`: Custom filename.
- `-o`, `--output`: Custom download folder for this specific run.
- `-d`, `--defaults`: Skip remaining interactive prompts.

**Examples:**
Download a 1080p English video silently (no prompts):
```powershell
dyt "https://youtube.com/watch?v=dQw4w9WgXcQ" -q 1080 -l en -d
```
Download just the audio (MP3) of a specific 1-minute segment silently:
```powershell
dyt "https://youtube.com/watch?v=dQw4w9WgXcQ" -a -s 01:30 -e 02:30 -d
```