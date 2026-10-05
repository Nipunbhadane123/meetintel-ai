from sqlalchemy.orm import Session
from . import models
import uuid

def create_user(db: Session, username: str, email: str, hashed_password: str) -> models.User:
    user = models.User(
        id=str(uuid.uuid4()),
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_meeting(db: Session, filename: str, user_id: str, duration: float = 0.0, file_hash: str = None) -> models.Meeting:
    meeting = models.Meeting(
        id=str(uuid.uuid4()),
        user_id=user_id,
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

def get_meeting_by_hash(db: Session, file_hash: str, user_id: str):
    if not file_hash:
        return None
    return db.query(models.Meeting).filter(models.Meeting.file_hash == file_hash, models.Meeting.user_id == user_id).first()

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

def get_meeting(db: Session, meeting_id: str, user_id: str = None):
    query = db.query(models.Meeting).filter(models.Meeting.id == meeting_id)
    if user_id:
        query = query.filter(models.Meeting.user_id == user_id)
    return query.first()

def get_all_meetings(db: Session, user_id: str = None):
    query = db.query(models.Meeting)
    if user_id:
        query = query.filter(models.Meeting.user_id == user_id)
    return query.order_by(models.Meeting.date.desc()).all()
