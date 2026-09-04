import os
import subprocess
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

def process_audio(input_file: str) -> str:
    """
    Takes an input audio/video file and processes it for Whisper/Pyannote:
    - Extracts audio
    - Converts to WAV
    - Mono
    - 16 kHz sample rate
    - Normalized volume
    Returns the path to the processed WAV file.
    """
    input_path = Path(input_file)
    output_filename = f"{input_path.stem}_processed.wav"
    output_path = PROCESSED_DIR / output_filename
    
    # If it already exists, remove it or return it. Here we remove to ensure fresh processing.
    if output_path.exists():
        output_path.unlink()
        
    logger.info(f"Processing audio from {input_path} to {output_path}")
    
    # FFmpeg command:
    # -i input
    # -vn : no video
    # -acodec pcm_s16le : 16-bit PCM
    # -ar 16000 : 16 kHz
    # -ac 1 : mono
    # -af loudnorm : normalize audio
    try:
        command = [
            'ffmpeg',
            '-i', str(input_path),
            '-vn',
            '-acodec', 'pcm_s16le',
            '-ar', '16000',
            '-ac', '1',
            '-af', 'loudnorm',
            '-y', # Overwrite output
            str(output_path)
        ]
        
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return str(output_path)
        
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg error: {e.stderr}")
        raise RuntimeError(f"Audio processing failed: {e.stderr}")
    except FileNotFoundError:
        raise RuntimeError("FFmpeg is not installed or not in PATH.")

def cleanup_file(file_path: str):
    """Removes a file to free up space."""
    path = Path(file_path)
    if path.exists():
        path.unlink()
