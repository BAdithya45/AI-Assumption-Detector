from pydantic import BaseModel, Field
from typing import Literal
from enum import Enum


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class AnalysisRequest(BaseModel):
    text: str = Field(description="The text to analyze for hidden assumptions")


class Assumption(BaseModel):
    text: str = Field(description="The identified assumption")
    risk: RiskLevel = Field(description="Risk level of the assumption")
    confidence: float = Field(ge=0, le=1, description="Confidence score between 0 and 1")
    explanation: str = Field(description="Why this is considered an assumption")
    validation: str = Field(description="Suggested way to validate this assumption")


class AnalysisResult(BaseModel):
    assumptions: list[Assumption] = Field(default_factory=list)
    summary: str = Field(default="")
