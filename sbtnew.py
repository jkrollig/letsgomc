import json
from pathlib import Path
import ffmpeg
import os
import whisper

model = whisper.load_model("small.en")
print("MODEL LOADED")
def transcribe_with_word_timestamps(audio_file, transcript):
    # Load the Whisper model
    
    # Convert MP4 to audio
    """ audio_file = 'temp_audio.wav'
    ffmpeg.input(input_file).output(audio_file).run(overwrite_output=True)
    print("FFMPEG PRINT FINISH") """
    # Transcribe audio
    result = model.transcribe(audio_file, prompt=transcript,word_timestamps=True)
    print("TRANSCRIBE FINISH")
    # Save result to JSON file
    return result
    with open(output_json, 'w') as f:
        json.dump(result, f, indent=4)

    print(f'Transcription saved to {output_json}')
    return 


def create_animated_subtitles(input_video, output_video, keyword_images, subtitle_data, day_number):
    # Read JSON file
    """ with open(json_file, 'r') as f:
        subtitle_data = json.load(f) """

    # Extract word-level timing information
    words = []
    for segment in subtitle_data['segments']:
        for word in segment['words']:
            words.append({
                'word': word['word'].strip(),
                'start': word['start'],
                'end': word['end']
            })

    # Create subtitle file
    subtitle_file = 'temp_subtitles.ass'
    with open(subtitle_file, 'w') as f:
        f.write('[Script Info]\n')
        f.write('ScriptType: v4.00+\n')
        f.write('PlayResX: 384\n')
        f.write('PlayResY: 512\n')
        f.write('WrapStyle: 0\n')
        f.write('\n')
        f.write('[V4+ Styles]\n')
        f.write('Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n')
        f.write('Style: Default,Impact,20,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,2,2,2,10,10,10,1\n')
        f.write('\n')
        f.write('[Events]\n')
        f.write('Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n')

        for i, word in enumerate(words):
            if word['word'].lower() in keyword_images:
                continue
            
            # Add 0.1 second delay to the start time
            delayed_start = word['start'] # + 0.01
            
            start = f"{int(delayed_start // 3600):02d}:{int(delayed_start % 3600 // 60):02d}:{delayed_start % 60:05.2f}"
            end = f"{int(word['end'] // 3600):02d}:{int(word['end'] % 3600 // 60):02d}:{word['end'] % 60:05.2f}"
            
            # Adjust animation duration to account for the delay
            animation_duration = min(0.5, (word['end'] - delayed_start) / 2) - 0.1
            
            f.write(f"Dialogue: 0,{start},{end},Default,,0,0,0,,{{\\fad({int(animation_duration*1000)},0)\\t(0,{int(animation_duration*1000)},\\fscx120\\fscy120)\\t({int(animation_duration*1000)},{int(animation_duration*2000)},\\fscx100\\fscy100)}}{word['word']}\n")

    # Process video with FFmpeg
    input_video_ffmpeg = ffmpeg.input(input_video)
    
    # Check if the input video has an audio stream
    probe = ffmpeg.probe(input_video)
    audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
    
    # Apply subtitle filter

    topic, day = day_number.split("/")
    if topic == "finance":
        upper_text = "Sharing the Secrets of Money"
    elif topic == "romance":
        upper_text = "Diving Deep into Romance & Relationships"
    elif topic == "science":
        upper_text = "A Science a Day Keeps the Skibidis Away"
    else:
        upper_text = "Daily Facts"

    day_text = f"Day {day}"

    margin_top = 180  # pixels from the top of the video
    text_spacing = 50  # pixels between upper_text and day_text

    video = (
    input_video_ffmpeg.video
    .filter('subtitles', subtitle_file, force_style=f'Fontname=Impact,FontSize=36,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Bold=1,BorderStyle=1,Outline=1,Shadow=0,Alignment=10')
    .drawtext(text=upper_text, fontfile='fonts/bebasneue.ttf', fontsize=60, fontcolor='white', x='(w-text_w)/2', y=f'{margin_top}', shadowcolor='black@0.5', shadowx=2, shadowy=2)
    .drawtext(text=day_text, fontfile='fonts/bebasneue.ttf', fontsize=100, fontcolor='white', x='(w-text_w)/2', y=f'{margin_top}+32+{text_spacing}', shadowcolor='black@0.5', shadowx=2, shadowy=2)
)

    

    # Overlay images for keywords
    for keyword, image_path in keyword_images.items():
        for word in words:
            if word['word'].lower() == keyword.lower():
                video = video.overlay(ffmpeg.input(image_path), x='(main_w-overlay_w)/2', y='(main_h-overlay_h)/2', enable=f'between(t,{word["start"]},{word["end"]})')

    if audio_stream:
        audio = input_video_ffmpeg.audio
        # output = ffmpeg.output(video, audio, output_video, vcodec='h264_nvenc', acodec='aac')
        output = ffmpeg.output(video, audio, output_video,
              vcodec='h264_nvenc',  # H.264 using NVIDIA GPU
              video_bitrate='8M',   # Increased video bitrate
              acodec='aac',
              audio_bitrate='256k', # Higher audio bitrate
              preset='slow',        # Slower preset for better compression
              maxrate='12M',
              bufsize='16M',
              **{'b:v': '8M', 'minrate': '6M', 'rc:v': 'vbr', 'cq': '23',
                 'profile:v': 'high', 'pix_fmt': 'yuv420p',  # 8-bit color
                 'ac': '2', 'ar': '48000'  # Audio channels and sample rate
                }
             )
    else:
        # output = ffmpeg.output(video, output_video, vcodec='h264_nvenc')
        output = ffmpeg.output(video, output_video,
              vcodec='h264_nvenc',  # H.264 using NVIDIA GPU
              video_bitrate='8M', # Increased video bitrate                             
              preset='slow',        # Slower preset for better compression
              maxrate='12M',
              bufsize='16M',
              **{'b:v': '8M', 'minrate': '6M', 'rc:v': 'vbr', 'cq': '23',
                 'profile:v': 'high', 'pix_fmt': 'yuv420p',  # 8-bit color
                
                }
             ).run(overwrite_output=True)
        
    print(ffmpeg.compile(output))  # Print the FFmpeg command
    
    try:
        out, err = ffmpeg.run(output, capture_stdout=True, capture_stderr=True, overwrite_output=True)
    except ffmpeg.Error as e:
        print('stdout:', e.stdout.decode('utf8'))
        print('stderr:', e.stderr.decode('utf8'))
        raise e

    # Clean up temporary subtitle file
    Path(subtitle_file).unlink()



def executor(number, transcript, day_number):
    os.makedirs(f"mp3/{day_number}", exist_ok=True)
   
    input_mp4 = f'./withaudio/{day_number}/xd_{number:03}.mp4'
    # output_json = f'./jasons/transcript_{number:03}.json'
    audio_file = f'./mp3/{day_number}/output_{number:03}.mp3'
    subtitle_data = transcribe_with_word_timestamps(audio_file, transcript)
    # Usage
    
    keyword_to_image = {
        'first': 'img/first.png',
        'know': 'img/know.png',
        'percent': 'img/percent.png',
        '%': 'img/percent.png',
        'people': 'img/people.png',
        'truth': 'img/truth.png',
        'you': 'img/you.png',
        'your': 'img/you.png',
        
    }
    os.makedirs(f"/content/drive/My Drive/final_videos/{day_number}", exist_ok=True)
    output_video = f'/content/drive/My Drive/final_videos/{day_number}/video_{number:03}.mp4'

    create_animated_subtitles(input_mp4, output_video, keyword_to_image, subtitle_data=subtitle_data, day_number=day_number)
    print("Success, final video has been saved at", output_video)


transcript = """Only 1 percent of people know this, are you one of them? Did you know that the secret to wealth accumulation often lies in understanding the "Rule of 72"? This simple formula allows you to estimate how long it will take for your investment to double at a fixed annual rate of return. Just divide 72 by your expected annual return rate. For example, if you expect a 6% return, it would take approximately 12 years for your investment to double (72 divided by 6).

Understanding this rule gives you a powerful tool to visualize your long-term financial growth and make better investment decisions. Many people overlook the impact of compound interest, and this rule simplifies it into something easy to grasp. So, what if you could turn that knowledge into a strategy that accelerates your savings? Imagine what your financial future could look like if you start applying it today!

What's your current annual return on investment, and how long do you think it will take to double it? Comment below!"""
# executor(27, transcript, 1)
