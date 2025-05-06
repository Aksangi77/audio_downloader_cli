#!/usr/bin/env python3
"""
Audio Downloader CLI Tool

This tool downloads audio from a YouTube playlist with embedded metadata
and cover art.
If not provided as arguments, it will prompt for the playlist URL and
output folder.

Usage examples:
    1. Interactive mode (no arguments):
       ./audio_downloader.py

    2. With arguments:
       ./audio_downloader.py "https://youtube.com/playlist?list=PLMC9KNkIncKvYin_USF1qoJQnIyMAfRxl&si=Xh6MevFrjrzQd9Wd" -o ~/Music
"""

import argparse
import os
import subprocess
import sys


def download_audio(playlist_url, output_folder):
    # Expand the tilde (~) in the output folder path
    output_folder = os.path.expanduser(output_folder)

    # Build the yt-dlp command with options
    command = [
        "yt-dlp",
        "--ignore-errors",
        "--format",
        "bestaudio[ext=m4a]",
        "--extract-audio",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "160K",
        "-P",
        output_folder,
        "--output",
        "%(title)s.%(ext)s",
        "--yes-playlist",
        "--embed-metadata",
        "--embed-thumbnail",
        "--add-metadata",
        "--postprocessor-args",
        "-id3v2_version 3",
        "--download-archive",
        os.path.join(output_folder, "downloaded.txt"),
        playlist_url,
    ]

    try:
        subprocess.run(command, check=True)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Exiting gracefully.")
        sys.exit(0)
    except subprocess.CalledProcessError as e:
        print(f"\nAn error occurred during download: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Download YouTube audio efficiently with embedded metadata and cover art."
        )
    )
    parser.add_argument(
        "playlist_url",
        nargs="?",
        default=None,
        help="YouTube playlist URL to download audio from.",
    )
    parser.add_argument(
        "-o",
        "--output-folder",
        default=None,
        help="Output folder for audio files (default: ~/Music)",
    )

    args = parser.parse_args()

    if not args.playlist_url:
        args.playlist_url = input("Enter the YouTube playlist URL: ").strip()

    if not args.output_folder:
        chosen = input(
            "Enter the output folder (Press Enter for default '~/Music'): "
        ).strip()
        args.output_folder = chosen if chosen else "~/Music"

    download_audio(args.playlist_url, args.output_folder)


if __name__ == "__main__":
    main()
