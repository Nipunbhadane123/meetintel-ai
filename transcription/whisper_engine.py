import os
import torch
from faster_whisper import WhisperModel
import logging

logger = logging.getLogger(__name__)

# Configurable model size, default to base for performance on CPU
MODEL_SIZE = os.getenv("WHISPER_MODEL", "base")
# Check if CUDA is available, otherwise default to CPU
if torch.cuda.is_available():
    DEVICE = "cuda"
    COMPUTE_TYPE = "float16"
else:
    DEVICE = "cpu"
    COMPUTE_TYPE = "int8"

class WhisperTranscriber:
    def __init__(self):
        self.model = None

    def load_model(self):
        if self.model is None:
            logger.info(f"Loading Whisper model: {MODEL_SIZE} on {DEVICE}...")
            self.model = WhisperModel(MODEL_SIZE, device=DEVICE, compute_type=COMPUTE_TYPE)
            logger.info("Whisper model loaded.")

    def transcribe(self, audio_path: str, language: str = None) -> list:
        """
        Transcribes audio and returns a list of segments.
        Each segment is a dictionary with start, end, text.
        """
        self.load_model()
        logger.info(f"Starting transcription for {audio_path}")
        
        # Generator for transcription
        segments, info = self.model.transcribe(audio_path, language=language, beam_size=5)
        
        logger.info(f"Detected language: {info.language} with probability {info.language_probability}")
        
        transcript_segments = []
        for segment in segments:
            transcript_segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": segment.text.strip(),
                "confidence": getattr(segment, 'avg_logprob', 1.0) # Using logprob as proxy for confidence
            })
            
        return transcript_segments
