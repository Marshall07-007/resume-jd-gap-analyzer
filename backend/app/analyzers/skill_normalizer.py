import json
import os
import re
from typing import Dict, List, Optional, Set, Tuple
from rapidfuzz import fuzz, process


class SkillNormalizer:
    def __init__(self, alias_file_path: Optional[str] = None):
        if alias_file_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            alias_file_path = os.path.join(base_dir, "data", "skill_aliases.json")
        
        self.aliases: Dict[str, str] = {}
        self.parent_relations: Dict[str, List[str]] = {}
        self._canonical_skills: Set[str] = set()

        if os.path.exists(alias_file_path):
            with open(alias_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.aliases = {k.lower().strip(): v for k, v in data.get("aliases", {}).items()}
                self.parent_relations = data.get("parent_relations", {})
                self._canonical_skills = set(self.aliases.values())

    def normalize(self, skill_raw: str) -> str:
        """Normalize a skill name into its canonical form."""
        if not skill_raw:
            return ""
        
        cleaned = skill_raw.strip().lower()
        
        # 1. Exact alias lookup
        if cleaned in self.aliases:
            return self.aliases[cleaned]
        
        # 2. Strip special punctuation (dots, hyphens)
        cleaned_no_punct = re.sub(r"[^\w\s]", "", cleaned)
        if cleaned_no_punct in self.aliases:
            return self.aliases[cleaned_no_punct]
        
        # 3. Fuzzy matching against known aliases for typos
        if self.aliases:
            match = process.extractOne(cleaned, self.aliases.keys(), scorer=fuzz.ratio, score_cutoff=88)
            if match:
                matched_key = match[0]
                return self.aliases[matched_key]
        
        # Fallback to Title Cased original
        return skill_raw.strip()

    def extract_skills_from_text(self, text: str) -> List[str]:
        """Extract and normalize all known skills found within a text segment."""
        if not text:
            return []
        
        found_skills: Set[str] = set()
        text_lower = f" {text.lower()} "

        # Sort alias keys by length descending to match multi-word phrases first (e.g. "responsive design", "rest api")
        sorted_keys = sorted(self.aliases.keys(), key=lambda k: len(k), reverse=True)
        
        for key in sorted_keys:
            # Word boundary search
            pattern = r"(?:^|[\s,;./()\-\[\]])" + re.escape(key) + r"(?:$|[\s,;./()\-\[\]])"
            if re.search(pattern, text_lower):
                canonical = self.aliases[key]
                found_skills.add(canonical)
                # Remove matched slice to avoid sub-match collisions if necessary
        
        return sorted(list(found_skills))

    def is_related(self, req_skill: str, resume_skill: str) -> Tuple[bool, str]:
        """
        Check if resume_skill is related to req_skill (e.g. JavaScript relates to React).
        Returns (is_related, explanation).
        """
        req_norm = self.normalize(req_skill)
        res_norm = self.normalize(resume_skill)

        if req_norm.lower() == res_norm.lower():
            return True, "Exact match"

        # Check parent relations
        parents_of_req = self.parent_relations.get(req_norm, [])
        if any(p.lower() == res_norm.lower() for p in parents_of_req):
            return True, f"Found foundational skill '{res_norm}', which is closely related to required '{req_norm}'."

        parents_of_res = self.parent_relations.get(res_norm, [])
        if any(p.lower() == req_norm.lower() for p in parents_of_res):
            return True, f"Found specialized skill '{res_norm}', which encompasses required '{req_norm}'."

        return False, ""


# Singleton instance
skill_normalizer = SkillNormalizer()
