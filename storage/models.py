from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Meeting(Base):
    __tablename__ = "meetings"
    
    id = Column(String, primary_key=True, index=True) # UUID
    filename = Column(String)
    title = Column(String, default="Untitled Meeting")
    file_hash = Column(String, nullable=True)
    date = Column(DateTime, default=func.now())
    duration = Column(Float, default=0.0) # seconds
    language = Column(String, default="en")
    speaker_count = Column(Integer, default=0)
    processing_status = Column(String, default="Pending") # Pending, Processing, Completed, Failed
    
    # AI Summary Fields
    executive_summary = Column(String, nullable=True)
    meeting_objective = Column(String, nullable=True)
    meeting_plan = Column(String, nullable=True)
    emotional_analysis = Column(String, nullable=True)
    key_topics = Column(String, nullable=True)
    key_points = Column(String, nullable=True)
    risks = Column(String, nullable=True)
    recommendations = Column(String, nullable=True)
    next_steps = Column(String, nullable=True)
    
    segments = relationship("TranscriptSegment", back_populates="meeting", cascade="all, delete-orphan")
    speakers = relationship("Speaker", back_populates="meeting", cascade="all, delete-orphan")
    action_items = relationship("ActionItem", back_populates="meeting", cascade="all, delete-orphan")
    decisions = relationship("Decision", back_populates="meeting", cascade="all, delete-orphan")
    participants = relationship("Participant", back_populates="meeting", cascade="all, delete-orphan")
    deadlines = relationship("Deadline", back_populates="meeting", cascade="all, delete-orphan")
    priorities = relationship("Priority", back_populates="meeting", cascade="all, delete-orphan")

class Speaker(Base):
    __tablename__ = "speakers"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(String, ForeignKey("meetings.id"))
    original_label = Column(String)
    display_name = Column(String)
    
    meeting = relationship("Meeting", back_populates="speakers")

class TranscriptSegment(Base):
    __tablename__ = "transcript_segments"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(String, ForeignKey("meetings.id"))
    speaker = Column(String)
    start = Column(Float)
    end = Column(Float)
    text = Column(String)
    confidence = Column(Float, default=1.0)
    
    meeting = relationship("Meeting", back_populates="segments")

class ActionItem(Base):
    __tablename__ = "action_items"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(String, ForeignKey("meetings.id"))
    task = Column(String)
    assigned_to = Column(String)
    deadline = Column(String)
    priority = Column(String)
    status = Column(String, default="Pending") # Pending, In Progress, Completed
    
    meeting = relationship("Meeting", back_populates="action_items")

class Decision(Base):
    __tablename__ = "decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(String, ForeignKey("meetings.id"))
    decision = Column(String)
    context = Column(String)
    timestamp_approx = Column(String, nullable=True)
    
    meeting = relationship("Meeting", back_populates="decisions")

class Participant(Base):
    __tablename__ = "participants"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(String, ForeignKey("meetings.id"))
    name = Column(String)
    speaker_id = Column(String)
    responsibilities = Column(String) # JSON list of strings
    
    meeting = relationship("Meeting", back_populates="participants")

class Deadline(Base):
    __tablename__ = "deadlines"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(String, ForeignKey("meetings.id"))
    description = Column(String)
    date = Column(String)
    related_task = Column(String)
    
    meeting = relationship("Meeting", back_populates="deadlines")

class Priority(Base):
    __tablename__ = "priorities"
    
    id = Column(Integer, primary_key=True, index=True)
    meeting_id = Column(String, ForeignKey("meetings.id"))
    item = Column(String)
    priority_level = Column(String)
    
    meeting = relationship("Meeting", back_populates="priorities")
