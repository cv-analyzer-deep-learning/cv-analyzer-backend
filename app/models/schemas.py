from pydantic import BaseModel, Field
from typing import List

class RadarChartData(BaseModel):
    technical_skills: int = Field(..., ge=1, le=5)
    domain_knowledge: int = Field(..., ge=1, le=5)
    tooling_and_infrastructure: int = Field(..., ge=1, le=5)
    soft_skills: int = Field(..., ge=1, le=5)
    experience_level: int = Field(..., ge=1, le=5)

class AnalysisResponse(BaseModel):
    compatibility_score: int = Field(..., ge=0, le=100)
    radar_chart_data: RadarChartData
    matching_entities: List[str]
    missing_entities: List[str]
    actionable_feedback: List[str]