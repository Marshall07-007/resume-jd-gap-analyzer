from typing import List, Optional
from pydantic import BaseModel, Field


class JDParseRequest(BaseModel):
    jd_text: str = Field(..., min_length=1, description="Raw job description text")


class JDParsed(BaseModel):
    role: str = "Software Engineer"
    company: Optional[str] = None
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    responsibilities: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    detected_role_category: Optional[str] = None
    raw_text: Optional[str] = ""
