from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ActionItemSchema(BaseModel):
    task: str
    description: Optional[str] = Field(default=None, description="Detailed actionable explanation of what needs to be delivered.")
    evidence_excerpt: Optional[str] = Field(default=None, description="Verbatim quote or excerpt from the transcript supporting this action.")
    assigned_to: str = Field(default="Unassigned", description="Name of the person explicitly assigned.")
    assignment_status: str = Field(default="Assigned", description="'Assigned' if clearly named, 'Needs assignment' if ambiguous.")
    deadline: Optional[str] = Field(default=None, description="Confirmed deadline date or stated phrase. Never invent exact dates.")
    deadline_ambiguous: bool = Field(default=False, description="True if deadline was vague like 'soon', 'later', or unspecified.")
    priority: str = Field(default="Medium", description="Low, Medium, High, or Urgent.")
    status: str = Field(default="Pending", description="Draft, Pending Approval, Approved, Scheduled, In Progress, Completed, Blocked, Rejected.")
    approval_status: str = Field(default="Draft", description="Draft, Pending Approval, Approved, Rejected.")
    confidence: float = Field(default=0.95, ge=0.0, le=1.0, description="Estimated confidence score in extraction accuracy.")
    estimated_effort_hours: Optional[float] = Field(default=None, description="Estimated effort in hours if explicitly mentioned.")
    dependencies: List[str] = Field(default_factory=list, description="Titles or IDs of tasks this item depends upon.")
    extraction_reason: Optional[str] = Field(default=None, description="Explanation of why this task was extracted from dialogue.")

class ParticipantSchema(BaseModel):
    name: str = Field(default="Unknown Participant")
    speaker_id: str = Field(default="Unknown")
    responsibilities: List[str] = Field(default_factory=list)
    attendance_status: str = Field(default="Attended", description="Attended or Absent based on verified dialogue/participation.")

class DeadlineSchema(BaseModel):
    description: str
    date: str
    related_task: str

class PrioritySchema(BaseModel):
    item: str
    priority: str

class DecisionSchema(BaseModel):
    title: Optional[str] = Field(default=None, description="Brief concise title of the decision.")
    decision: str
    context: str
    rationale: Optional[str] = Field(default=None, description="Underlying reasons and justification for the decision.")
    alternatives: Optional[str] = Field(default=None, description="Alternative options discussed or discarded.")
    evidence_excerpt: Optional[str] = Field(default=None, description="Verbatim excerpt from dialogue supporting this decision.")
    confidence: float = Field(default=0.95, ge=0.0, le=1.0)
    proposer: Optional[str] = Field(default=None, description="Name of the person who proposed the decision.")
    status: str = Field(default="Approved", description="Proposed, Approved, Superseded, or Rejected.")
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
    
    # Optional and backward compatible fields
    executive_summary: Optional[str] = None
    meeting_objective: Optional[str] = None
    meeting_type: Optional[str] = None
    emotional_analysis: Optional[str] = Field(default="Neutral")
    key_topics: Optional[List[str]] = Field(default_factory=list)
    risks: Optional[List[RiskSchema]] = Field(default_factory=list)
    recommendations: Optional[List[str]] = Field(default_factory=list)
    next_steps: Optional[List[str]] = Field(default_factory=list)
    meeting_plan: Optional[str] = None

class MeetingPrepBriefSchema(BaseModel):
    meeting_purpose: str
    previous_meeting_summary: str
    unresolved_decisions: List[str]
    outstanding_action_items: List[str]
    blockers_and_risks: List[str]
    suggested_agenda: List[str]
    suggested_discussion_points: List[str]
