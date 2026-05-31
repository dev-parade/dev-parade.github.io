import os
import json
import argparse
import yt_dlp
import whisper
from moviepy.editor import ImageClip, AudioFileClip, TextClip, CompositeVideoClip

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'data', 'lyrics_database.json')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

def get_lyrics(song_id):
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}. Run extract_lyrics.py first.")
    
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        db = json.load(f)
        
    for song in db:
        if song['id'] == song_id:
            return song['lyrics'], song.get('audio_url', '')
            
    raise ValueError(f"Song ID '{song_id}' not found in database.")

def download_audio(url, output_path):
    print(f"Downloading audio from {url}...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path.replace('.mp3', ''),  # yt-dlp adds the extension
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print(f"✅ Audio downloaded to {output_path}")

def generate_video(song_id, audio_path, image_path, output_name="output.mp4"):
    # 1. Load lyrics and auto-download audio if needed
    print(f"Loading lyrics for {song_id}...")
    lyrics, audio_url = get_lyrics(song_id)
    
    if not audio_path:
        audio_path = os.path.join(BASE_DIR, 'assets', f"{song_id}.mp3")
        
    if not os.path.exists(audio_path):
        if audio_url:
            print(f"Audio file not found locally. Auto-downloading from {audio_url}")
            os.makedirs(os.path.dirname(audio_path), exist_ok=True)
            download_audio(audio_url, audio_path)
        else:
            raise FileNotFoundError(f"Audio file not found at {audio_path} and no URL in DB.")
    
    # 2. Analyze audio with Whisper
    print(f"Loading Whisper model (this may take a while)...")
    # Using 'base' model for speed; use 'small' or 'medium' for better accuracy
    model = whisper.load_model("base") 
    
    print(f"Analyzing audio: {audio_path}")
    # Using the original lyrics as the initial prompt to guide Whisper's transcription
    result = model.transcribe(
        audio_path,
        word_timestamps=True,
        initial_prompt=lyrics,
        language="ja"
    )
    
    # 3. Setup MoviePy Video
    print("Setting up video project...")
    audio = AudioFileClip(audio_path)
    
    # TikTok/Shorts resolution (9:16)
    W, H = 1080, 1920
    
    # Setup background
    bg_clip = ImageClip(image_path)
    
    # Resize and crop to fill 1080x1920
    bg_clip = bg_clip.resize(height=H)
    if bg_clip.w < W:
        bg_clip = bg_clip.resize(width=W)
    bg_clip = bg_clip.crop(x_center=bg_clip.w/2, y_center=bg_clip.h/2, width=W, height=H)
    bg_clip = bg_clip.set_duration(audio.duration)
    
    # 4. Generate TextClips based on Whisper word timestamps
    print("Generating lyrics animations...")
    text_clips = []
    
    # Iterate through segments and words
    for segment in result["segments"]:
        # We can do word-level or segment-level. For simplicity and readability,
        # we will display the whole segment text, but time it.
        # Whisper segments usually correspond to a phrase.
        
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text'].strip()
        
        if not text:
            continue
            
        # Create TextClip
        # Note: You may need to specify a font that supports Japanese, e.g., font='Noto-Sans-CJK-JP'
        # To avoid font issues dynamically, we use a fallback or system font.
        try:
            txt_clip = TextClip(
                text,
                fontsize=70,
                color='white',
                font='Arial-Unicode-MS', # Mac default font with CJK support
                stroke_color='black',
                stroke_width=3,
                method='caption',
                size=(W - 100, None) # Padding
            )
            
            # Position at center, show only during the segment
            txt_clip = txt_clip.set_position('center').set_start(start_time).set_end(end_time)
            
            # Add subtle animation (e.g. pop in) if desired
            # txt_clip = txt_clip.crossfadein(0.1)
            
            text_clips.append(txt_clip)
        except Exception as e:
            print(f"Warning: Failed to render text '{text}'. (Font issue?) Error: {e}")
            
    # 5. Composite and Export
    print("Compositing video...")
    final_video = CompositeVideoClip([bg_clip] + text_clips)
    final_video = final_video.set_audio(audio)
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(OUTPUT_DIR, output_name)
    
    print(f"Exporting video to {out_path}...")
    final_video.write_videofile(
        out_path,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        threads=4
    )
    print("✅ Video generation complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate MV/TikTok short with automated lyrics")
    parser.add_argument("--song-id", required=True, help="ID of the song (e.g. '03_パルフェ')")
    parser.add_argument("--audio", help="Path to the audio file (optional, will auto-download if empty)")
    parser.add_argument("--image", required=True, help="Path to the background image (jpg/png)")
    parser.add_argument("--output", default="output.mp4", help="Output filename")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.image):
        print(f"Error: Image file not found at {args.image}")
        exit(1)
        
    generate_video(args.song_id, args.audio, args.image, args.output)
