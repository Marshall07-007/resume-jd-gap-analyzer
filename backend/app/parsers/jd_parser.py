import re
from typing import List, Set, Tuple
from app.schemas.job_description import JDParsed
from app.analyzers.skill_normalizer import skill_normalizer


class JDParser:
    REQUIRED_CUES = [
        r"\brequired\b",
        r"\bmust have\b",
        r"\bminimum qualifications\b",
        r"\brequirements\b",
        r"\bessential\b",
        r"\bcore requirements\b",
        r"\bexperience with\b",
        r"\bstrong background in\b",
        r"\bproficient in\b",
        r"\bhands-on experience\b",
        r"\bmandatory\b",
    ]

    PREFERRED_CUES = [
        r"\bpreferred\b",
        r"\bplus\b",
        r"\bnice to have\b",
        r"\bgood to have\b",
        r"\bbonus\b",
        r"\boptional\b",
        r"\badditional\b",
        r"\bdesired\b",
    ]

    TOOL_KEYWORDS = [
        "Git", "Docker", "Postman", "Selenium", "Jira", "Linux", "VS Code", "Figma", "Kubernetes", "AWS", "Azure"
    ]

    def parse(self, jd_text: str) -> JDParsed:
        """
        Parse JD text into structured requirements, distinguishing required vs preferred skills.
        """
        if not jd_text or not jd_text.strip():
            return JDParsed(raw_text="")

        clean_text = jd_text.strip()
        lines = [l.strip() for l in clean_text.split("\n") if l.strip()]

        role_title = self._detect_role_title(lines, clean_text)
        required_skills, preferred_skills = self._categorize_skills(clean_text, lines)
        responsibilities = self._extract_responsibilities(lines)
        tools = self._extract_tools(required_skills + preferred_skills, clean_text)
        keywords = self._extract_keywords(clean_text)

        return JDParsed(
            role=role_title,
            company="",
            required_skills=required_skills,
            preferred_skills=preferred_skills,
            tools=tools,
            responsibilities=responsibilities,
            keywords=keywords,
            raw_text=clean_text,
        )

    def _detect_role_title(self, lines: List[str], full_text: str) -> str:
        # Check first 3 lines
        for line in lines[:3]:
            if len(line) < 60 and any(kw in line.lower() for kw in ["developer", "engineer", "analyst", "specialist", "intern", "qa", "support", "tester"]):
                return line.strip("#-*• \t")
        
        # Search for "Role:", "Job Title:", "Position:"
        match = re.search(r"(?:Job Title|Position|Role|Title)\s*:\s*([^\n\r]+)", full_text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        return "Software Engineer / Technical Role"

    def _categorize_skills(self, full_text: str, lines: List[str]) -> Tuple[List[str], List[str]]:
        required_skills: Set[str] = set()
        preferred_skills: Set[str] = set()

        current_mode = "required"  # Default assumption for listed skills

        for line in lines:
            line_lower = line.lower()

            # Check if line indicates section switch
            if any(re.search(cue, line_lower) for cue in self.PREFERRED_CUES):
                current_mode = "preferred"
            elif any(re.search(cue, line_lower) for cue in self.REQUIRED_CUES):
                current_mode = "required"

            skills_in_line = skill_normalizer.extract_skills_from_text(line)

            if current_mode == "preferred":
                for s in skills_in_line:
                    preferred_skills.add(s)
            else:
                for s in skills_in_line:
                    required_skills.add(s)

        # Remove from required if explicitly in preferred
        required_skills = required_skills - preferred_skills

        # If no skills categorized as required but full text has skills, extract all as required
        if not required_skills and not preferred_skills:
            all_skills = skill_normalizer.extract_skills_from_text(full_text)
            required_skills = set(all_skills)

        return sorted(list(required_skills)), sorted(list(preferred_skills))

    def _extract_responsibilities(self, lines: List[str]) -> List[str]:
        responsibilities = []
        in_resp_section = False

        for line in lines:
            if re.search(r"\b(responsibilities|what you'll do|role overview|duties)\b", line, re.IGNORECASE):
                in_resp_section = True
                continue
            elif in_resp_section and re.search(r"\b(requirements|qualifications|skills|about you|benefits)\b", line, re.IGNORECASE):
                in_resp_section = False
                continue

            if in_resp_section and (line.startswith(("-", "•", "*")) or len(line) > 30):
                responsibilities.append(re.sub(r"^[•\-\*]\s*", "", line))

        return responsibilities[:8]

    def _extract_tools(self, found_skills: List[str], full_text: str) -> List[str]:
        tools = set()
        for t in self.TOOL_KEYWORDS:
            canonical = skill_normalizer.normalize(t)
            if canonical in found_skills or re.search(rf"\b{re.escape(t)}\b", full_text, re.IGNORECASE):
                tools.add(canonical)
        return sorted(list(tools))

    def _extract_keywords(self, text: str) -> List[str]:
        # General tech buzzwords and methodologies
        buzzwords = ["Agile", "Scrum", "CI/CD", "Microservices", "RESTful", "TDD", "Clean Code", "Design Patterns", "Cross-browser Compatibility"]
        found = []
        for b in buzzwords:
            if re.search(rf"\b{re.escape(b)}\b", text, re.IGNORECASE):
                found.append(b)
        return found


jd_parser = JDParser()
