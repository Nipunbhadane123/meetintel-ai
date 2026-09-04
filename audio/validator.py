import os
import subprocess
from pathlib import Path
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

MAGIC_AVAILABLE = False
try:
    import magic
    MAGIC_AVAILABLE = True
except ImportError as e:
    logger.warning(f"libmagic is not available: {e}")

SUPPORTED_AUDIO = {'.wav', '.mp3', '.m4a', '.flac', '.ogg'}
SUPPORTED_VIDEO = {'.mp4', '.mov', '.mkv', '.avi'}
SUPPORTED_EXTENSIONS = SUPPORTED_AUDIO.union(SUPPORTED_VIDEO)

MAX_FILE_SIZE_MB = 1000 # Configurable limit

def validate_file(file_path: str) -> Tuple[bool, str]:
    """
    Validates a file for transcription.
    Returns: (is_valid, error_message_if_any)
    """
    path = Path(file_path)
    
    # 1. Check existence
    if not path.exists() or not path.is_file():
        return False, "File does not exist or is not readable."
        
    # 2. Check extension
    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        return False, f"Unsupported file format. Please upload {', '.join(SUPPORTED_EXTENSIONS)}."
        
    # 3. Check size
    size_mb = path.stat().st_size / (1024 * 1024)
    if size_mb == 0:
        return False, "File is empty."
    if size_mb > MAX_FILE_SIZE_MB:
        return False, f"File is too large. Maximum allowed size is {MAX_FILE_SIZE_MB}MB."
        
    # 4. Check MIME type (using python-magic if available, else fallback to extension)
    if MAGIC_AVAILABLE:
        try:
            mime = magic.from_file(file_path, mime=True)
            if not mime.startswith('audio/') and not mime.startswith('video/') and mime != 'application/octet-stream':
                return False, f"Invalid file content type detected: {mime}"
        except Exception as e:
            return False, f"Error reading file type: {str(e)}"
    else:
        logger.warning("libmagic not available, skipping strict MIME validation.")
        
    # 5. Check if it's a valid media file using FFmpeg
    try:
        # Check streams using ffprobe
        result = subprocess.run([
            'ffprobe', 
            '-v', 'error', 
            '-show_entries', 'stream=codec_type', 
            '-of', 'default=noprint_wrappers=1:nokey=1', 
            file_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if result.returncode != 0:
            return False, "File is corrupted or not a valid media format."
            
        streams = result.stdout.split('\n')
        if 'audio' not in streams:
            return False, "No audio stream found in the uploaded file."
            
    except FileNotFoundError:
        # FFmpeg not found, skip strict media check
        pass
        
    return True, "Valid"

def get_file_metadata(file_path: str) -> dict:
    """Gets basic metadata about the media file"""
    path = Path(file_path)
    metadata = {
        'filename': path.name,
        'size_mb': round(path.stat().st_size / (1024 * 1024), 2),
        'format': path.suffix.lower().replace('.', '').upper()
    }
    
    # Try to get duration with ffprobe
    try:
        result = subprocess.run([
            'ffprobe', 
            '-v', 'error', 
            '-show_entries', 'format=duration', 
            '-of', 'default=noprint_wrappers=1:nokey=1', 
            file_path
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0 and result.stdout.strip():
            metadata['duration_sec'] = float(result.stdout.strip())
            # Format to MM:SS
            m, s = divmod(int(metadata['duration_sec']), 60)
            h, m = divmod(m, 60)
            if h > 0:
                metadata['duration'] = f"{h:02d}:{m:02d}:{s:02d}"
            else:
                metadata['duration'] = f"{m:02d}:{s:02d}"
    except Exception:
        metadata['duration'] = "Unknown"
        
    return metadata
