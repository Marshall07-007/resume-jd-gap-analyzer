from fastapi import APIRouter, HTTPException
from app.schemas.bullet import BulletRewriteRequest, BulletRewriteResponse
from app.analyzers.bullet_rewriter import bullet_rewriter

router = APIRouter(tags=["Bullet Rewrite"])


@router.post("/rewrite-bullet", response_model=BulletRewriteResponse)
async def rewrite_bullet(req: BulletRewriteRequest):
    if not req.original_bullet or len(req.original_bullet.strip()) < 3:
        raise HTTPException(status_code=400, detail="Bullet text must have at least 3 characters.")
    
    return bullet_rewriter.rewrite(
        original_bullet=req.original_bullet,
        target_skill=req.target_skill,
        role_context=req.role_context or "Software Engineer",
    )
