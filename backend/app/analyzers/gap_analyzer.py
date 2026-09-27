import re
from typing import Dict, List, Set, Tuple
from app.schemas.resume import StructuredResume
from app.schemas.job_description import JDParsed
from app.schemas.analysis import SkillGapItem
from app.analyzers.skill_normalizer import skill_normalizer
from app.analyzers.role_matcher import role_matcher


class GapAnalyzer:
    def analyze(
        self,
        resume: StructuredResume,
        jd: JDParsed,
        target_role_id: str = None,
    ) -> Tuple[List[SkillGapItem], List[SkillGapItem], List[SkillGapItem], List[SkillGapItem], Dict]:
        """
        Performs gap analysis comparing Resume vs JD vs Curated Role Skill Map.
        Returns (matched, partial, missing, bonus, role_info).
        """
        # 1. Determine Role Category
        if target_role_id:
            role_info = role_matcher.get_role_by_id_or_category(target_role_id)
        else:
            role_info = role_matcher.detect_role(
                jd_text=jd.raw_text or "",
                jd_role_title=jd.role or "",
                extracted_skills=jd.required_skills + jd.preferred_skills,
            )

        if not role_info:
            role_info = role_matcher.get_all_roles()[0]

        # 2. Normalize and collect resume skills & evidence sources
        resume_skills_canonical = {skill_normalizer.normalize(s) for s in resume.skills if s}
        resume_raw_text = (resume.raw_text or "").lower()

        # Build resume evidence mapping
        resume_evidence_map = self._build_resume_evidence_map(resume, resume_skills_canonical)

        # 3. Collect target skills from JD and Role
        jd_required = [skill_normalizer.normalize(s) for s in jd.required_skills if s]
        jd_preferred = [skill_normalizer.normalize(s) for s in jd.preferred_skills if s]
        role_core = [skill_normalizer.normalize(s) for s in role_info.get("core_skills", [])]

        all_target_skills: Dict[str, Dict] = {}

        # Add JD Required
        for s in jd_required:
            if s:
                all_target_skills[s] = {
                    "source": "JD",
                    "importance": "required",
                    "jd_evidence": self._find_jd_snippet(jd.raw_text or "", s, "Required Skill in JD"),
                }

        # Add JD Preferred
        for s in jd_preferred:
            if s and s not in all_target_skills:
                all_target_skills[s] = {
                    "source": "JD",
                    "importance": "preferred",
                    "jd_evidence": self._find_jd_snippet(jd.raw_text or "", s, "Preferred / Nice-to-have in JD"),
                }

        # Add Role Core skills if not already present
        for s in role_core:
            if s and s not in all_target_skills:
                all_target_skills[s] = {
                    "source": "Role Skill Map",
                    "importance": "role_core",
                    "jd_evidence": f"Core expectation for {role_info.get('title', 'Role')}",
                }

        matched: List[SkillGapItem] = []
        partial: List[SkillGapItem] = []
        missing: List[SkillGapItem] = []
        processed_skills: Set[str] = set()

        for skill, meta in all_target_skills.items():
            processed_skills.add(skill.lower())

            # Check for EXACT / DIRECT MATCH in resume
            if skill in resume_skills_canonical or self._has_exact_mention_in_text(resume_raw_text, skill):
                res_evidence = resume_evidence_map.get(skill, f"Directly mentioned in resume text or skills list.")
                matched.append(
                    SkillGapItem(
                        skill=skill,
                        status="matched",
                        resume_evidence=res_evidence,
                        jd_evidence=meta["jd_evidence"],
                        source=meta["source"],
                        explanation=f"Resume clearly demonstrates '{skill}'.",
                    )
                )
                continue

            # Check for PARTIAL MATCH (related foundational or peer skill)
            related_found, relation_explanation = self._check_partial_match(skill, resume_skills_canonical, resume_raw_text)
            if related_found:
                partial.append(
                    SkillGapItem(
                        skill=skill,
                        status="partial",
                        resume_evidence=relation_explanation["resume_evidence"],
                        jd_evidence=meta["jd_evidence"],
                        source=meta["source"],
                        explanation=relation_explanation["explanation"],
                    )
                )
                continue

            # Otherwise MISSING
            missing.append(
                SkillGapItem(
                    skill=skill,
                    status="missing",
                    resume_evidence="No sufficient evidence found in resume.",
                    jd_evidence=meta["jd_evidence"],
                    source=meta["source"],
                    explanation=f"Required for {role_info.get('title', 'Role')} but missing from resume.",
                )
            )

        # 4. Detect BONUS skills from resume that are relevant but not targeted
        bonus: List[SkillGapItem] = []
        for s in resume_skills_canonical:
            if s.lower() not in processed_skills and len(s) > 1:
                res_ev = resume_evidence_map.get(s, "Listed in resume skills.")
                bonus.append(
                    SkillGapItem(
                        skill=s,
                        status="bonus",
                        resume_evidence=res_ev,
                        jd_evidence="Additional candidate strength not explicitly demanded by JD",
                        source="Resume",
                        explanation=f"Demonstrates additional technical breadth.",
                    )
                )

        return matched, partial, missing, bonus, role_info

    def _has_exact_mention_in_text(self, text: str, skill: str) -> bool:
        if not text or not skill:
            return False
        pattern = r"(?:^|[\s,;./()\-\[\]])" + re.escape(skill.lower()) + r"(?:$|[\s,;./()\-\[\]])"
        return bool(re.search(pattern, text))

    def _check_partial_match(
        self, req_skill: str, resume_skills: Set[str], resume_raw_text: str
    ) -> Tuple[bool, Dict[str, str]]:
        """
        Check if resume has related foundational technology for req_skill.
        E.g., if React is required, and resume has JavaScript.
        """
        for r_skill in resume_skills:
            is_rel, rel_exp = skill_normalizer.is_related(req_skill, r_skill)
            if is_rel:
                return True, {
                    "resume_evidence": f"Found related skill '{r_skill}' in resume.",
                    "explanation": f"Candidate possesses foundational '{r_skill}', but '{req_skill}' is not explicitly demonstrated.",
                }
        return False, {}

    def _build_resume_evidence_map(self, resume: StructuredResume, resume_skills: Set[str]) -> Dict[str, str]:
        evidence_map: Dict[str, str] = {}

        # Skills list evidence
        for s in resume.skills:
            norm = skill_normalizer.normalize(s)
            evidence_map[norm] = f"Explicitly listed under Skills section ({s})."

        # Projects evidence (higher quality)
        for proj in resume.projects:
            for tech in proj.technologies:
                norm = skill_normalizer.normalize(tech)
                evidence_map[norm] = f"Applied in Project '{proj.title}': {proj.description[:100]}..."

        # Experience evidence
        for exp in resume.experience:
            for tech in exp.technologies:
                norm = skill_normalizer.normalize(tech)
                evidence_map[norm] = f"Demonstrated in Experience at '{exp.company}' ({exp.role})."

        return evidence_map

    def _find_jd_snippet(self, jd_text: str, skill: str, default_label: str) -> str:
        if not jd_text:
            return default_label
        
        # Look for the sentence containing the skill
        sentences = re.split(r"[.\n•\-]", jd_text)
        for sentence in sentences:
            if re.search(r"\b" + re.escape(skill) + r"\b", sentence, re.IGNORECASE):
                snippet = sentence.strip()
                if len(snippet) > 10:
                    return snippet[:120]

        return default_label


gap_analyzer = GapAnalyzer()
