import yt_dlp
import whisper
from pydub import AudioSegment
import tempfile
import os
from pydub.effects import normalize,strip_silence
import warnings


# Suppress FutureWarnings from torch
warnings.filterwarnings("ignore", category=FutureWarning, module="torch")
def transcribe_from_youtube(youtube_url):
    # Configure yt_dlp to download audio
    temp_dir = tempfile.gettempdir()  # Use a temporary directory
    temp_audio_file = os.path.join(temp_dir, "temp_audio")  # No extension

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': temp_audio_file,  # Let yt_dlp handle the extension
    }

    try:
        # Download audio from YouTube
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        # Append .mp3 to match the processed file
        temp_audio_file += ".mp3"

        # Load Whisper model
        model = whisper.load_model("base")

        # Process audio in chunks
        audio = AudioSegment.from_file(temp_audio_file, format="mp3")
        total_duration = len(audio)
        chunk_duration = 60000  # 60 seconds chunks
        overlap = 5000  # 5 seconds overlap
        transcripts = []

        for start in range(0, total_duration, chunk_duration - overlap):
            end = min(start + chunk_duration, total_duration)
            chunk = audio[start:end]
            chunk=normalize(chunk)
            chunk=strip_silence(chunk,silence_len=1000,silence_thresh=-40)

            # Export chunk to WAV
            chunk_path = os.path.join(temp_dir, f"chunk_{start // 1000}.wav")
            chunk.export(chunk_path, format="wav")

            # Load the audio data as a NumPy array
            audio_array = whisper.audio.load_audio(chunk_path)

            # Transcribe chunk using Whisper
            result = model.transcribe(audio_array,language="en",task="translate",temperature=0.0)
            cleaned_text=" ".join(segment["text"] for segment in result["segments"] if not segment.get("no_speech_prob",0)>0.5)
            transcripts.append(cleaned_text)

            # Remove temporary chunk file
            os.remove(chunk_path)

        # Join all transcripts into one
        return " ".join(transcripts)
    except:
        print("Error while searching for the video")
    finally:
        # Ensure the temporary file is deleted after processing
        if os.path.exists(temp_audio_file):
            os.remove(temp_audio_file)

