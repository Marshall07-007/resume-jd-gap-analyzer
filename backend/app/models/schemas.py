from pydantic import BaseModel, Field
from typing import List


# -----------------------------
# Resume Structures
# -----------------------------

class Project(BaseModel):
    name: str
    description: str = ""
    technologies: List[str] = []


class Education(BaseModel):
    degree: str = ""
    institution: str = ""


class Experience(BaseModel):
    company: str = ""
    role: str = ""
    description: str = ""


class ResumeData(BaseModel):
    skills: List[str] = []
    projects: List[Project] = []
    education: List[Education] = []
    experience: List[Experience] = []


# -----------------------------
# Job Description Structures
# -----------------------------

class JobDescriptionData(BaseModel):
    job_title: str = ""
    required_skills: List[str] = []
    preferred_skills: List[str] = []
    responsibilities: List[str] = []


# -----------------------------
# Analysis Result Structures
# -----------------------------

class SkillMatch(BaseModel):
    skill: str
    sources: List[str] = []


class MissingSkill(BaseModel):
    skill: str
    sources: List[str] = []


class Suggestion(BaseModel):
    suggestion: str
    sources: List[str] = []


# -----------------------------
# Current API Response
# -----------------------------

class AnalyzeResponse(BaseModel):
    filename: str
    resume_text: str
    job_description: str


# -----------------------------
# Final Gap Analysis Response
# (We will use this later)
# -----------------------------

class GapAnalysisResponse(BaseModel):
    match_score: float = Field(
        ...,
        ge=0,
        le=100,
        description="Match percentage between resume and job description"
    )

    matched_skills: List[SkillMatch] = []
    missing_skills: List[MissingSkill] = []

    suggestions: List[Suggestion] = []

    retrieved_role: str = ""

    sources: List[str] = []