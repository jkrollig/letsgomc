import os
from google.cloud import texttospeech
import ffmpeg
import subprocess
from random import choice


def synthesize_speech(text, number, day_number):
    
    client = texttospeech.TextToSpeechClient()

    input_text = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Journey-D",  # Use the appropriate voice name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16,
        speaking_rate=1
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    
    os.makedirs(f"mp3raw/{day_number}", exist_ok=True)
    os.makedirs(f"mp3/{day_number}", exist_ok=True)

    output_base_filename = f"mp3raw/{day_number}/output_{number:03}.mp3"
    with open(output_base_filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_base_filename}"')
    speed=1.25
    adjusted_filename = f"mp3/{day_number}/output_{number:03}.mp3"
    # adjust_playback_speed(output_base_filename, adjusted_filename, speed=speed)
    subprocess.run([
    'ffmpeg',
    '-y',
    '-i', output_base_filename,
    '-filter:a', f'atempo={speed}',
    '-codec:a', 'libmp3lame',  # You can specify other codecs like 'aac' if needed
    '-q:a', '0',               # Set the audio quality (0 is the best quality)
    adjusted_filename
], check=True)

    return adjusted_filename    


def get_duration(file_path):
    """Get the duration of the media file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist.")
    
    try:
        probe = ffmpeg.probe(file_path, v='error', show_entries='format=duration', format='json')
        duration = float(probe['format']['duration'])
        return duration
    except (KeyError, IndexError, ValueError) as e:
        raise RuntimeError(f"Error retrieving duration for {file_path}: {e}")

def trim_media(input_file, duration, output_file):
    """Trim video file to the specified duration with optimized speed, no audio processing."""
    ffmpeg.input(input_file, t=duration).output(            
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


def combine_audio_video(number, day_number):
    clip_files = [f for f in os.listdir("/content/drive/My Drive/clippeds/") if f.endswith(".mp4")]

    # Choose a random clip file
    random_clip = choice(clip_files)

    # Create the full path to the randomly selected clip
    # input_video = os.path.join("/content/drive/My Drive/clippeds/", random_clip)
    
    os.makedirs(f"mp3/{day_number}", exist_ok=True)
    input_video = os.path.join("/content/drive/My Drive/clippeds/", random_clip)
    input_audio = f"mp3/{day_number}/output_{number:03}.mp3"

    # input_video = f"clippeds/clip_{number:03}.mp4"
    # output_file = f"combined_{number:03}.mp4"
    
    try:
        # Get the durations of audio and video
        audio_duration = get_duration(input_audio)
        video_duration = get_duration(input_video)
        
        # Determine the shortest duration
        shortest_duration = min(audio_duration, video_duration)
        if shortest_duration < 30:
            return False
        # Trim the longer input to the shortest duration
        os.makedirs(f"trimmed/{day_number}", exist_ok=True)
        trimmed_audio_file = f"trimmed/{day_number}/trimmed_audio_{number:03}.mp3"
        trimmed_video_file = f"trimmed/{day_number}/trimmed_video_{number:03}.mp4"
        
        if audio_duration > shortest_duration:
            return False
            trim_media(input_audio, shortest_duration, trimmed_audio_file)
            input_audio = trimmed_audio_file
        
        if video_duration > shortest_duration:
            trim_media(input_video, shortest_duration, trimmed_video_file)
            input_video = trimmed_video_file
        
                # Combine the audio and video files
        

        audio = ffmpeg.input(input_audio)
        video = ffmpeg.input(input_video)
        os.makedirs(f"withaudio/{day_number}", exist_ok=True)
        (
        ffmpeg
        .output(video, audio, f'withaudio/{day_number}/xd_{number:03}.mp4',
                vcodec='h264_nvenc',   # Use NVIDIA GPU acceleration for H.264 encoding
                video_bitrate='8M',    # Target video bitrate (adjust as needed)
                acodec='aac',          # AAC audio codec
                audio_bitrate='256k',  # High audio bitrate for better quality
                preset='slow',         # Slow preset for better quality compression
                maxrate='12M',         # Maximum video bitrate
                minrate='4M',          # Minimum video bitrate to maintain quality
                bufsize='16M',         # Buffer size for bitrate control
                cq=18,                 # Constant Quality mode (lower value for higher quality)
                loglevel='error'       # Reduce verbosity of logs
               )
        .global_args('-hide_banner')  # Hide banner information
        .run(overwrite_output=True)
    )
        
        
    
    except Exception as e:
        print(f"Error combining audio and video: {e}")
    return True



text = ("""Only 1 percent of people know the secret to making the fluffiest, most tender croissants in the world, are you one of them? Do you know what makes a croissant truly exceptional? It's not the type of flour used, nor the temperature of the oven, but rather the way the dough is laminated. 

Lamination is the process of folding and rolling the dough multiple times to create the signature layers of butter and dough in a croissant. But what's fascinating is that the optimal number of laminations is 27. Yes, you heard that right, 27! This specific number of folds creates the perfect balance of flaky, crispy, and soft layers, making the croissant truly divine. 

So, the next time you're attempting to make croissants at home, remember the magic number 27. But, what happens if you laminate the dough 28 times? Does it make a difference? Comment down below with your thoughts!""")


number = 1



# combine_audio_video(number)

def generate_video_from_answer(text, number, day_number):
    print("Text-to-Speech begins")
    synthesize_speech(text,number, day_number)
    print("Text-to-Speech ends")
    return combine_audio_video(number, day_number)
    #return false if 1.25x audio is longer than 1min
        

""" from sbtnew import executor

executor(number) """

# generate_video_from_answer(text, 1)


