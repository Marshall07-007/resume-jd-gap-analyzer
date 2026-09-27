from typing import List, Dict, Tuple
from app.schemas.analysis import SkillGapItem, ScoreBreakdown
from app.schemas.job_description import JDParsed
from app.analyzers.skill_normalizer import skill_normalizer


class TransparentScoringEngine:
    """
    Transparent, explainable scoring engine.
    Weights:
      - Required skill coverage: 60%
      - Preferred skill coverage: 20%
      - Role skill-map alignment: 20%
    """
    WEIGHT_REQUIRED = 0.60
    WEIGHT_PREFERRED = 0.20
    WEIGHT_ROLE = 0.20

    def calculate_score(
        self,
        matched: List[SkillGapItem],
        partial: List[SkillGapItem],
        missing: List[SkillGapItem],
        jd: JDParsed,
        role_info: Dict,
    ) -> Tuple[int, ScoreBreakdown]:
        # Group items by requirement source
        jd_req_skills = {skill_normalizer.normalize(s).lower() for s in jd.required_skills if s}
        jd_pref_skills = {skill_normalizer.normalize(s).lower() for s in jd.preferred_skills if s}
        role_core_skills = {skill_normalizer.normalize(s).lower() for s in role_info.get("core_skills", [])}

        # 1. Required Skills Score
        req_score = self._calc_group_coverage(jd_req_skills, matched, partial)

        # 2. Preferred Skills Score
        if jd_pref_skills:
            pref_score = self._calc_group_coverage(jd_pref_skills, matched, partial)
        else:
            # If no preferred skills in JD, grant full credit or fallback to required
            pref_score = req_score

        # 3. Role Skill Map Alignment Score
        role_score = self._calc_group_coverage(role_core_skills, matched, partial)

        # 4. Overall Weighted Score
        overall = (
            (req_score * self.WEIGHT_REQUIRED) +
            (pref_score * self.WEIGHT_PREFERRED) +
            (role_score * self.WEIGHT_ROLE)
        )

        overall_clamped = max(0, min(100, int(round(overall))))

        breakdown = ScoreBreakdown(
            required_skills=round(req_score, 1),
            preferred_skills=round(pref_score, 1),
            role_alignment=round(role_score, 1),
            overall_match=float(overall_clamped),
        )

        return overall_clamped, breakdown

    def _calc_group_coverage(
        self, target_group: set, matched: List[SkillGapItem], partial: List[SkillGapItem]
    ) -> float:
        if not target_group:
            return 100.0

        earned_points = 0.0
        total_possible = float(len(target_group))

        matched_set = {m.skill.lower() for m in matched}
        partial_set = {p.skill.lower() for p in partial}

        for item in target_group:
            if item in matched_set:
                earned_points += 1.0
            elif item in partial_set:
                earned_points += 0.5

        coverage_pct = (earned_points / total_possible) * 100.0
        return max(0.0, min(100.0, coverage_pct))


scoring_engine = TransparentScoringEngine()
