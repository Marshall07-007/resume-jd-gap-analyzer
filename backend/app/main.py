from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

from app.routes.resume import router as resume_router
from app.routes.analysis import router as analysis_router
from app.routes.roles import router as roles_router
from app.routes.bullets import router as bullets_router
from app.routes.health import router as health_router

app = FastAPI(
    title="Resume ↔ JD Gap Analyzer API",
    description="Production-grade API for structured resume parsing, job description analysis, explainable gap matching, and actionable career recommendations.",
    version="1.0.0",
)

# CORS Configuration for local frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers with /api prefix
app.include_router(health_router, prefix="/api")
app.include_router(resume_router, prefix="/api")
app.include_router(analysis_router, prefix="/api")
app.include_router(roles_router, prefix="/api")
app.include_router(bullets_router, prefix="/api")


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "path": request.url.path,
        },
    )


if __name__ == "__main__":
    uvicorn.run("app.main.py:app", host="127.0.0.1", port=8000, reload=True)
