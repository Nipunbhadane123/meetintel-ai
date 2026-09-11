from transcription.whisper_engine import WhisperTranscriber

def test_transcription():
    t = WhisperTranscriber()
    segments = t.transcribe("test_meeting.wav")
    text = " ".join([s["text"] for s in segments])
    print(f"TRANSCRIPT: {text}")

if __name__ == "__main__":
    test_transcription()
