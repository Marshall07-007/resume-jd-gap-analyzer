from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from app.schemas.resume import StructuredResume
from app.schemas.job_description import JDParsed


class SkillGapItem(BaseModel):
    skill: str
    status: Literal["matched", "partial", "missing", "bonus"]
    resume_evidence: str = "Not found in resume"
    jd_evidence: str = "Not specified"
    source: str = "JD"  # "JD", "Role Skill Map", "Resume"
    category: Optional[str] = "General"
    explanation: Optional[str] = ""


class ScoreBreakdown(BaseModel):
    required_skills: float = Field(..., description="Coverage percentage of required skills")
    preferred_skills: float = Field(..., description="Coverage percentage of preferred skills")
    role_alignment: float = Field(..., description="Alignment with curated role skill map")
    overall_match: float = Field(..., description="Weighted composite score 0-100")


class RecommendationItem(BaseModel):
    id: int
    suggestion: str
    reason: str
    source_type: Literal["JD_REQUIRED", "JD_PREFERRED", "ROLE_SKILL_MAP"]
    source_text: str
    priority: Literal["high", "medium", "low"] = "high"
    actionable_steps: List[str] = Field(default_factory=list)


class AnalysisRequest(BaseModel):
    resume_structured: Optional[StructuredResume] = None
    resume_text: Optional[str] = None
    jd_text: str = Field(..., min_length=1)
    target_role_category: Optional[str] = None  # "Frontend", "Data", "QA", "Support", or auto-detect


class AnalysisResult(BaseModel):
    overall_score: int
    score_breakdown: ScoreBreakdown
    matched_skills: List[SkillGapItem] = Field(default_factory=list)
    partial_skills: List[SkillGapItem] = Field(default_factory=list)
    missing_skills: List[SkillGapItem] = Field(default_factory=list)
    bonus_skills: List[SkillGapItem] = Field(default_factory=list)
    gap_table: List[SkillGapItem] = Field(default_factory=list)
    recommendations: List[RecommendationItem] = Field(default_factory=list)
    detected_role: str
    resume_summary: StructuredResume
    jd_summary: JDParsed
    created_at: Optional[str] = None
