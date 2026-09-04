def validate_transcript(segments: list) -> dict:
    """
    Validates the generated transcript.
    Returns a dictionary of status checks.
    """
    results = {
        "is_generated": len(segments) > 0,
        "is_not_empty": False,
        "has_speakers": False,
        "has_valid_timestamps": True,
        "overall_status": "FAILED"
    }
    
    if not results["is_generated"]:
        return results
        
    has_text = any(len(s.get("text", "").strip()) > 0 for s in segments)
    results["is_not_empty"] = has_text
    
    has_speaker_labels = all("speaker" in s and s["speaker"] for s in segments)
    results["has_speakers"] = has_speaker_labels
    
    for s in segments:
        if s.get("start", -1) < 0 or s.get("end", -1) <= s.get("start", -1):
            results["has_valid_timestamps"] = False
            break
            
    if all([
        results["is_generated"],
        results["is_not_empty"],
        results["has_speakers"],
        results["has_valid_timestamps"]
    ]):
        results["overall_status"] = "PASSED"
        
    return results
