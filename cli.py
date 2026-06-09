import os
import sys
import json
import argparse
from typing import Optional

from core import fetch_metadata, download_media

# CONFIGURATION
CONFIG_FILE = "config.json"

def load_config() -> dict:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}

def save_config(config: dict):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def get_default_folder() -> str:
    config = load_config()
    return config.get("download_folder", os.path.join(os.path.expanduser("~"), "Downloads"))

# HELPER FUNCTIONS
def parse_time(time_str: str) -> Optional[int]:
    """
    Parses a time string like '90', '1:30', or '00:01:30' into raw seconds.
    """
    if not time_str:
        return None
        
    parts = time_str.split(':')
    parts.reverse() # Reverse so seconds are always index 0
    
    try:
        seconds = 0
        if len(parts) > 0:
            seconds += int(parts[0])
        if len(parts) > 1:
            seconds += int(parts[1]) * 60
        if len(parts) > 2:
            seconds += int(parts[2]) * 3600
        return seconds
    except ValueError:
        return None
    
# CLI Setup & Subcommands
def main():
    parser = argparse.ArgumentParser()
    
    # Positional arguments
    parser.add_argument("url", nargs="?", help="The YouTube URL, or 'folder' / 'info' commands")
    parser.add_argument("value", nargs="?", help="The path (for 'folder') or the URL (for 'info')")
    
    # Flags
    parser.add_argument("-a", "--audio", action="store_true", help="Download audio only")
    parser.add_argument("-n", "--native", action="store_true", help="Keep native audio format")
    parser.add_argument("-q", "--quality", type=int, help="Max video height (e.g., 1080)")
    parser.add_argument("-l", "--lang", type=str, help="Audio language code (e.g., en)")
    parser.add_argument("-s", "--start", type=str, help="Start time (seconds or MM:SS)")
    parser.add_argument("-e", "--end", type=str, help="End time (seconds or MM:SS)")
    parser.add_argument("-t", "--title", type=str, help="Custom filename")
    parser.add_argument("-o", "--output", type=str, help="Custom download folder for this run")
    parser.add_argument("-d", "--defaults", action="store_true", help="Skip prompts and use defaults")

    args = parser.parse_args()

    # If no URL or command is provided, show help
    if not args.url:
        parser.print_help()
        sys.exit(0)

    # Subcommand: dyt folder
    if args.url.lower() == "folder":
        if args.value:
            config = load_config()
            config["download_folder"] = args.value
            save_config(config)
            print(f"Default download folder saved: {args.value}")
        else:
            print(f"Current download folder: {get_default_folder()}")
        sys.exit(0)

    # Subcommand: dyt info <url>
    if args.url.lower() == "info":
        if not args.value:
            print("Error: Please provide a URL after 'info'")
            sys.exit(1)
        
        print(f"Fetching metadata for: {args.value}\n")
        try:
            data = fetch_metadata(args.value)
            print("--- Video Metadata ---")
            for key, value in data.items():
                print(f"{key.capitalize()}: {value}")
        except Exception as e:
            print(f"Error fetching metadata: {e}")
        sys.exit(0)

    # If it wasn't a subcommand, the first argument is our target URL
    target_url = args.url
    if not args.defaults:
        print(f"Fetching metadata for: {target_url}...")
    try:
        meta = fetch_metadata(target_url)
        if not args.defaults:
            print(f"\n--- Video: {meta['title']} ({meta['duration']}s) ---")
    except Exception as e:
        print(f"Error fetching metadata: {e}")
        sys.exit(1)

    # 1. Audio Only?
    audio_only = args.audio
    if not audio_only and not args.defaults:
        ans = input("Download audio only? (y/n, default n): ").strip().lower()
        if ans == 'y':
            audio_only = True

    # 2. Keep Native Audio?
    keep_native = args.native
    if audio_only and not keep_native and not args.defaults:
        ans = input("Keep native format instead of MP3? (y/n, default n): ").strip().lower()
        if ans == 'y':
            keep_native = True

    # 3. Video Quality
    max_height = args.quality
    if not audio_only and not max_height and not args.defaults:
        print(f"Available Resolutions: {meta['resolutions']}")
        ans = input("Enter max height (e.g., 1080) or press Enter for best: ").strip()
        if ans.isdigit():
            max_height = int(ans)

    # 4. Audio Language
    audio_lang = args.lang
    # Only prompt for language if there are actually multiple audio tracks
    if not audio_lang and not args.defaults and len(meta['languages']) > 1:
        print(f"Available Languages: {meta['languages']}")
        ans = input("Enter language code (or press Enter for default): ").strip()
        if ans:
            audio_lang = ans

    # 5. Trimming
    start_time = parse_time(args.start) if args.start else None
    end_time = parse_time(args.end) if args.end else None
    
    if not args.start and not args.end and not args.defaults:
        s_ans = input("Enter start time (e.g., 01:30 or 90) or press Enter to skip: ").strip()
        if s_ans: 
            start_time = parse_time(s_ans)
            
        e_ans = input("Enter end time (e.g., 02:00 or 120) or press Enter to skip: ").strip()
        if e_ans: 
            end_time = parse_time(e_ans)

    # 6. Custom Title and Folder
    title = args.title
    if not title and not args.defaults:
        ans = input("Enter custom title (or press Enter to keep original): ").strip()
        if ans:
            title = ans
            
    final_folder = args.output if args.output else get_default_folder()

    try:
        saved_path = download_media(
            url=target_url,
            download_folder=final_folder,
            audio_only=audio_only,
            keep_native_audio=keep_native,
            max_height=max_height,
            audio_lang=audio_lang,
            start_time=start_time,
            end_time=end_time,
            title=title
        )
        print(f"\nSUCCESS! File saved to: {saved_path}")
        
        try:
            from win11toast import toast
            folder_uri = f'file:///{os.path.dirname(saved_path).replace(os.sep, "/")}'
            toast('Download Complete', f"Saved: {os.path.basename(saved_path)}", on_click=folder_uri)
        except ImportError:
            pass # Fails silently if not on Windows
            
    except Exception as e:
        print(f"\nDownload Error: {e}")
        sys.exit(1)
if __name__ == "__main__":
    main()