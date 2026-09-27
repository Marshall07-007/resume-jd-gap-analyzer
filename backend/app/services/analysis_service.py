from datetime import datetime, timezone
from typing import Dict, List, Optional
from app.schemas.resume import StructuredResume
from app.schemas.job_description import JDParsed
from app.schemas.analysis import AnalysisResult, AnalysisRequest, SkillGapItem
from app.parsers.resume_parser import resume_parser
from app.parsers.jd_parser import jd_parser
from app.analyzers.gap_analyzer import gap_analyzer
from app.analyzers.scoring_engine import scoring_engine
from app.analyzers.recommendation_engine import recommendation_engine


class AnalysisService:
    def __init__(self):
        # In-memory history cache (can also be saved to SQLite)
        self.history: List[AnalysisResult] = []

    def perform_analysis(self, req: AnalysisRequest) -> AnalysisResult:
        # 1. Obtain structured resume
        if req.resume_structured and (req.resume_structured.skills or req.resume_structured.projects):
            resume = req.resume_structured
        elif req.resume_text:
            resume = resume_parser.parse(req.resume_text)
        else:
            raise ValueError("No resume content provided. Please upload a resume or provide resume text.")

        # 2. Obtain parsed JD
        if not req.jd_text or not req.jd_text.strip():
            raise ValueError("No job description provided. Please paste a job description.")
        
        jd = jd_parser.parse(req.jd_text)

        # 3. Gap Analysis
        matched, partial, missing, bonus, role_info = gap_analyzer.analyze(
            resume=resume,
            jd=jd,
            target_role_id=req.target_role_category,
        )

        # 4. Scoring
        overall_score, breakdown = scoring_engine.calculate_score(
            matched=matched,
            partial=partial,
            missing=missing,
            jd=jd,
            role_info=role_info,
        )

        # 5. Exactly 3 Traceable Recommendations
        recommendations = recommendation_engine.generate_recommendations(
            matched=matched,
            partial=partial,
            missing=missing,
            jd=jd,
            role_info=role_info,
            resume=resume,
        )

        # 6. Build combined gap table
        gap_table = matched + partial + missing + bonus

        result = AnalysisResult(
            overall_score=overall_score,
            score_breakdown=breakdown,
            matched_skills=matched,
            partial_skills=partial,
            missing_skills=missing,
            bonus_skills=bonus,
            gap_table=gap_table,
            recommendations=recommendations,
            detected_role=role_info.get("title", "Software Engineer"),
            resume_summary=resume,
            jd_summary=jd,
            created_at=datetime.now(timezone.utc).isoformat(),
        )

        self.history.append(result)
        return result

    def get_history(self) -> List[AnalysisResult]:
        return list(reversed(self.history))


analysis_service = AnalysisService()
