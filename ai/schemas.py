from pydantic import BaseModel, Field
from typing import List, Optional

class ActionItemSchema(BaseModel):
    task: str
    owner: str = Field(default="Not specified")
    deadline: str = Field(default="Not specified")
    priority: str = Field(default="Medium")
    status: str = Field(default="Pending")

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
    executive_summary: str
    meeting_objective: str = Field(default="Not explicitly identified")
    meeting_type: str
    emotional_analysis: str = Field(default="Neutral")
    key_topics: List[str]
    key_points: List[str]
    decisions: List[DecisionSchema]
    action_items: List[ActionItemSchema]
    risks: List[RiskSchema]
    recommendations: List[str]
    next_steps: List[str]
    meeting_plan: str
