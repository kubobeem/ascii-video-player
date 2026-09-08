import subprocess


def extract_frames_live(video_path='downloads/video.mp4', output_folder='vidFrames', width=80, height=40, fps=15):
    import os
    os.makedirs(output_folder, exist_ok=True)

    cmd = [
        'ffmpeg',
        '-i', video_path,
        '-vf', f'scale={width}:{height}',
        '-r', str(fps),
        f'{output_folder}/frame_%04d.png'
    ]

    process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return process
