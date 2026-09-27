import json
import os
from typing import Dict, List, Optional, Any
from app.analyzers.skill_normalizer import skill_normalizer


class RoleMatcher:
    def __init__(self, corpus_path: Optional[str] = None):
        if corpus_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            corpus_path = os.path.join(base_dir, "data", "role_skill_maps.json")
        
        self.roles: List[Dict[str, Any]] = []
        if os.path.exists(corpus_path):
            with open(corpus_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.roles = data.get("roles", [])

    def get_all_roles(self) -> List[Dict[str, Any]]:
        return self.roles

    def get_role_by_id_or_category(self, identifier: str) -> Optional[Dict[str, Any]]:
        if not identifier:
            return None
        target = identifier.lower().strip()
        for r in self.roles:
            if r.get("id", "").lower() == target or r.get("category", "").lower() == target or r.get("title", "").lower() == target:
                return r
        return None

    def detect_role(self, jd_text: str, jd_role_title: str = "", extracted_skills: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Detect the most relevant curated role based on JD title, keywords, and skill overlap.
        Defaults to Frontend if no clear match.
        """
        if not self.roles:
            return {
                "id": "frontend",
                "title": "Frontend Developer",
                "category": "Frontend",
                "core_skills": ["HTML", "CSS", "JavaScript", "React", "Git", "REST APIs", "Responsive Design"],
                "recommended_actions": {}
            }

        combined_text = f"{jd_role_title} {jd_text}".lower()
        extracted_skills = extracted_skills or []
        normalized_skills = [skill_normalizer.normalize(s).lower() for s in extracted_skills]

        best_role = self.roles[0]
        highest_score = -1

        for role in self.roles:
            score = 0
            
            # Title keyword matching (high weight)
            for kw in role.get("keywords", []):
                if kw in combined_text:
                    score += 5
            
            # Core skill overlap
            core_skills = [skill_normalizer.normalize(s).lower() for s in role.get("core_skills", [])]
            for s in normalized_skills:
                if s in core_skills:
                    score += 2
            
            if score > highest_score:
                highest_score = score
                best_role = role

        return best_role


role_matcher = RoleMatcher()
