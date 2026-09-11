import os
import time
from storage.database import get_db, Base, engine
from storage.repository import create_meeting
from audio.processor import process_audio
from transcription.whisper_engine import WhisperTranscriber
from transcription.diarization import SpeakerDiarizer
from transcription.alignment import align_transcript_with_speakers
from transcription.formatter import format_transcript, generate_text_transcript
from ai.meeting_analyzer import MeetingAnalyzer

Base.metadata.create_all(bind=engine)
db = next(get_db())

print("Testing full pipeline on test_meeting.wav")
meeting = create_meeting(db, "test_meeting.wav", 13.0, file_hash="test_hash")
t0 = time.time()
print("Processing audio...")
processed_wav = process_audio("test_meeting.wav")

print("Transcribing...")
t_w = time.time()
transcriber = WhisperTranscriber()
whisper_segments = transcriber.transcribe(processed_wav)
print(f"Whisper: {time.time() - t_w:.2f}s")

print("Diarizing...")
t_d = time.time()
diarizer = SpeakerDiarizer()
speaker_segments = diarizer.diarize(processed_wav)
print(f"Diarization: {time.time() - t_d:.2f}s")

print("Aligning...")
aligned = align_transcript_with_speakers(whisper_segments, speaker_segments)
clean_segments = format_transcript(aligned, mode="Clean Verbatim")
text_transcript = generate_text_transcript(clean_segments)

print("Analyzing...")
t_a = time.time()
analyzer = MeetingAnalyzer()
insights = analyzer.analyze(text_transcript)
print(f"Analysis: {time.time() - t_a:.2f}s")
print(f"Total time: {time.time() - t0:.2f}s")
