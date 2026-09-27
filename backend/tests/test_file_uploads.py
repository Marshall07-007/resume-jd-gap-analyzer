import os
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

samples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "samples")


def test_upload_real_pdf_resume():
    pdf_path = os.path.join(samples_dir, "sample_resume_frontend.pdf")
    assert os.path.exists(pdf_path), "Sample PDF should exist"

    with open(pdf_path, "rb") as f:
        response = client.post(
            "/api/resume/upload",
            files={"file": ("sample_resume_frontend.pdf", f, "application/pdf")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["file_name"] == "sample_resume_frontend.pdf"
    assert data["file_type"] == "PDF"
    assert len(data["structured"]["skills"]) > 0
    assert "HTML" in data["structured"]["skills"] or "JavaScript" in data["structured"]["skills"]


def test_upload_real_docx_resume():
    docx_path = os.path.join(samples_dir, "sample_resume_qa.docx")
    assert os.path.exists(docx_path), "Sample DOCX should exist"

    with open(docx_path, "rb") as f:
        response = client.post(
            "/api/resume/upload",
            files={"file": ("sample_resume_qa.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["file_name"] == "sample_resume_qa.docx"
    assert data["file_type"] == "DOCX"
    assert len(data["structured"]["skills"]) > 0
    assert "Manual Testing" in data["structured"]["skills"] or "Postman" in data["structured"]["skills"]
