from typing import List
from fastapi import APIRouter, HTTPException
from app.schemas.analysis import AnalysisRequest, AnalysisResult
from app.services.analysis_service import analysis_service

router = APIRouter(tags=["Analysis"])


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_gap(req: AnalysisRequest):
    try:
        result = analysis_service.perform_analysis(req)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gap analysis encountered an error: {str(e)}")


@router.get("/analyses", response_model=List[AnalysisResult])
async def get_analysis_history():
    return analysis_service.get_history()
