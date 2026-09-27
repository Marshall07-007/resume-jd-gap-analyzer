import re
from typing import Dict, List, Optional
from app.schemas.resume import (
    StructuredResume,
    PersonalDetails,
    ProjectItem,
    EducationItem,
    ExperienceItem,
    CertificationItem,
)
from app.analyzers.skill_normalizer import skill_normalizer


class ResumeParser:
    SECTION_HEADERS = {
        "skills": [r"skills?", r"technical skills?", r"technologies", r"core competencies", r"tools & technologies", r"tech stack"],
        "projects": [r"projects?", r"academic projects?", r"personal projects?", r"key projects?"],
        "education": [r"education", r"academic background", r"academics", r"qualifications", r"degrees?"],
        "experience": [r"experience", r"work experience", r"employment history", r"professional experience", r"internships?"],
        "certifications": [r"certifications?", r"certificates?", r"licenses & certifications", r"courses? & certifications?"],
    }

    EMAIL_REGEX = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    PHONE_REGEX = r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}"
    LINKEDIN_REGEX = r"(?:https?://)?(?:www\.)?linkedin\.com/in/[a-zA-Z0-9_-]+"
    GITHUB_REGEX = r"(?:https?://)?(?:www\.)?github\.com/[a-zA-Z0-9_-]+"

    def parse(self, raw_text: str) -> StructuredResume:
        """
        Parse raw resume text into structured schema.
        """
        if not raw_text or not raw_text.strip():
            return StructuredResume()

        clean_text = self._clean_text(raw_text)
        sections = self._segment_sections(clean_text)
        
        personal = self._extract_personal(clean_text)
        skills = self._extract_skills(clean_text, sections.get("skills", ""))
        projects = self._extract_projects(sections.get("projects", ""))
        education = self._extract_education(sections.get("education", ""))
        experience = self._extract_experience(sections.get("experience", ""))
        certifications = self._extract_certifications(sections.get("certifications", ""))

        return StructuredResume(
            personal=personal,
            skills=skills,
            projects=projects,
            education=education,
            experience=experience,
            certifications=certifications,
            raw_text=clean_text,
        )

    def _clean_text(self, text: str) -> str:
        # Normalize carriage returns and non-breaking spaces
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = text.replace("\xa0", " ").replace("\u200b", "")
        # Remove repeated horizontal lines or decorative dashes
        text = re.sub(r"[-_=]{3,}", "---", text)
        return text.strip()

    def _segment_sections(self, text: str) -> Dict[str, str]:
        """
        Split text into logical sections based on headers.
        """
        lines = text.split("\n")
        sections: Dict[str, List[str]] = {}
        current_section = "header"

        # Build regex for matching any section header line
        header_patterns = {}
        for section_name, patterns in self.SECTION_HEADERS.items():
            pattern = r"^\s*(?:" + "|".join(patterns) + r")\s*[:\-—]*\s*$"
            header_patterns[section_name] = re.compile(pattern, re.IGNORECASE)

        for line in lines:
            line_str = line.strip()
            if not line_str:
                continue

            # Check if this line matches a section header
            matched_header = None
            for section_name, regex in header_patterns.items():
                if regex.match(line_str) or (len(line_str.split()) <= 4 and any(re.search(rf"\b{p}\b", line_str, re.IGNORECASE) for p in self.SECTION_HEADERS[section_name]) and line_str.isupper()):
                    matched_header = section_name
                    break

            if matched_header:
                current_section = matched_header
                if current_section not in sections:
                    sections[current_section] = []
            else:
                if current_section not in sections:
                    sections[current_section] = []
                sections[current_section].append(line_str)

        return {k: "\n".join(v) for k, v in sections.items()}

    def _extract_personal(self, text: str) -> PersonalDetails:
        personal = PersonalDetails()
        
        # Email
        email_match = re.search(self.EMAIL_REGEX, text)
        if email_match:
            personal.email = email_match.group(0)

        # Phone
        phone_match = re.search(self.PHONE_REGEX, text)
        if phone_match:
            personal.phone = phone_match.group(0)

        # LinkedIn
        li_match = re.search(self.LINKEDIN_REGEX, text, re.IGNORECASE)
        if li_match:
            personal.linkedin = li_match.group(0)

        # GitHub
        gh_match = re.search(self.GITHUB_REGEX, text, re.IGNORECASE)
        if gh_match:
            personal.github = gh_match.group(0)

        # Name heuristic: First non-empty line of the resume that doesn't contain email/phone/url
        first_lines = text.split("\n")[:5]
        for line in first_lines:
            l = line.strip()
            if l and len(l) < 50 and not any(char in l for char in ["@", "http", ".com", "|", "/", "\\"]):
                if not any(re.search(p, l, re.IGNORECASE) for patterns in self.SECTION_HEADERS.values() for p in patterns):
                    personal.name = l
                    break

        return personal

    def _extract_skills(self, full_text: str, skills_section_text: str) -> List[str]:
        """
        Extract normalized skills from the skills section and the entire resume.
        """
        skills_set = set()
        
        # 1. First extract explicitly from Skills section
        if skills_section_text:
            # Handle comma/bullet separated lines
            direct_skills = skill_normalizer.extract_skills_from_text(skills_section_text)
            skills_set.update(direct_skills)
            
            # Also check comma-separated tokens
            for line in skills_section_text.split("\n"):
                tokens = re.split(r"[,;|•\t]", line)
                for token in tokens:
                    tok = token.strip()
                    if tok and len(tok) <= 30:
                        norm = skill_normalizer.normalize(tok)
                        if norm:
                            skills_set.add(norm)

        # 2. Extract any recognized skills across the entire resume text
        all_text_skills = skill_normalizer.extract_skills_from_text(full_text)
        skills_set.update(all_text_skills)

        return sorted(list(skills_set))

    def _extract_projects(self, projects_text: str) -> List[ProjectItem]:
        if not projects_text:
            return []

        projects: List[ProjectItem] = []
        # Split projects by bullet headers or double newlines or dates
        blocks = re.split(r"\n(?=[A-Z0-9][\w\s\-–]+(?:\(|\||–|-|Technologies|Tech Stack|20\d\d))", projects_text)
        if len(blocks) <= 1:
            blocks = [p for p in projects_text.split("\n\n") if p.strip()]

        for block in blocks:
            lines = [l.strip() for l in block.split("\n") if l.strip()]
            if not lines:
                continue

            title = lines[0]
            # Clean title
            title = re.sub(r"^[•\-\*]\s*", "", title)
            
            desc_lines = lines[1:] if len(lines) > 1 else lines
            description = " ".join(desc_lines)
            
            # Extract technologies in this project block
            techs = skill_normalizer.extract_skills_from_text(block)
            
            projects.append(
                ProjectItem(
                    title=title,
                    description=description,
                    technologies=techs,
                    evidence=f"{title}: {description[:120]}..." if len(description) > 120 else f"{title}: {description}",
                )
            )

        return projects

    def _extract_education(self, education_text: str) -> List[EducationItem]:
        if not education_text:
            return []

        education_list: List[EducationItem] = []
        lines = [l.strip() for l in education_text.split("\n") if l.strip()]
        
        deg_pattern = r"(Bachelor|Master|B\.S\.|M\.S\.|B\.Tech|M\.Tech|B\.E\.|BCA|MCA|Associate|Ph\.D\.|High School)[\w\s,.]*"
        year_pattern = r"(20\d\d|19\d\d)(?:\s*[-–]\s*(?:20\d\d|Present|Current))?"

        for line in lines:
            deg_match = re.search(deg_pattern, line, re.IGNORECASE)
            year_match = re.search(year_pattern, line)
            
            deg = deg_match.group(0).strip() if deg_match else "Degree / Studies"
            yr = year_match.group(0).strip() if year_match else ""
            
            # Try to get institution by stripping degree and year
            inst = line
            if deg_match:
                inst = inst.replace(deg_match.group(0), "")
            if year_match:
                inst = inst.replace(year_match.group(0), "")
            inst = re.sub(r"^[•\-\*|, ]+|[•\-\*|, ]+$", "", inst).strip()
            
            if not inst and not deg_match and not year_match:
                continue

            education_list.append(
                EducationItem(
                    degree=deg,
                    institution=inst or "University / College",
                    year=yr,
                )
            )

        if not education_list and lines:
            education_list.append(
                EducationItem(
                    degree="Degree / Coursework",
                    institution=lines[0],
                    year="",
                )
            )

        return education_list

    def _extract_experience(self, exp_text: str) -> List[ExperienceItem]:
        if not exp_text:
            return []

        exp_list: List[ExperienceItem] = []
        blocks = [b.strip() for b in exp_text.split("\n\n") if b.strip()]
        if len(blocks) <= 1:
            blocks = [exp_text]

        for block in blocks:
            lines = [l.strip() for l in block.split("\n") if l.strip()]
            if not lines:
                continue
            
            role = lines[0]
            company = ""
            if len(lines) > 1 and not lines[1].startswith(("-", "•", "*")):
                company = lines[1]
                responsibilities = lines[2:]
            else:
                responsibilities = lines[1:]

            techs = skill_normalizer.extract_skills_from_text(block)

            exp_list.append(
                ExperienceItem(
                    role=role,
                    company=company,
                    duration="",
                    responsibilities=responsibilities,
                    technologies=techs,
                )
            )

        return exp_list

    def _extract_certifications(self, cert_text: str) -> List[CertificationItem]:
        if not cert_text:
            return []
        
        certs = []
        for line in cert_text.split("\n"):
            l = line.strip()
            if l:
                clean_name = re.sub(r"^[•\-\*]\s*", "", l)
                certs.append(CertificationItem(name=clean_name))
        return certs


resume_parser = ResumeParser()
