import re

FILLER_WORDS = [
    r'\buh\b', r'\bum\b', r'\ber\b', r'\bah\b', r'\bhm+\b',
    r'\buh-huh\b', r'\bmm-hmm\b', r'\blike\b', r'\byou know\b'
]

FILLER_REGEX = re.compile(r'(?i)(' + '|'.join(FILLER_WORDS) + r')[,.\s]*')

def apply_clean_verbatim(text: str) -> str:
    """
    Removes common filler words and hesitation markers.
    """
    cleaned = re.sub(FILLER_REGEX, ' ', text)
    # Remove excessive spaces and fix punctuation
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = re.sub(r'\s([?.!,"](?:\s|$))', r'\1', cleaned) # fix spaces before punctuation
    return cleaned.strip()

def format_transcript(segments: list, mode: str = "Full Verbatim", speaker_map: dict = None) -> list:
    """
    Formats the transcript segments according to the chosen mode (Clean or Full).
    Applies speaker renaming if speaker_map is provided.
    """
    formatted_segments = []
    
    for seg in segments:
        text = seg["text"]
        if mode == "Clean Verbatim":
            text = apply_clean_verbatim(text)
            
        speaker = seg["speaker"]
        if speaker_map and speaker in speaker_map:
            speaker = speaker_map[speaker]
            
        formatted_segments.append({
            "start": seg["start"],
            "end": seg["end"],
            "speaker": speaker,
            "text": text,
            "confidence": seg.get("confidence", 1.0)
        })
        
    return formatted_segments

def generate_text_transcript(formatted_segments: list) -> str:
    """Generates a plain text transcript format."""
    lines = []
    for seg in formatted_segments:
        # Convert seconds to MM:SS
        m, s = divmod(int(seg["start"]), 60)
        h, m = divmod(m, 60)
        if h > 0:
            timestamp = f"[{h:02d}:{m:02d}:{s:02d}]"
        else:
            timestamp = f"[{m:02d}:{s:02d}]"
            
        lines.append(f"{timestamp} {seg['speaker']}:\n{seg['text']}\n")
        
    return "\n".join(lines)
