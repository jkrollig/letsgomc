import ffmpeg

def convert_webm_to_mp4(input_path, output_path):
    (
        ffmpeg
        .input(input_path)
        .output(output_path, vcodec='h264_nvenc', preset='slow', crf=18, acodec='aac', strict='experimental')
        .run(overwrite_output=True)
    )

# Example usage:
convert_webm_to_mp4('input.webm', 'input.mp4')
