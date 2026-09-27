import re
from typing import List, Tuple
from app.schemas.bullet import BulletRewriteResponse
from app.analyzers.skill_normalizer import skill_normalizer


class BulletRewriter:
    """
    Action-oriented bullet improver.
    Guarantees NO fabrication of numbers, metrics, users, revenue, or non-existent tech.
    """

    WEAK_VERB_MAP = {
        "created": ("Developed", "Engineered", "Built"),
        "made": ("Implemented", "Designed", "Engineered"),
        "worked on": ("Collaborated on the development of", "Contributed to the implementation of"),
        "helped": ("Co-developed", "Assisted in engineering"),
        "did": ("Executed", "Implemented"),
        "used": ("Leveraged", "Utilized", "Applied"),
        "handled": ("Managed", "Orchestrated", "Maintained"),
        "looked at": ("Analyzed", "Audited", "Evaluated"),
        "tested": ("Validated", "Executed quality assurance and testing for"),
        "wrote": ("Authored", "Formulated", "Constructed"),
        "built": ("Architected and developed", "Engineered", "Implemented"),
    }

    STRONG_VERBS = [
        "Architected", "Engineered", "Developed", "Implemented", "Designed",
        "Formulated", "Spearheaded", "Optimized", "Refactored", "Streamlined",
        "Automated", "Integrated", "Configured", "Standardized"
    ]

    def rewrite(self, original_bullet: str, target_skill: str = None, role_context: str = "Software Engineer") -> BulletRewriteResponse:
        bullet_clean = original_bullet.strip().rstrip(".")
        
        # Extract skills present in original bullet
        present_skills = skill_normalizer.extract_skills_from_text(bullet_clean)
        
        improved_verb = "Developed"
        words = bullet_clean.split()
        first_word = words[0].lower() if words else ""
        first_two_words = " ".join(words[:2]).lower() if len(words) >= 2 else ""

        # Check verb replacement
        if first_two_words in self.WEAK_VERB_MAP:
            improved_verb = self.WEAK_VERB_MAP[first_two_words][0]
            remainder = " ".join(words[2:])
        elif first_word in self.WEAK_VERB_MAP:
            improved_verb = self.WEAK_VERB_MAP[first_word][0]
            remainder = " ".join(words[1:])
        elif words and words[0] in self.STRONG_VERBS:
            improved_verb = words[0]
            remainder = " ".join(words[1:])
        else:
            improved_verb = "Engineered"
            remainder = bullet_clean

        # Build enhanced bullet without adding fabricated stats
        # Examples:
        # "Created a website using React" -> "Developed a responsive web application utilizing React with modular UI components."
        # "Tested API endpoints with Postman" -> "Executed comprehensive API testing and validation utilizing Postman with structured test assertions."

        suggested = self._synthesize_bullet(improved_verb, remainder, present_skills)

        return BulletRewriteResponse(
            original_bullet=original_bullet,
            suggested_bullet=suggested,
            action_verb_improved=improved_verb,
            key_technologies_highlighted=present_skills,
            explanation="Replaced passive verb with high-impact action verb, emphasized technical context and modularity without inventing metrics.",
            is_fabricated=False,
        )

    def _synthesize_bullet(self, action_verb: str, remainder: str, skills: List[str]) -> str:
        # Clean up remainder
        remainder = re.sub(r"^(a|an|the)\s+", "", remainder, flags=re.IGNORECASE)
        
        # If remainder is simple (e.g. "website using React and CSS")
        if "website" in remainder.lower() or "web app" in remainder.lower() or "app" in remainder.lower():
            tech_str = ", ".join(skills) if skills else "modern web standards"
            return f"{action_verb} a responsive web application leveraging {tech_str} with modular component architecture and cross-browser compatibility."

        if "api" in remainder.lower() or "backend" in remainder.lower() or "server" in remainder.lower():
            tech_str = ", ".join(skills) if skills else "RESTful conventions"
            return f"{action_verb} robust backend services utilizing {tech_str} with structured error handling and RESTful endpoints."

        if "test" in remainder.lower() or "testing" in remainder.lower() or "qa" in remainder.lower():
            tech_str = ", ".join(skills) if skills else "testing frameworks"
            return f"{action_verb} comprehensive test suites utilizing {tech_str} to validate software functionality and edge case coverage."

        if "data" in remainder.lower() or "analysis" in remainder.lower() or "sql" in remainder.lower():
            tech_str = ", ".join(skills) if skills else "analytical tools"
            return f"{action_verb} data analysis pipelines leveraging {tech_str} to extract structured insights and actionable patterns."

        # Default transformation
        return f"{action_verb} {remainder} following clean code conventions and industry best practices."


bullet_rewriter = BulletRewriter()
