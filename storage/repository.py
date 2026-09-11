from sqlalchemy.orm import Session
from . import models
import uuid

def create_meeting(db: Session, filename: str, duration: float = 0.0, file_hash: str = None) -> models.Meeting:
    meeting = models.Meeting(
        id=str(uuid.uuid4()),
        filename=filename,
        title=f"Meeting - {filename}",
        duration=duration,
        file_hash=file_hash,
        processing_status="Processing"
    )
    db.add(meeting)
    db.commit()
    db.refresh(meeting)
    return meeting

def get_meeting_by_hash(db: Session, file_hash: str):
    if not file_hash:
        return None
    return db.query(models.Meeting).filter(models.Meeting.file_hash == file_hash).first()

def update_meeting_status(db: Session, meeting_id: str, status: str):
    meeting = db.query(models.Meeting).filter(models.Meeting.id == meeting_id).first()
    if meeting:
        meeting.processing_status = status
        db.commit()

def save_transcript(db: Session, meeting_id: str, segments: list):
    # Get unique speakers
    unique_speakers = set()
    db_segments = []
    
    for seg in segments:
        spk = seg.get("speaker", "UNKNOWN")
        unique_speakers.add(spk)
        db_segments.append(
            models.TranscriptSegment(
                meeting_id=meeting_id,
                speaker=spk,
                start=seg["start"],
                end=seg["end"],
                text=seg["text"],
                confidence=seg.get("confidence", 1.0)
            )
        )
        
    for spk in unique_speakers:
        db.add(models.Speaker(meeting_id=meeting_id, original_label=spk, display_name=spk))
        
    db.bulk_save_objects(db_segments)
    
    meeting = db.query(models.Meeting).filter(models.Meeting.id == meeting_id).first()
    if meeting:
        meeting.speaker_count = len(unique_speakers)
        
    db.commit()

def get_meeting(db: Session, meeting_id: str):
    return db.query(models.Meeting).filter(models.Meeting.id == meeting_id).first()

def get_all_meetings(db: Session):
    return db.query(models.Meeting).order_by(models.Meeting.date.desc()).all()
