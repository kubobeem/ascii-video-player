import os
import time
import glob

def play_ascii_frames(folder='asciiFrames', fps=15):
    seen = set()
    delay = 1.0 / fps

    print("[PLAY] Starting playback...")

    while True:
        frames = sorted(glob.glob(f"{folder}/frame_*.txt"))

        # Get only the new frames
        new_frames = [f for f in frames if f not in seen]

        if not new_frames:
            if _is_ascii_conversion_done(folder):
                print("[DONE] Playback complete.")
                break
            time.sleep(0.1)
            continue

        for frame_path in new_frames:
            os.system("cls" if os.name == "nt" else "clear")
            with open(frame_path, "r", encoding="utf-8") as f:
                print(f.read())
            seen.add(frame_path)
            time.sleep(delay)

def _is_ascii_conversion_done(folder):
    current_frames = len(glob.glob(f"{folder}/frame_*.txt"))
    time.sleep(0.5)
    later_frames = len(glob.glob(f"{folder}/frame_*.txt"))
    return current_frames == later_frames and current_frames > 0
