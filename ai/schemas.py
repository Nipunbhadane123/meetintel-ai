from pydantic import BaseModel, Field
from typing import List, Optional

class ActionItemSchema(BaseModel):
    task: str
    assigned_to: str = Field(default="Unassigned")
    deadline: Optional[str] = None
    priority: str = Field(default="Medium")
    status: str = Field(default="Pending")

class ParticipantSchema(BaseModel):
    name: str = Field(default="Unknown Participant")
    speaker_id: str = Field(default="Unknown")
    responsibilities: List[str] = Field(default_factory=list)

class DeadlineSchema(BaseModel):
    description: str
    date: str
    related_task: str

class PrioritySchema(BaseModel):
    item: str
    priority: str

class DecisionSchema(BaseModel):
    decision: str
    context: str
    timestamp_approx: Optional[str] = None

class RiskSchema(BaseModel):
    risk: str
    impact: str
    context: str
    mitigation: Optional[str] = None

class MeetingInsightsSchema(BaseModel):
    summary: str
    key_points: List[str]
    decisions: List[DecisionSchema]
    action_items: List[ActionItemSchema]
    participants: List[ParticipantSchema]
    deadlines: List[DeadlineSchema]
    priorities: List[PrioritySchema]
    
    # Old fields for backward compat or if needed
    executive_summary: Optional[str] = None
    meeting_objective: Optional[str] = None
    meeting_type: Optional[str] = None
    emotional_analysis: Optional[str] = Field(default="Neutral")
    key_topics: Optional[List[str]] = Field(default_factory=list)
    risks: Optional[List[RiskSchema]] = Field(default_factory=list)
    recommendations: Optional[List[str]] = Field(default_factory=list)
    next_steps: Optional[List[str]] = Field(default_factory=list)
    meeting_plan: Optional[str] = None
