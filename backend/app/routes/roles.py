from typing import List, Dict, Any
from fastapi import APIRouter
from app.analyzers.role_matcher import role_matcher

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("", response_model=List[Dict[str, Any]])
async def get_roles():
    return role_matcher.get_all_roles()
