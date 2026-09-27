from typing import List, Optional
from pydantic import BaseModel, Field


class BulletRewriteRequest(BaseModel):
    original_bullet: str = Field(..., min_length=3, description="Original bullet text from resume")
    target_skill: Optional[str] = None
    role_context: Optional[str] = "Software Engineer"


class BulletRewriteResponse(BaseModel):
    original_bullet: str
    suggested_bullet: str
    action_verb_improved: str
    key_technologies_highlighted: List[str] = Field(default_factory=list)
    explanation: str
    is_fabricated: bool = False
