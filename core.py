import os
import yt_dlp
from typing import Any, Dict, Optional

def fetch_metadata(url: str) -> dict:
    """
    Fetches and parses video information into a clean dictionary.
    Runs yt-dlp in dry-run mode (no download).
    """
    ydl_opts: Any = {
        "quiet": True,
        "extract_flat": False,
        "remote_components": ["ejs:github"],  # Sometimes needed for cipher parsing
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    if not info:
        raise ValueError("Could not extract metadata. The video may be private or deleted.")

    resolutions = set()
    languages = set()

    formats = info.get("formats") or []

    for f in formats:
        
        # Extract Video Resolutions
        vcodec = f.get("vcodec", "none")
        height = f.get("height")
        if vcodec != "none" and height is not None:
            resolutions.add(height)

        # Extract Audio Languages
        acodec = f.get("acodec", "none")
        lang = f.get("language")
        if acodec != "none" and lang and lang != "None":
            languages.add(lang)

    sorted_resolutions = sorted(list(resolutions), reverse=True)
    
    lang_list = list(languages)
    if not lang_list:
        lang_list = ["default"]

    return {
        "title": info.get("title", "Unknown Title"),
        "duration": info.get("duration", 0),  # In seconds
        "resolutions": sorted_resolutions,
        "languages": lang_list
    }

def download_media(
    url: str,
    download_folder: str,
    audio_only: bool = False,
    keep_native_audio: bool = False,
    max_height: Optional[int] = None,
    audio_lang: Optional[str] = None,
    start_time: Optional[int] = None,
    end_time: Optional[int] = None,
    title: Optional[str] = None
) -> str:
    """
    Downloads media based on strict parameters, returning the final filepath.
    """
    os.makedirs(download_folder, exist_ok=True)
    
    if title:
        outtmpl = os.path.join(download_folder, f"{title}.%(ext)s")
    else:
        outtmpl = os.path.join(download_folder, "%(title)s [%(id)s].%(ext)s")

    ydl_opts: Any = {
        "outtmpl": outtmpl,
        "quiet": False,
        "remote_components": ["ejs:github"],
        "postprocessors": [],
        "force_keyframes_at_cuts": True, # Fixes black screen on trimmed videos
        "merge_output_format": "mp4"     # Fixes missing Windows Properties metadata
    }
    
    if audio_only:
        if audio_lang and audio_lang != "default":
            ydl_opts["format"] = f"bestaudio[language={audio_lang}]"
        else:
            ydl_opts["format"] = "bestaudio"
    else:
        height_filter = f"[height<={max_height}]" if max_height else "" # "" = best available
        
        if audio_lang and audio_lang != "default":
            ydl_opts["format"] = (
                f"bestvideo{height_filter}[protocol^=https]+bestaudio[language={audio_lang}]/"
                f"best{height_filter}[language={audio_lang}]"
            )
        else:
            ydl_opts["format"] = (
                f"bestvideo{height_filter}[protocol^=https]+bestaudio/"
                f"best{height_filter}"
            )
    
    if start_time is not None or end_time is not None:
        
        # yt-dlp expects a callable function that returns a list of dictionaries
        def time_range_func(info_dict, ydl):
            s = start_time if start_time is not None else 0
            e = end_time if end_time is not None else float('inf')
            return [{'start_time': s, 'end_time': e}]
            
        ydl_opts["download_ranges"] = time_range_func
    
    if audio_only and not keep_native_audio:
        ydl_opts["postprocessors"].append({
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
        })
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        
        info = ydl.extract_info(url, download=True)
        
        if not info:
            raise ValueError("Download failed or aborted.")
            
        # Figure out what yt-dlp actually named the file on the disk
        final_filename = ydl.prepare_filename(info)
        
        # If we converted to mp3, yt-dlp changes the file extension post-download.
        # We need to manually update our string to reflect the new .mp3 extension.
        if audio_only and not keep_native_audio:
            base, _ = os.path.splitext(final_filename)
            final_filename = base + ".mp3"
            
        return final_filename