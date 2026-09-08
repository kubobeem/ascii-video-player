# 🎞️ ASCII Video Player (Color Fork)

A real-time terminal video player that converts **YouTube videos to colorful ASCII art**, streams them frame-by-frame, and renders them directly in your terminal — all offline, and built from scratch.

> Fork of [AddisionS/ascii-video-player](https://github.com/AddisionS/ascii-video-player) with **24-bit truecolor (ANSI) support**.

Original: grayscale only. This fork keeps the original luminance-to-character mapping, but colors each character with the pixel's **true RGB color** using ANSI 24-bit truecolor escape codes (`\x1b[38;2;R;G;Bm`), so the terminal output looks like the actual video instead of gray blobs.

## ✨ New in this fork

- 🎨 **Truecolor output** — every character is colored with its exact RGB pixel value
- ⬛ **Pixel mode** (`--pixel`) — renders frames as solid colored blocks (`█`) instead of characters
- 🏃 **Run-length compressed escapes** — the escape code is only emitted when the color changes, keeping output size small
- 🧵 **Reliable tail playback** — frames left over after ffmpeg finishes are now converted too (original dropped any batch smaller than 90 frames)
- 🪟 **Windows fixes** — stdout is forced to UTF-8 (no more `cp932` UnicodeEncodeError crash with emoji/blocks), and frame writes are atomic (temp file + rename) so the player never reads a half-written frame

## ⚙️ Features

- 🔻 Downloads any YouTube video via `yt-dlp`
- 🧠 Extracts frames using `ffmpeg`
- 🪄 Converts each frame to colored ASCII using Python + Pillow
- 🚀 Plays the video frame-by-frame in your terminal while conversion happens in the background
- 💥 Fully threaded & multiprocessing optimized
- 🧼 Auto-cleans temp files (`video.mp4`, `frames/`, `asciiFrames/`) on exit

## 📦 Requirements

- Python 3.10+
- [ffmpeg](https://ffmpeg.org/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [Pillow](https://pypi.org/project/pillow/)
- [Psutil](https://pypi.org/project/psutil/)

## 🚀 Usage

```bash
# colorful ASCII characters (default)
python main.py

# solid color blocks (pixel art style)
python main.py --pixel
```

Then paste a YouTube URL when prompted.

> 💡 **Tip:** truecolor output needs a terminal that supports 24-bit color (Windows Terminal, VS Code, iTerm2, GNOME Terminal, etc.). On legacy consoles colors may be ignored.

## 🧰 Tech Stack

- **Python**
- `yt-dlp` — YouTube video downloader
- `ffmpeg` — frame extraction
- `Pillow` — image processing
- `multiprocessing` & `threading` — real-time parallel conversion + playback
- `shutil`, `atexit`, `signal` — safe cleanup