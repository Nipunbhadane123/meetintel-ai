def get_overlap(start1, end1, start2, end2):
    """Calculates the overlap duration between two time segments."""
    overlap_start = max(start1, start2)
    overlap_end = min(end1, end2)
    if overlap_start < overlap_end:
        return overlap_end - overlap_start
    return 0

def align_transcript_with_speakers(whisper_segments: list, diarization_segments: list) -> list:
    """
    Aligns Whisper transcript segments with Pyannote speaker segments.
    Assigns the speaker that overlaps the most with the whisper segment.
    """
    aligned_segments = []
    
    for w_seg in whisper_segments:
        best_speaker = "UNKNOWN"
        max_overlap = 0.0
        
        for d_seg in diarization_segments:
            overlap = get_overlap(w_seg["start"], w_seg["end"], d_seg["start"], d_seg["end"])
            if overlap > max_overlap:
                max_overlap = overlap
                best_speaker = d_seg["speaker"]
                
        # If no overlap found, use the closest speaker (or just stick with UNKNOWN)
        # For simplicity, we just use the best overlap
        
        aligned_segments.append({
            "start": w_seg["start"],
            "end": w_seg["end"],
            "speaker": best_speaker,
            "text": w_seg["text"],
            "confidence": w_seg.get("confidence", 1.0)
        })
        
    return aligned_segments
