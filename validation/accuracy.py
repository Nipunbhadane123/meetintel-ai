import jiwer

def calculate_accuracy(reference: str, hypothesis: str) -> dict:
    """
    Calculates Word Error Rate (WER) and Accuracy.
    Accuracy = (1 - WER) * 100
    Returns a dict with WER, Accuracy, Substitutions, Deletions, Insertions.
    """
    # Clean texts
    ref = jiwer.RemovePunctuation()(reference.lower().strip())
    hyp = jiwer.RemovePunctuation()(hypothesis.lower().strip())
    
    # Remove multiple spaces
    ref = jiwer.RemoveMultipleSpaces()(ref)
    hyp = jiwer.RemoveMultipleSpaces()(hyp)
    
    if not ref:
        return {"error": "Reference text is empty."}
        
    out = jiwer.process_words(ref, hyp)
    
    wer = out.wer
    accuracy = max(0.0, (1 - wer) * 100)
    
    return {
        "wer": round(wer, 4),
        "accuracy": round(accuracy, 2),
        "substitutions": out.substitutions,
        "deletions": out.deletions,
        "insertions": out.insertions,
        "status": "PASSED" if accuracy >= 90 else "FAILED"
    }
