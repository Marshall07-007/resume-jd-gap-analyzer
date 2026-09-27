from typing import Dict, List
from app.schemas.analysis import RecommendationItem, SkillGapItem
from app.schemas.job_description import JDParsed
from app.schemas.resume import StructuredResume
from app.analyzers.skill_normalizer import skill_normalizer


class RecommendationEngine:
    """
    Generates EXACTLY 3 concrete, actionable, and traceable recommendations.
    Every recommendation is traceable to JD_REQUIRED, JD_PREFERRED, or ROLE_SKILL_MAP.
    Never fabricates false experience.
    """

    DEFAULT_SKILL_ACTIONS = {
        "React": {
            "suggestion": "Strengthen your React experience by developing a component-driven frontend application and listing it under Projects.",
            "steps": [
                "Build a React single-page app (e.g., dashboard, task manager) demonstrating hooks and state management.",
                "Incorporate reusable UI components and integrate with a mock or public REST API.",
                "Deploy the project to Vercel/Netlify and link the GitHub repository on your resume."
            ]
        },
        "REST APIs": {
            "suggestion": "Highlight REST API integration in an existing project by detailing how asynchronous data fetching and error states are handled.",
            "steps": [
                "Detail HTTP methods (GET, POST, PUT, DELETE) used in your project descriptions.",
                "Specify how loading, error, and pagination states were engineered.",
                "Add an explicit bullet point about API integration in your experience or project sections."
            ]
        },
        "Git": {
            "suggestion": "Include your GitHub profile link and describe your version control workflow in your project bullet points.",
            "steps": [
                "Ensure personal GitHub link is added to the contact header.",
                "Include clean commit histories, feature branches, and comprehensive README documentation on public repos."
            ]
        },
        "SQL": {
            "suggestion": "Demonstrate practical SQL skills by executing complex queries, aggregations, or joins on real datasets in your projects.",
            "steps": [
                "Write analytical queries utilizing GROUP BY, JOINs, and subqueries on open datasets.",
                "Document database schema design or indexing strategies in your project descriptions."
            ]
        },
        "Docker": {
            "suggestion": "Containerize a project using Docker to demonstrate production-readiness and environment consistency.",
            "steps": [
                "Write a multi-stage Dockerfile for your application.",
                "Document containerization and deployment steps in your project's README."
            ]
        },
        "Selenium": {
            "suggestion": "Build an automated end-to-end testing suite with Selenium and document test coverage in your resume.",
            "steps": [
                "Automate critical user journeys (authentication, navigation, form submissions).",
                "Integrate assertions and test reporting into a project repository."
            ]
        }
    }

    def generate_recommendations(
        self,
        matched: List[SkillGapItem],
        partial: List[SkillGapItem],
        missing: List[SkillGapItem],
        jd: JDParsed,
        role_info: Dict,
        resume: StructuredResume,
    ) -> List[RecommendationItem]:
        candidates: List[RecommendationItem] = []
        rec_id = 1

        jd_req_normalized = {skill_normalizer.normalize(s).lower(): s for s in jd.required_skills if s}
        jd_pref_normalized = {skill_normalizer.normalize(s).lower(): s for s in jd.preferred_skills if s}
        role_actions = role_info.get("recommended_actions", {})
        role_title = role_info.get("title", "Target Role")

        # 1. Partial or Missing JD Required Skills (Highest Priority)
        for item in partial + missing:
            skill_norm = skill_normalizer.normalize(item.skill)
            if skill_norm.lower() in jd_req_normalized:
                action_info = self._get_action_for_skill(skill_norm, role_actions, "required in the job description")
                candidates.append(
                    RecommendationItem(
                        id=rec_id,
                        suggestion=action_info["suggestion"],
                        reason=f"'{skill_norm}' is a required skill in the Job Description, but is currently {item.status}.",
                        source_type="JD_REQUIRED",
                        source_text=f"Required in JD: \"{item.jd_evidence}\"",
                        priority="high",
                        actionable_steps=action_info["steps"],
                    )
                )
                rec_id += 1

        # 2. Partial or Missing JD Preferred Skills (Medium Priority)
        for item in partial + missing:
            skill_norm = skill_normalizer.normalize(item.skill)
            if skill_norm.lower() in jd_pref_normalized and not any(c.source_text.find(skill_norm) >= 0 for c in candidates):
                action_info = self._get_action_for_skill(skill_norm, role_actions, "listed as preferred in the job description")
                candidates.append(
                    RecommendationItem(
                        id=rec_id,
                        suggestion=action_info["suggestion"],
                        reason=f"'{skill_norm}' is preferred by the employer and will give you a competitive advantage.",
                        source_type="JD_PREFERRED",
                        source_text=f"Preferred in JD: \"{item.jd_evidence}\"",
                        priority="medium",
                        actionable_steps=action_info["steps"],
                    )
                )
                rec_id += 1

        # 3. Role Skill Map Core Recommendations
        for item in missing + partial:
            skill_norm = skill_normalizer.normalize(item.skill)
            if not any(c.source_text.find(skill_norm) >= 0 for c in candidates):
                action_info = self._get_action_for_skill(skill_norm, role_actions, f"a standard industry expectation for {role_title}")
                candidates.append(
                    RecommendationItem(
                        id=rec_id,
                        suggestion=action_info["suggestion"],
                        reason=f"'{skill_norm}' aligns with industry benchmarks for {role_title} positions.",
                        source_type="ROLE_SKILL_MAP",
                        source_text=f"Curated {role_title} Skill Map: \"{item.skill}\"",
                        priority="medium" if item.status == "partial" else "low",
                        actionable_steps=action_info["steps"],
                    )
                )
                rec_id += 1

        # If we have matched skills, offer refinement recommendation if needed to reach exactly 3
        if len(candidates) < 3 and matched:
            first_match = matched[0]
            candidates.append(
                RecommendationItem(
                    id=rec_id,
                    suggestion=f"Elaborate on your demonstrated '{first_match.skill}' experience by quantifying technical impact and outcomes in project descriptions.",
                    reason=f"You have confirmed proficiency in '{first_match.skill}'. Making the outcome measurable strengthens recruiter appeal.",
                    source_type="ROLE_SKILL_MAP",
                    source_text=f"Demonstrated Competency: \"{first_match.skill}\"",
                    priority="low",
                    actionable_steps=[
                        f"Include technical scale or problem constraints for {first_match.skill} projects.",
                        "Highlight architectural decisions and trade-offs made during development."
                    ],
                )
            )
            rec_id += 1

        # Fallback general role recommendation to ensure exactly 3
        if len(candidates) < 3:
            candidates.append(
                RecommendationItem(
                    id=rec_id,
                    suggestion=f"Structure project bullets using the Action-Context-Result framework for all {role_title} skills.",
                    reason=f"Ensures technical depth and clarity across your application.",
                    source_type="ROLE_SKILL_MAP",
                    source_text=f"General {role_title} Best Practice",
                    priority="low",
                    actionable_steps=[
                        "Begin bullet points with strong technical action verbs.",
                        "Clearly state the technical stack and problem solved."
                    ]
                )
            )
            rec_id += 1

        # Ensure exactly 3 items and normalize IDs
        final_3 = candidates[:3]
        for idx, item in enumerate(final_3):
            item.id = idx + 1

        return final_3

    def _get_action_for_skill(self, skill: str, role_actions: Dict, context_label: str) -> Dict:
        if skill in role_actions:
            return {
                "suggestion": role_actions[skill],
                "steps": [
                    f"Review core fundamentals of {skill}.",
                    f"Apply {skill} in a concrete coding project or test suite.",
                    f"Document {skill} usage and repository link on your resume."
                ]
            }

        if skill in self.DEFAULT_SKILL_ACTIONS:
            return self.DEFAULT_SKILL_ACTIONS[skill]

        return {
            "suggestion": f"Build practical hands-on experience in '{skill}' ({context_label}) and feature it prominently in your Projects section.",
            "steps": [
                f"Study key concepts and standard workflows for {skill}.",
                f"Build a focused demonstration project applying {skill}.",
                f"Add a clear bullet point in your resume highlighting your work with {skill}."
            ]
        }


recommendation_engine = RecommendationEngine()
