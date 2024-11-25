# Davinci Resolve video converter

A Python script to convert all videos to a format that Davinci Resolve supports

Davinci Resolve has to be special on Linux as in [not supporting H.264 and H.265 in the free version](https://documents.blackmagicdesign.com/SupportNotes/DaVinci_Resolve_18_Supported_Codec_List.pdf?_v=1705996810000#page=12)

This tool solves this by re-encoding all the files with `mpeg4` for video and `flac` for audio

The script currently looks for `mp4`, `avi` and `mkv` files

##### Note: re-encoding takes some time, especially on lower end hardware, so dont panic if it looks stuck, the script should detect when encoding finishes or fails

## Usage
1. Install FFmpeg
2. Install the requirements with `pip install -r requirements.txt`
3. Run `main.py`

## Features
- [x] Variable selection of videos
- [x] Basic conversion progress
- [x] Multithreading
- [ ] FFmpeg error logging (currently only logs that something happened)
- [ ] Better converting status description
- [ ] Check if video is already converted
- [ ] Live mode (convert new videos as they are added)

#### Thanks to [this video](https://www.youtube.com/watch?v=WLcW4UWPC5Y) for the ffmpeg parameters