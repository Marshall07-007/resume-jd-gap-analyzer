import re


SKILL_DATABASE = [
    "python",
    "java",
    "javascript",
    "typescript",
    "react",
    "html",
    "css",
    "fastapi",
    "django",
    "flask",
    "sql",
    "mysql",
    "sqlite",
    "mongodb",
    "git",
    "github",
    "rest api",
    "rest apis",
    "machine learning",
    "data analysis",
    "tensorflow",
    "pytorch",
    "node.js",
    "nodejs",
    "express",
    "docker",
    "aws",
    "azure",
    "linux",
    "c++",
    "c#"
]


def normalize_skill(skill: str) -> str:
    """Normalize similar skill names."""

    skill = skill.lower().strip()

    aliases = {
        "nodejs": "node.js",
        "rest apis": "rest api"
    }

    return aliases.get(skill, skill)


def extract_skills(text: str) -> list[str]:
    """Extract known skills from text."""

    text = text.lower()

    found_skills = []

    for skill in SKILL_DATABASE:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            normalized = normalize_skill(skill)

            if normalized not in found_skills:
                found_skills.append(normalized)

    return sorted(found_skills)


def calculate_gap_analysis(
    resume_text: str,
    job_description: str
):
    """Compare resume skills with JD skills."""

    resume_skills = extract_skills(resume_text)

    jd_skills = extract_skills(job_description)

    matched_skills = sorted(
        list(set(resume_skills) & set(jd_skills))
    )

    missing_skills = sorted(
        list(set(jd_skills) - set(resume_skills))
    )

    if jd_skills:
        match_score = round(
            (len(matched_skills) / len(jd_skills)) * 100,
            2
        )
    else:
        match_score = 0.0

    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": match_score
    }