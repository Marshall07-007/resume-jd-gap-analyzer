import axios from 'axios';
import {
  ResumeUploadResponse,
  StructuredResume,
  AnalysisResult,
  RoleSkillMap,
  BulletRewriteResponse,
} from '../types';

const API_BASE = '/api';

export const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Upload resume file (PDF/DOCX)
  async uploadResume(file: File): Promise<ResumeUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await apiClient.post<ResumeUploadResponse>('/resume/upload', formData, {
      headers: {
        'Content-Type': undefined,
      },
    });
    return res.data;
  },

  // Parse raw text resume
  async parseResumeText(raw_text: string): Promise<StructuredResume> {
    const res = await apiClient.post<StructuredResume>('/resume/parse', { raw_text });
    return res.data;
  },

  // Execute gap analysis
  async analyzeGap(payload: {
    resume_structured?: StructuredResume;
    resume_text?: string;
    jd_text: string;
    target_role_category?: string;
  }): Promise<AnalysisResult> {
    const res = await apiClient.post<AnalysisResult>('/analyze', payload);
    return res.data;
  },

  // Get curated roles
  async getRoles(): Promise<RoleSkillMap[]> {
    const res = await apiClient.get<RoleSkillMap[]>('/roles');
    return res.data;
  },

  // Bullet rewrite stretch feature
  async rewriteBullet(original_bullet: string, role_context: string = 'Software Engineer'): Promise<BulletRewriteResponse> {
    const res = await apiClient.post<BulletRewriteResponse>('/rewrite-bullet', {
      original_bullet,
      role_context,
    });
    return res.data;
  },

  // Analysis history
  async getHistory(): Promise<AnalysisResult[]> {
    const res = await apiClient.get<AnalysisResult[]>('/analyses');
    return res.data;
  },

  // Health check
  async checkHealth(): Promise<{ status: string }> {
    const res = await apiClient.get<{ status: string }>('/health');
    return res.data;
  },
};
