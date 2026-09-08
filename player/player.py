import os
import time
import glob
import sys

DONE_FLAG = "_DONE"
FRAME_GLOB = "frame_*.txt"

# ANSI sequences - no cmd.exe spawn per frame, so no flicker
HOME = "\x1b[H"          # cursor to top-left
CLEAR_BELOW = "\x1b[0J"  # clear from cursor to end of screen
RESET = "\x1b[0m"
HIDE_CURSOR = "\x1b[?25l"
SHOW_CURSOR = "\x1b[?25h"


def play_ascii_frames(folder='asciiFrames', fps=15):
    seen = set()
    delay = 1.0 / fps
    done_flag = os.path.join(folder, DONE_FLAG)

    sys.stdout.write(HIDE_CURSOR + "[PLAY] Starting playback...\n")
    sys.stdout.flush()

    try:
        while True:
            frames = sorted(glob.glob(os.path.join(folder, FRAME_GLOB)))
            new_frames = [f for f in frames if f not in seen]

            if not new_frames:
                if os.path.exists(done_flag):
                    sys.stdout.write(RESET + CLEAR_BELOW + SHOW_CURSOR + "[DONE] Playback complete.\n")
                    sys.stdout.flush()
                    break
                time.sleep(0.02)
                continue

            for frame_path in new_frames:
                with open(frame_path, "r", encoding="utf-8") as f:
                    content = f.read()
                # Home cursor + overwrite the fixed-size frame in place.
                # Frames are always exactly width cells wide, so no stale
                # characters remain and there is no blank-screen flash.
                sys.stdout.write(HOME + content + RESET + CLEAR_BELOW)
                sys.stdout.flush()
                seen.add(frame_path)
                time.sleep(delay)
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write(RESET + SHOW_CURSOR)
        sys.stdout.flush()