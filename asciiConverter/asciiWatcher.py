import glob
import os
import time
from multiprocessing import Pool
from asciiText.ascii import convert_and_save_ascii

DONE_FLAG = "_DONE"


def convert_and_save_ascii_wrapper(frame_path, output_dir, pixel_mode=False):
    convert_and_save_ascii(frame_path, output_folder=output_dir, pixel_mode=pixel_mode)


def watch_and_convert(output_folder="vidFrames", ascii_output="asciiFrames",
                      poll_interval=0.1, pixel_mode=False, ffmpeg_proc=None):
    seen = set()
    done_flag = os.path.join(ascii_output, DONE_FLAG)

    # Reuse one pool for the whole run - spawning per batch is very slow on Windows
    pool = Pool()
    try:
        while True:
            frames = sorted(glob.glob(f"{output_folder}/frame_*.png"))
            new = [f for f in frames if f not in seen]

            if new:
                # Stream: convert whatever just appeared, in order
                args = [(frame, ascii_output, pixel_mode) for frame in new]
                pool.starmap(convert_and_save_ascii_wrapper, args)
                seen.update(new)

            # ffmpeg finished when its process object is gone (None or poll() != None)
            ffmpeg_done = ffmpeg_proc is None or ffmpeg_proc.poll() is not None
            if ffmpeg_done and not new:
                # Give ffmpeg a moment to flush its last frames, then make sure
                # nothing appeared before declaring the conversion complete
                time.sleep(0.5)
                remaining = [f for f in sorted(glob.glob(f"{output_folder}/frame_*.png")) if f not in seen]
                if remaining:
                    args = [(frame, ascii_output, pixel_mode) for frame in remaining]
                    pool.starmap(convert_and_save_ascii_wrapper, args)
                    seen.update(remaining)
                with open(done_flag, "w", encoding="utf-8") as f:
                    f.write("done")
                break

            time.sleep(poll_interval)
    finally:
        pool.close()
        pool.join()