import os
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
        try:
            ffmpeg.input(input_file).output(
            
            output_file,
            cq=18,
            preset='slow',
            rc='vbr',
            b='5M',
            maxrate='10M',
            an=None,
            vf='crop=ih*(9/16):ih',
            vcodec='h264_nvenc'  # Optional: use GPU acceleration with NVIDIA encoder
        ).run(overwrite_output=True)
        except:
            pass
        print(f'Processed {input_file} -> {output_file}')
