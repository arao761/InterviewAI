"""
Dashboard schemas for user statistics and interview history.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class DashboardStatsResponse(BaseModel):
    """Dashboard statistics response."""
    total_interviews: int
    average_score: float
    best_score: Optional[float]
    hours_spent: float

    class Config:
        from_attributes = True


class InterviewHistoryItem(BaseModel):
    """Single interview history item."""
    id: int
    interview_type: Optional[str]
    technical_domain: Optional[str]
    date: datetime
    score: Optional[float]
    duration_minutes: Optional[float]
    status: str

    class Config:
        from_attributes = True


class InterviewHistoryResponse(BaseModel):
    """Interview history response."""
    interviews: List[InterviewHistoryItem]

    class Config:
        from_attributes = True

