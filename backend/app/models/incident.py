from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class LogEntry(BaseModel):
    """Represents a single log entry."""
    timestamp: Optional[str] = None
    level: Optional[str] = None
    message: str


class LogUploadRequest(BaseModel):
    """Request body for uploading logs."""
    logs: List[str] = Field(..., description="List of log messages")


class IncidentAnalysis(BaseModel):
    """Structured analysis result from the LLM."""
    summary: str = Field(..., description="Short incident summary")
    root_cause: str = Field(..., description="Likely root cause")
    severity_level: str = Field(..., description="P1 critical to P4 minor")
    recommended_owner: str = Field(..., description="Suggested responsible team")
    next_steps: str = Field(..., description="Recommended next action")


class AnalysisResult(BaseModel):
    """Full analysis result with metadata."""
    id: str
    logs: List[str]
    similar_incidents: Optional[List[str]] = None
    analysis: IncidentAnalysis
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class AnalyzeRequest(BaseModel):
    """Request body for incident analysis."""
    logs: Optional[List[str]] = Field(None, description="Log messages to analyze")
    query: Optional[str] = Field(None, description="Incident description or query")
