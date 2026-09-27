export interface PersonalDetails {
  name?: string;
  email?: string;
  phone?: string;
  linkedin?: string;
  github?: string;
}

export interface ProjectItem {
  title: string;
  description: string;
  technologies: string[];
  evidence: string;
}

export interface EducationItem {
  degree: string;
  field?: string;
  institution: string;
  year?: string;
}

export interface ExperienceItem {
  role: string;
  company: string;
  duration?: string;
  responsibilities: string[];
  technologies: string[];
}

export interface StructuredResume {
  personal?: PersonalDetails;
  skills: string[];
  projects: ProjectItem[];
  education: EducationItem[];
  experience: ExperienceItem[];
  certifications: { name: string; issuer?: string; year?: string }[];
  raw_text?: string;
}

export interface ResumeUploadResponse {
  file_name: string;
  file_type: string;
  file_size_bytes: number;
  structured: StructuredResume;
  message: string;
}

export interface JDParsed {
  role: string;
  company?: string;
  required_skills: string[];
  preferred_skills: string[];
  tools: string[];
  responsibilities: string[];
  keywords: string[];
  raw_text?: string;
}

export type SkillStatus = 'matched' | 'partial' | 'missing' | 'bonus';

export interface SkillGapItem {
  skill: string;
  status: SkillStatus;
  resume_evidence: string;
  jd_evidence: string;
  source: string;
  category?: string;
  explanation?: string;
}

export interface ScoreBreakdown {
  required_skills: number;
  preferred_skills: number;
  role_alignment: number;
  overall_match: number;
}

export type RecommendationSourceType = 'JD_REQUIRED' | 'JD_PREFERRED' | 'ROLE_SKILL_MAP';

export interface RecommendationItem {
  id: number;
  suggestion: string;
  reason: string;
  source_type: RecommendationSourceType;
  source_text: string;
  priority: 'high' | 'medium' | 'low';
  actionable_steps: string[];
}

export interface AnalysisResult {
  overall_score: number;
  score_breakdown: ScoreBreakdown;
  matched_skills: SkillGapItem[];
  partial_skills: SkillGapItem[];
  missing_skills: SkillGapItem[];
  bonus_skills: SkillGapItem[];
  gap_table: SkillGapItem[];
  recommendations: RecommendationItem[];
  detected_role: string;
  resume_summary: StructuredResume;
  jd_summary: JDParsed;
  created_at?: string;
}

export interface BulletRewriteResponse {
  original_bullet: string;
  suggested_bullet: string;
  action_verb_improved: string;
  key_technologies_highlighted: string[];
  explanation: string;
  is_fabricated: boolean;
}

export interface RoleSkillMap {
  id: string;
  title: string;
  category: string;
  keywords: string[];
  core_skills: string[];
  recommended_actions: Record<string, string>;
}
