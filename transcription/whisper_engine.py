import os
import logging
from faster_whisper import WhisperModel
import streamlit as st

logger = logging.getLogger(__name__)

MODEL_SIZE = os.getenv("WHISPER_MODEL", "small")

# Determine device and compute type
if os.uname().sysname == "Darwin" and os.uname().machine == "arm64":
    # Apple Silicon (M1/M2/M3)
    DEVICE = "cpu"  
    # int8 compute is significantly faster on Mac CPU
    COMPUTE_TYPE = "int8"
else:
    DEVICE = "cpu"
    COMPUTE_TYPE = "int8"

@st.cache_resource(show_spinner=False)
def get_whisper_model(model_size, device, compute_type):
    logger.info(f"Loading Whisper model (Cached): {model_size} on {device}...")
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    logger.info("Whisper model loaded.")
    return model

class WhisperTranscriber:
    def __init__(self):
        self.model = None

    def load_model(self):
        if self.model is None:
            self.model = get_whisper_model(MODEL_SIZE, DEVICE, COMPUTE_TYPE)

    def transcribe(self, audio_path: str, language: str = None) -> list:
        """
        Transcribes audio and returns a list of segments.
        Each segment is a dictionary with start, end, text.
        """
        self.load_model()
        logger.info(f"Starting transcription for {audio_path}")
        
        import time
        start_time = time.time()
        
        segments, info = self.model.transcribe(
            audio_path, 
            language=language, 
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
            condition_on_previous_text=False,
            initial_prompt="Meeting transcript:"
        )
        
        logger.info(f"Detected language: {info.language} with probability {info.language_probability}")
        
        transcript_segments = []
        for segment in segments:
            text = segment.text.strip()
            if not text:
                continue
                
            transcript_segments.append({
                "start": segment.start,
                "end": segment.end,
                "text": text,
                "confidence": getattr(segment, 'avg_logprob', 1.0)
            })
            
        logger.info(f"Whisper transcription completed in {time.time() - start_time:.2f}s")
        return transcript_segments
