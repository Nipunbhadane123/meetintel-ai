import os
import torch
import logging
from pyannote.audio import Pipeline

logger = logging.getLogger(__name__)

class SpeakerDiarizer:
    def __init__(self):
        self.pipeline = None

    def load_pipeline(self):
        if self.pipeline is None:
            token = os.getenv("HUGGINGFACE_TOKEN")
            if not token:
                raise ValueError("HUGGINGFACE_TOKEN environment variable not set. Required for diarization.")
            
            logger.info("Loading Pyannote diarization pipeline...")
            try:
                self.pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-community-1",
                    token=token
                )
            except TypeError:
                self.pipeline = Pipeline.from_pretrained(
                    "pyannote/speaker-diarization-community-1",
                    use_auth_token=token
                )
            
            # Use CUDA if available, otherwise CPU (MPS can cause hangs in pyannote)
            if torch.cuda.is_available():
                self.pipeline.to(torch.device("cuda"))
            else:
                self.pipeline.to(torch.device("cpu"))
                
            logger.info("Diarization pipeline loaded.")

    def diarize(self, audio_path: str) -> list:
        """
        Diarizes the audio and returns a list of speaker segments.
        Returns: [{"start": float, "end": float, "speaker": str}, ...]
        """
        self.load_pipeline()
        logger.info(f"Starting diarization for {audio_path}")
        
        import scipy.io.wavfile as wavfile
        import numpy as np
        import torch
        
        try:
            # Completely bypass torchaudio and torchcodec by manually loading the WAV file.
            sample_rate, data = wavfile.read(audio_path)
            
            # Reshape to (channels, samples)
            if data.ndim == 1:
                data = data.reshape(1, -1)
            else:
                data = data.T
                
            # Normalize to float32 [-1, 1] as expected by Pyannote
            if data.dtype == np.int16:
                data = data.astype(np.float32) / 32768.0
            elif data.dtype == np.int32:
                data = data.astype(np.float32) / 2147483648.0
            else:
                data = data.astype(np.float32)
                
            waveform = torch.from_numpy(data)
            
            # Pass dictionary directly to pyannote pipeline
            diarization = self.pipeline({"waveform": waveform, "sample_rate": sample_rate})
        except Exception as e:
            logger.warning(f"scipy wavfile backend failed: {e}. Falling back to default loader.")
            diarization = self.pipeline(audio_path)
        
        segments = []
        
        # In Pyannote 3.1+, the pipeline might return a DiarizeOutput object
        # which wraps the actual Annotation in a .speaker_diarization attribute
        if hasattr(diarization, "speaker_diarization"):
            annotation = diarization.speaker_diarization
        else:
            annotation = diarization
            
        for turn, _, speaker in annotation.itertracks(yield_label=True):
            segments.append({
                "start": turn.start,
                "end": turn.end,
                "speaker": speaker
            })
            
        return segments
