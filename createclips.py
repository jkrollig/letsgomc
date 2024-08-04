import os
import subprocess
import ffmpeg

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
        base_name = f'clip_{i+1:03d}'
        output_file = os.path.join(output_folder, f'{base_name}.mp4')
        counter = i

        # Ensure unique file names
        while os.path.exists(output_file):
            output_file = os.path.join(output_folder, f'clip_{counter:03d}.mp4')
            counter += 1
        
        """ cmd = f'ffmpeg -i "{input_file}" -ss {start_time} -t {clip_duration} -an -c:v libx264 -preset medium "{output_file}"'
        subprocess.call(cmd, shell=True) """
        (
    (
    ffmpeg
    .input(input_file, ss=start_time, t=clip_duration)
    .output(output_file, 
            vcodec='h264_nvenc',
            cq=18,
            preset='slow',
            rc='vbr',
            b='5M',
            maxrate='10M',
            an=None)
    .run(overwrite_output=True)
)
)
        print(f""" 






                    OUTPUT FILE HAS BEEN GENERATED{output_file} 






""")

    print(f"Created {num_clips} clips in {output_folder}")

# Usage
input_file = 'input.mp4'
output_folder = 'clips'
create_clips(input_file, output_folder)
