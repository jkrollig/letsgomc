import yt_dlp
import sys


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now converting ...')

ydl_opts = {
    'format': 'bestvideo[ext=mp4][height<=1440]',
    'outtmpl': 'input.%(ext)s',
    
    'noplaylist': True,
    'progress_hooks': [my_hook],
    'verbose': True
}

video_url = "https://www.youtube.com/watch?v=FGYogb7khaQ"  # Replace with your video URL

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr)
    if hasattr(e, 'exc_info'):
        print(f"Exception info: {e.exc_info()[1]}", file=sys.stderr)
    print(f"Error type: {type(e).__name__}", file=sys.stderr)


""" 
import os
import subprocess

def create_clips(input_file, output_folder, clip_duration=60):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get video duration
    duration_cmd = f'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{input_file}"'
    duration = float(subprocess.check_output(duration_cmd, shell=True).decode('utf-8').strip())

    # Calculate number of clips
    num_clips = int(duration // clip_duration) + (1 if duration % clip_duration > 0 else 0)

    for i in range(num_clips):
        start_time = i * clip_duration
        output_file = os.path.join(output_folder, f'clip_{i+1:03d}.mp4')
        
        cmd = f'ffmpeg -i "{input_file}" -ss {start_time} -t {clip_duration} -an -c:v libx264 -crf 23 -preset medium "{output_file}"'
        subprocess.call(cmd, shell=True)

    print(f"Created {num_clips} clips in {output_folder}")

# Usage
input_file = '2hmc.mp4'
output_folder = 'clips'
create_clips(input_file, output_folder)


import ffmpeg

# Define input and output directories
input_dir = 'clips'
output_dir = 'clippeds'

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Loop through all files in the input directory
for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Add other video formats if needed
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, filename)
        
        # Apply ffmpeg command
        ffmpeg.input(input_file).output(
            output_file,
            vf='crop=ih*(9/16):ih',
            vcodec='h264_nvenc'  # Optional: use GPU acceleration with NVIDIA encoder
        ).run(overwrite_output=True)

        print(f'Processed {input_file} -> {output_file}') """