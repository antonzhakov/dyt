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
git clone <your-github-repo-url>
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

## Usage
*(Usage documentation coming soon)*