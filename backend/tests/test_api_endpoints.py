import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_get_roles():
    response = client.get("/api/roles")
    assert response.status_code == 200
    roles = response.json()
    assert len(roles) >= 4
    categories = [r["category"] for r in roles]
    assert "Frontend" in categories
    assert "Data" in categories
    assert "QA" in categories
    assert "Support" in categories


def test_analyze_endpoint_end_to_end():
    payload = {
        "resume_text": "Experienced web developer. Skills: HTML, CSS, JavaScript, Git. Built portfolio website using JavaScript and CSS.",
        "jd_text": "Role: Frontend Developer\nRequirements: HTML, CSS, JavaScript, React, Git.\nPreferred: REST APIs.",
        "target_role_category": "Frontend"
    }
    response = client.post("/api/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()
    
    assert "overall_score" in data
    assert "score_breakdown" in data
    assert "matched_skills" in data
    assert "partial_skills" in data
    assert "missing_skills" in data
    assert "recommendations" in data
    assert len(data["recommendations"]) == 3
    
    # Check partial React
    partial_names = [p["skill"] for p in data["partial_skills"]]
    assert "React" in partial_names


def test_empty_inputs_error_handling():
    # Empty JD
    res = client.post("/api/analyze", json={"resume_text": "HTML CSS", "jd_text": ""})
    assert res.status_code == 422 or res.status_code == 400

    # No Resume
    res2 = client.post("/api/analyze", json={"jd_text": "Need React developer"})
    assert res2.status_code == 400


def test_rewrite_bullet_endpoint():
    payload = {
        "original_bullet": "Created a website using React.",
        "role_context": "Frontend Developer"
    }
    response = client.post("/api/rewrite-bullet", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "suggested_bullet" in data
    assert "Developed" in data["suggested_bullet"] or "Engineered" in data["suggested_bullet"]
