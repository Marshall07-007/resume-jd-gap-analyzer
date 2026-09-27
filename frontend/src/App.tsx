import React, { useState } from 'react';
import { Navbar } from './components/Navbar';
import { ResumeUploader } from './components/ResumeUploader';
import { JDInput } from './components/JDInput';
import { ScoreCard } from './components/ScoreCard';
import { SkillCoverage } from './components/SkillCoverage';
import { SkillTable } from './components/SkillTable';
import { RecommendationCard } from './components/RecommendationCard';
import { BulletSuggestion } from './components/BulletSuggestion';
import { StructuredResume, AnalysisResult } from './types';
import { DEMO_RESUME_TEXT, DEMO_JD_TEXT } from './services/demoData';
import { api } from './services/api';
import { AlertTriangle, Sparkles, FileCheck2 } from 'lucide-react';

export const App: React.FC = () => {
  const [structuredResume, setStructuredResume] = useState<StructuredResume | null>(null);
  const [rawResumeText, setRawResumeText] = useState<string>('');
  const [jdText, setJdText] = useState<string>('');
  const [targetRole, setTargetRole] = useState<string>('');
  
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [skillFilter, setSkillFilter] = useState<string>('all');

  // Load standard Demo Mode matching prompt spec
  const handleLoadDemo = async () => {
    setError(null);
    setRawResumeText(DEMO_RESUME_TEXT);
    setJdText(DEMO_JD_TEXT);
    setTargetRole('frontend');

    try {
      setLoading(true);
      const parsedResume = await api.parseResumeText(DEMO_RESUME_TEXT);
      setStructuredResume(parsedResume);

      // Perform analysis directly for instant Demo experience
      const res = await api.analyzeGap({
        resume_structured: parsedResume,
        resume_text: DEMO_RESUME_TEXT,
        jd_text: DEMO_JD_TEXT,
        target_role_category: 'frontend',
      });
      setAnalysisResult(res);
    } catch (err: any) {
      console.error('Demo error:', err);
      setError('Could not connect to analysis API. Ensure backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setStructuredResume(null);
    setRawResumeText('');
    setJdText('');
    setTargetRole('');
    setAnalysisResult(null);
    setError(null);
    setSkillFilter('all');
  };

  const handleAnalyze = async () => {
    if (!structuredResume && !rawResumeText.trim()) {
      setError('Please upload a resume or paste resume text first.');
      return;
    }
    if (!jdText.trim()) {
      setError('Please paste a job description.');
      return;
    }

    setError(null);
    setLoading(true);

    try {
      const res = await api.analyzeGap({
        resume_structured: structuredResume || undefined,
        resume_text: rawResumeText || structuredResume?.raw_text || '',
        jd_text: jdText,
        target_role_category: targetRole || undefined,
      });
      setAnalysisResult(res);

      // Smooth scroll down to results
      setTimeout(() => {
        const resultsEl = document.getElementById('results-section');
        if (resultsEl) {
          resultsEl.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    } catch (err: any) {
      const msg = err.response?.data?.detail || err.message || 'Failed to complete analysis.';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  const canAnalyze = Boolean(
    (structuredResume !== null || rawResumeText.trim().length > 0) &&
    jdText.trim().length > 0
  );

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans selection:bg-sky-500 selection:text-white">
      {/* Navigation Header */}
      <Navbar
        onLoadDemo={handleLoadDemo}
        onReset={handleReset}
        hasResults={Boolean(analysisResult)}
      />

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Error Banner */}
        {error && (
          <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm font-medium flex items-center justify-between shadow-xs animate-in fade-in">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0" />
              <span>{error}</span>
            </div>
            <button
              onClick={() => setError(null)}
              className="text-xs font-bold text-rose-600 hover:text-rose-900 underline"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Top Hero Banner */}
        <div className="text-center max-w-3xl mx-auto space-y-2 pt-2 pb-1">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-50 border border-sky-200 text-sky-700 text-xs font-bold mb-1">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Structured Document NLP & Role Skill-Map Grounding</span>
          </div>
          <h1 className="text-2xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
            Analyze the Gap Between Your <span className="text-sky-600">Resume</span> & <span className="text-indigo-600">Target Role</span>
          </h1>
          <p className="text-sm text-slate-600">
            Extract structured credentials, identify missing competencies, and receive 3 concrete, 100% traceable recommendations.
          </p>
        </div>

        {/* TWO-PANEL INTERFACE */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 items-stretch">
          {/* Left Panel: Resume Uploader */}
          <div className="h-full">
            <ResumeUploader
              structuredResume={structuredResume}
              onStructuredResumeChange={setStructuredResume}
              rawResumeText={rawResumeText}
              onRawResumeTextChange={setRawResumeText}
            />
          </div>

          {/* Right Panel: Job Description Input */}
          <div className="h-full">
            <JDInput
              jdText={jdText}
              onJdTextChange={setJdText}
              targetRole={targetRole}
              onTargetRoleChange={setTargetRole}
              onAnalyze={handleAnalyze}
              loading={loading}
              canAnalyze={canAnalyze}
            />
          </div>
        </div>

        {/* RESULTS DASHBOARD */}
        {analysisResult && (
          <section id="results-section" className="space-y-8 pt-6 animate-in fade-in duration-300">
            <div className="flex items-center justify-between border-b border-slate-200 pb-3">
              <div className="flex items-center gap-2">
                <FileCheck2 className="w-5 h-5 text-sky-600" />
                <h2 className="text-lg sm:text-xl font-extrabold text-slate-900">
                  Gap Analysis Intelligence Report
                </h2>
              </div>
              <span className="text-xs text-slate-500 font-mono">
                {new Date().toLocaleTimeString()}
              </span>
            </div>

            {/* 1. ScoreCard with Breakdown */}
            <ScoreCard
              overallScore={analysisResult.overall_score}
              breakdown={analysisResult.score_breakdown}
              detectedRole={analysisResult.detected_role}
            />

            {/* 2. Skill Highlights & Badges */}
            <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-4">
              <h3 className="text-base font-bold text-slate-900">
                Extracted Skill Coverage Summary
              </h3>
              <SkillCoverage
                matched={analysisResult.matched_skills}
                partial={analysisResult.partial_skills}
                missing={analysisResult.missing_skills}
                bonus={analysisResult.bonus_skills}
                selectedFilter={skillFilter}
                onFilterChange={setSkillFilter}
              />
            </div>

            {/* 3. Skill Gap Table */}
            <SkillTable items={analysisResult.gap_table} />

            {/* 4. Three Traceable Recommendations */}
            <RecommendationCard recommendations={analysisResult.recommendations} />

            {/* 5. Stretch Feature: Improve Resume Bullet */}
            <BulletSuggestion
              structuredResume={analysisResult.resume_summary}
              detectedRole={analysisResult.detected_role}
            />
          </section>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 mt-12 py-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <p>© 2026 Resume ↔ JD Gap Analyzer — Built with FastAPI, PyMuPDF, python-docx & React</p>
          <p className="font-semibold text-slate-700">Internship Project S-2</p>
        </div>
      </footer>
    </div>
  );
};

export default App;
