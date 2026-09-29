import os
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any
import hashlib

# Default to a fast, local model
DEFAULT_MODEL = "all-MiniLM-L6-v2"

class EmbeddingService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
        
    def _initialize(self):
        self.model_name = os.getenv("EMBEDDING_MODEL", DEFAULT_MODEL)
        self.model = SentenceTransformer(self.model_name)
        
    def generate_embedding(self, text: str) -> List[float]:
        if not text or not text.strip():
            return []
        # Return as list of floats
        return self.model.encode(text).tolist()
        
    def generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

def generate_content_hash(text: str) -> str:
    """Generate a deterministic hash for content to prevent duplicate embeddings."""
    return hashlib.md5(text.encode("utf-8")).hexdigest()

def chunk_transcript(segments: List[Dict[str, Any]], max_chars: int = 1000, overlap: int = 200) -> List[Dict[str, Any]]:
    """
    Chunks transcript segments.
    Input segments: [{"start": 0.0, "end": 2.5, "speaker": "SPEAKER_00", "text": "Hello"}]
    Output chunks: [{"text": "chunk text", "start": 0.0, "end": 10.5, "speakers": ["SPEAKER_00"], "chunk_id": "...", "content_hash": "..."}]
    """
    if not segments:
        return []
        
    chunks = []
    current_chunk_text = ""
    current_start = segments[0].get("start", 0.0)
    current_end = segments[0].get("end", 0.0)
    current_speakers = set()
    
    for seg in segments:
        text = seg.get("text", "").strip()
        if not text:
            continue
            
        if len(current_chunk_text) + len(text) > max_chars and current_chunk_text:
            # Save current chunk
            chunk_text = current_chunk_text.strip()
            chunks.append({
                "text": chunk_text,
                "start": current_start,
                "end": current_end,
                "speakers": list(current_speakers),
                "content_hash": generate_content_hash(chunk_text)
            })
            # Start new chunk
            current_chunk_text = text + " "
            current_start = seg.get("start", 0.0)
            current_end = seg.get("end", 0.0)
            current_speakers = {seg.get("speaker", "UNKNOWN")}
        else:
            current_chunk_text += text + " "
            current_end = seg.get("end", current_end)
            speaker = seg.get("speaker")
            if speaker:
                current_speakers.add(speaker)
            
    if current_chunk_text:
        chunk_text = current_chunk_text.strip()
        chunks.append({
            "text": chunk_text,
            "start": current_start,
            "end": current_end,
            "speakers": list(current_speakers),
            "content_hash": generate_content_hash(chunk_text)
        })
        
    return chunks

def chunk_text(text: str, max_chars: int = 1000) -> List[Dict[str, str]]:
    """Simple text chunker for summaries, decisions, etc."""
    if not text:
        return []
        
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        if current_length + len(word) > max_chars and current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "text": chunk_text,
                "content_hash": generate_content_hash(chunk_text)
            })
            current_chunk = [word]
            current_length = len(word) + 1
        else:
            current_chunk.append(word)
            current_length += len(word) + 1
            
    if current_chunk:
        chunk_text = " ".join(current_chunk)
        chunks.append({
            "text": chunk_text,
            "content_hash": generate_content_hash(chunk_text)
        })
        
    return chunks
