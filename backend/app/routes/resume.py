from fastapi import APIRouter, File, UploadFile, HTTPException, Body
from app.parsers.document_parser import DocumentParser, DocumentParserError
from app.parsers.resume_parser import resume_parser
from app.schemas.resume import ResumeUploadResponse, StructuredResume

router = APIRouter(prefix="/resume", tags=["Resume"])


@router.post("/upload", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")

    filename = file.filename.lower()
    if not (filename.endswith(".pdf") or filename.endswith(".docx")):
        raise HTTPException(
            status_code=400,
            detail="Invalid file format. Only .pdf and .docx documents are supported.",
        )

    try:
        file_bytes = await file.read()
        if not file_bytes:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")

        raw_text = DocumentParser.extract_text_from_bytes(file_bytes, file.filename)
        structured = resume_parser.parse(raw_text)

        return ResumeUploadResponse(
            file_name=file.filename,
            file_type=filename.split(".")[-1].upper(),
            file_size_bytes=len(file_bytes),
            structured=structured,
            message="Resume successfully uploaded and structured.",
        )
    except DocumentParserError as de:
        raise HTTPException(status_code=422, detail=str(de))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process resume: {str(e)}")


@router.post("/parse", response_model=StructuredResume)
async def parse_resume_text(body: dict = Body(...)):
    raw_text = body.get("raw_text", "")
    if not raw_text or not raw_text.strip():
        raise HTTPException(status_code=400, detail="Resume text is required.")
    
    return resume_parser.parse(raw_text)
