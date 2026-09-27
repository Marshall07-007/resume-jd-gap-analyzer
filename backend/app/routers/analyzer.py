from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models.schemas import AnalyzeResponse
from app.services.document_parser import extract_resume_text
from app.services.skill_analyzer import calculate_gap_analysis

router = APIRouter(prefix="/analyze", tags=["Resume Analysis"])


@router.post("/", response_model=AnalyzeResponse)
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    allowed_extensions = (".pdf", ".docx")

    if not resume.filename.lower().endswith(allowed_extensions):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    if not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty."
        )

    try:
        file_content = await resume.read()

        resume_text = extract_resume_text(
            resume.filename,
            file_content
        )

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the resume."
            )

        analysis = calculate_gap_analysis(
            resume_text,
            job_description
        )

        suggestions = []

        if analysis["missing_skills"]:
            suggestions.append(
                "Learn and add relevant missing skills to your portfolio."
            )

        suggestions.append(
            "Add measurable achievements to your project descriptions."
        )

        suggestions.append(
            "Tailor your resume keywords to match the job description."
        )

        return AnalyzeResponse(
            filename=resume.filename,
            resume_skills=analysis["resume_skills"],
            jd_skills=analysis["jd_skills"],
            matched_skills=analysis["matched_skills"],
            missing_skills=analysis["missing_skills"],
            match_score=analysis["match_score"],
            suggestions=suggestions
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )