from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Resume ↔ JD Gap Analyzer API",
        "version": "1.0.0",
        "parsers": ["PyMuPDF", "python-docx"],
        "analyzers": ["SkillNormalizer", "GapAnalyzer", "ScoringEngine", "RecommendationEngine"],
    }
