import pytest
from app.schemas.resume import StructuredResume, ProjectItem
from app.schemas.job_description import JDParsed
from app.analyzers.gap_analyzer import gap_analyzer
from app.analyzers.skill_normalizer import skill_normalizer
from app.analyzers.scoring_engine import scoring_engine
from app.analyzers.recommendation_engine import recommendation_engine
from app.analyzers.bullet_rewriter import bullet_rewriter
from app.parsers.resume_parser import resume_parser
from app.parsers.jd_parser import jd_parser


def test_skill_normalization():
    assert skill_normalizer.normalize("JS") == "JavaScript"
    assert skill_normalizer.normalize("javascript") == "JavaScript"
    assert skill_normalizer.normalize("ReactJS") == "React"
    assert skill_normalizer.normalize("React.js") == "React"
    assert skill_normalizer.normalize("NodeJS") == "Node.js"
    assert skill_normalizer.normalize("Postgres") == "PostgreSQL"


def test_case_1_javascript_resume_react_jd_is_partial():
    """Case 1: Resume has JavaScript, JD requires React -> Result: Partial"""
    resume = StructuredResume(
        skills=["JavaScript", "HTML", "CSS"],
        projects=[ProjectItem(title="Web Portfolio", description="Built UI with JavaScript", technologies=["JavaScript"])],
        raw_text="Skills: JavaScript, HTML, CSS. Built web apps using JavaScript."
    )
    jd = JDParsed(
        role="Frontend Developer",
        required_skills=["React"],
        preferred_skills=[],
        raw_text="Looking for a Frontend Developer. Must have strong experience with React."
    )

    matched, partial, missing, bonus, role_info = gap_analyzer.analyze(resume, jd, target_role_id="frontend")
    
    partial_skill_names = [p.skill for p in partial]
    matched_skill_names = [m.skill for m in matched]
    
    assert "React" in partial_skill_names, f"Expected React in partial skills, got: {partial_skill_names}"
    assert "React" not in matched_skill_names


def test_case_2_react_resume_react_jd_is_matched():
    """Case 2: Resume has React, JD requires React -> Result: Matched"""
    resume = StructuredResume(
        skills=["React", "JavaScript", "HTML", "CSS"],
        projects=[ProjectItem(title="React App", description="Single page app built with React", technologies=["React"])],
        raw_text="Skills: React, JavaScript. Built single page app in React."
    )
    jd = JDParsed(
        role="Frontend Developer",
        required_skills=["React"],
        preferred_skills=[],
        raw_text="Requirements: Experience with React."
    )

    matched, partial, missing, bonus, role_info = gap_analyzer.analyze(resume, jd, target_role_id="frontend")
    matched_skill_names = [m.skill for m in matched]

    assert "React" in matched_skill_names, f"Expected React in matched skills, got: {matched_skill_names}"


def test_case_3_no_docker_resume_docker_jd_is_missing():
    """Case 3: Resume has no Docker, JD requires Docker -> Result: Missing"""
    resume = StructuredResume(
        skills=["Python", "FastAPI"],
        projects=[ProjectItem(title="API Server", description="Built REST API", technologies=["Python"])],
        raw_text="Skills: Python, FastAPI. Built backend API."
    )
    jd = JDParsed(
        role="Backend Developer",
        required_skills=["Docker", "Python"],
        preferred_skills=[],
        raw_text="Requirements: Python, Docker required for container deployment."
    )

    matched, partial, missing, bonus, role_info = gap_analyzer.analyze(resume, jd)
    missing_skill_names = [m.skill for m in missing]

    assert "Docker" in missing_skill_names, f"Expected Docker in missing skills, got: {missing_skill_names}"


def test_recommendations_exactly_three_and_traceable():
    """Verify recommendation engine always returns exactly 3 traceable suggestions."""
    resume = StructuredResume(
        skills=["HTML", "CSS", "JavaScript"],
        raw_text="HTML, CSS, JavaScript"
    )
    jd = JDParsed(
        role="Frontend Developer",
        required_skills=["React", "Git"],
        preferred_skills=["REST APIs"],
        raw_text="Required: React, Git. Preferred: REST APIs"
    )

    matched, partial, missing, bonus, role_info = gap_analyzer.analyze(resume, jd, target_role_id="frontend")
    recs = recommendation_engine.generate_recommendations(matched, partial, missing, jd, role_info, resume)

    assert len(recs) == 3, f"Expected exactly 3 recommendations, got {len(recs)}"
    for r in recs:
        assert r.source_type in ["JD_REQUIRED", "JD_PREFERRED", "ROLE_SKILL_MAP"]
        assert len(r.suggestion) > 10
        assert len(r.reason) > 5
        assert len(r.source_text) > 0


def test_scoring_engine():
    """Verify explainable score calculation."""
    resume = StructuredResume(skills=["HTML", "CSS", "JavaScript", "Git"], raw_text="HTML CSS JavaScript Git")
    jd = JDParsed(role="Frontend Developer", required_skills=["HTML", "CSS", "JavaScript", "Git"], preferred_skills=["REST APIs"])
    matched, partial, missing, bonus, role_info = gap_analyzer.analyze(resume, jd, target_role_id="frontend")
    
    overall, breakdown = scoring_engine.calculate_score(matched, partial, missing, jd, role_info)
    assert 0 <= overall <= 100
    assert 0 <= breakdown.required_skills <= 100
    assert 0 <= breakdown.preferred_skills <= 100
    assert 0 <= breakdown.role_alignment <= 100


def test_bullet_rewriting_no_metric_fabrication():
    """Verify bullet rewriter improves verb/clarity without fabricating numbers or tech."""
    original = "Created a website using JavaScript."
    result = bullet_rewriter.rewrite(original)

    assert result.original_bullet == original
    assert result.action_verb_improved in ["Developed", "Engineered", "Implemented", "Architected"]
    assert not result.is_fabricated
    # Ensure no fabricated percentages or random numbers were added
    assert "%" not in result.suggested_bullet
    assert "$" not in result.suggested_bullet
