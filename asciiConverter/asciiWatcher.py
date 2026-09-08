import glob
import os
import time
from multiprocessing import Pool
from asciiText.ascii import convert_and_save_ascii

def convert_and_save_ascii_wrapper(frame_path, output_dir, pixel_mode=False):
    convert_and_save_ascii(frame_path, output_folder=output_dir, pixel_mode=pixel_mode)

def watch_and_convert(output_folder="vidFrames", ascii_output="asciiFrames", batch_size=90, poll_interval=1, pixel_mode=False):
    seen = set()

    while True:
        frames = sorted(glob.glob(f"{output_folder}/frame_*.png"))
        new = [f for f in frames if f not in seen]

        if len(new) >= batch_size:
            batch = new[:batch_size]
            args = [(frame, ascii_output, pixel_mode) for frame in batch]

            with Pool() as pool:
                pool.starmap(convert_and_save_ascii_wrapper, args)

            seen.update(batch)

        elif new:
            # ffmpeg is done but frames remain: convert the rest in one go
            args = [(frame, ascii_output, pixel_mode) for frame in new]

            with Pool() as pool:
                pool.starmap(convert_and_save_ascii_wrapper, args)

            seen.update(new)
            break

        elif not is_ffmpeg_running():
            break

        time.sleep(poll_interval)

def is_ffmpeg_running():
    try:
        import psutil
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and 'ffmpeg' in proc.info['name'].lower():
                return True
    except Exception as e:
        print(f"[WARN] Could not check ffmpeg process: {e}")
    return False
