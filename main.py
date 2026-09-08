from downloader.downloader import download_video
from frames.extracter import extract_frames_live
from asciiConverter.asciiWatcher import watch_and_convert
from player.player import play_ascii_frames
from threading import Thread
import argparse
import atexit
import signal
import sys
from utils.cleanup import cleanup

def main():
    # Windows consoles default to cp932; force UTF-8 so ANSI colors and
    # the full-block char in pixel mode are printed correctly
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Colorful ASCII video player (fork of AddisionS/ascii-video-player)")
    parser.add_argument("--pixel", action="store_true", help="pixel mode: fill with solid color blocks instead of characters")
    args = parser.parse_args()

    url = input("Enter YouTube URL: ").strip()

    print("Downloading video...")
    download_video(url)

    print("Starting frame extraction...")
    ffmpeg_proc = extract_frames_live()

    print("Launching ASCII converter thread...")
    converter_thread = Thread(target=watch_and_convert, kwargs={"pixel_mode": args.pixel, "ffmpeg_proc": ffmpeg_proc})
    converter_thread.start()

    print("Launching ASCII playback thread...")
    player_thread = Thread(target=play_ascii_frames)
    player_thread.start()

    ffmpeg_proc.wait()
    converter_thread.join()
    player_thread.join()

    print("Done.")
    cleanup()

if __name__ == "__main__":
    def handle_exit(*args):
        cleanup()
        exit(0)

    atexit.register(cleanup)
    signal.signal(signal.SIGINT, handle_exit)

    main()
