from typing import List, Optional
from pydantic import BaseModel, Field


class PersonalDetails(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


class ProjectItem(BaseModel):
    title: str = ""
    description: str = ""
    technologies: List[str] = Field(default_factory=list)
    evidence: str = ""


class EducationItem(BaseModel):
    degree: str = ""
    field: Optional[str] = ""
    institution: str = ""
    year: Optional[str] = ""


class ExperienceItem(BaseModel):
    role: str = ""
    company: str = ""
    duration: Optional[str] = ""
    responsibilities: List[str] = Field(default_factory=list)
    technologies: List[str] = Field(default_factory=list)


class CertificationItem(BaseModel):
    name: str = ""
    issuer: Optional[str] = ""
    year: Optional[str] = ""


class StructuredResume(BaseModel):
    personal: Optional[PersonalDetails] = Field(default_factory=PersonalDetails)
    skills: List[str] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    experience: List[ExperienceItem] = Field(default_factory=list)
    certifications: List[CertificationItem] = Field(default_factory=list)
    raw_text: Optional[str] = ""


class ResumeUploadResponse(BaseModel):
    file_name: str
    file_type: str
    file_size_bytes: int
    structured: StructuredResume
    message: str = "Resume parsed successfully"
