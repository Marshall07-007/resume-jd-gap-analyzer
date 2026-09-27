import React, { useState } from 'react';
import { Info, ChevronDown, ChevronUp, Layers } from 'lucide-react';
import { ScoreBreakdown } from '../types';

interface ScoreCardProps {
  overallScore: number;
  breakdown: ScoreBreakdown;
  detectedRole: string;
}

export const ScoreCard: React.FC<ScoreCardProps> = ({
  overallScore,
  breakdown,
  detectedRole,
}) => {
  const [showFormula, setShowFormula] = useState(false);

  // Dynamic color palette based on score
  const getScoreTheme = (score: number) => {
    if (score >= 75) {
      return {
        bg: 'from-emerald-500 to-teal-600',
        text: 'text-emerald-700',
        border: 'border-emerald-200',
        badge: 'bg-emerald-100 text-emerald-800',
        label: 'Strong Match',
      };
    }
    if (score >= 50) {
      return {
        bg: 'from-amber-500 to-orange-600',
        text: 'text-amber-700',
        border: 'border-amber-200',
        badge: 'bg-amber-100 text-amber-800',
        label: 'Moderate Alignment',
      };
    }
    return {
      bg: 'from-rose-500 to-red-600',
      text: 'text-rose-700',
      border: 'border-rose-200',
      badge: 'bg-rose-100 text-rose-800',
      label: 'Significant Skill Gaps',
    };
  };

  const theme = getScoreTheme(overallScore);

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 pb-6 border-b border-slate-100">
        {/* Left Side: Score & Role */}
        <div className="flex items-center space-x-6">
          {/* Large Hero Score Badge */}
          <div className={`w-28 h-28 rounded-2xl bg-gradient-to-br ${theme.bg} p-1 shadow-lg shadow-sky-500/10 flex items-center justify-center text-white shrink-0`}>
            <div className="w-full h-full rounded-xl bg-white/10 backdrop-blur-xs flex flex-col items-center justify-center p-2 text-center">
              <span className="text-3xl sm:text-4xl font-black tracking-tight">{overallScore}</span>
              <span className="text-[11px] font-semibold uppercase tracking-wider opacity-90">/ 100</span>
            </div>
          </div>

          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${theme.badge}`}>
                {theme.label}
              </span>
              <span className="text-xs font-medium text-slate-500">•</span>
              <span className="text-xs font-medium text-slate-600">Target Role: <strong className="text-slate-900">{detectedRole}</strong></span>
            </div>
            <h1 className="text-xl sm:text-2xl font-extrabold text-slate-900 tracking-tight">
              Resume ↔ JD Compatibility
            </h1>
            <p className="text-xs sm:text-sm text-slate-500 mt-1 max-w-lg">
              Deterministic & semantic comparison across required JD competencies, preferred tools, and curated role skill expectations.
            </p>
          </div>
        </div>

        {/* Right Side Formula Toggle */}
        <button
          type="button"
          onClick={() => setShowFormula(!showFormula)}
          className="self-start md:self-center px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
        >
          <Info className="w-4 h-4 text-sky-600" />
          <span>Explainable Formula</span>
          {showFormula ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
        </button>
      </div>

      {/* Score Breakdown Progress Bars */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 pt-6">
        {/* Required Skills Coverage */}
        <div className="space-y-2 p-4 rounded-xl bg-slate-50 border border-slate-100">
          <div className="flex justify-between items-center text-xs">
            <span className="font-bold text-slate-700">Required Skills</span>
            <span className="font-extrabold text-sky-700">{breakdown.required_skills}%</span>
          </div>
          <div className="w-full h-2.5 bg-slate-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-sky-600 rounded-full transition-all duration-700"
              style={{ width: `${Math.min(100, breakdown.required_skills)}%` }}
            />
          </div>
          <p className="text-[11px] text-slate-500">Weight: 60% of overall score</p>
        </div>

        {/* Preferred Skills Coverage */}
        <div className="space-y-2 p-4 rounded-xl bg-slate-50 border border-slate-100">
          <div className="flex justify-between items-center text-xs">
            <span className="font-bold text-slate-700">Preferred Skills</span>
            <span className="font-extrabold text-indigo-700">{breakdown.preferred_skills}%</span>
          </div>
          <div className="w-full h-2.5 bg-slate-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-indigo-600 rounded-full transition-all duration-700"
              style={{ width: `${Math.min(100, breakdown.preferred_skills)}%` }}
            />
          </div>
          <p className="text-[11px] text-slate-500">Weight: 20% of overall score</p>
        </div>

        {/* Role Alignment */}
        <div className="space-y-2 p-4 rounded-xl bg-slate-50 border border-slate-100">
          <div className="flex justify-between items-center text-xs">
            <span className="font-bold text-slate-700">Role Alignment</span>
            <span className="font-extrabold text-teal-700">{breakdown.role_alignment}%</span>
          </div>
          <div className="w-full h-2.5 bg-slate-200 rounded-full overflow-hidden">
            <div
              className="h-full bg-teal-600 rounded-full transition-all duration-700"
              style={{ width: `${Math.min(100, breakdown.role_alignment)}%` }}
            />
          </div>
          <p className="text-[11px] text-slate-500">Weight: 20% of overall score</p>
        </div>
      </div>

      {/* Formula Explanation Collapsible */}
      {showFormula && (
        <div className="mt-6 p-4 rounded-xl bg-sky-50/70 border border-sky-200 text-xs text-slate-700 space-y-2 animate-in fade-in">
          <p className="font-bold text-sky-900 flex items-center gap-1.5">
            <Layers className="w-4 h-4 text-sky-700" />
            Deterministic Scoring Methodology:
          </p>
          <ul className="list-disc list-inside space-y-1 text-slate-600">
            <li><strong>Matched items</strong> receive 100% full credit (1.0 weight).</li>
            <li><strong>Partial items</strong> (related foundational skills present, e.g. JS for React) receive 50% credit (0.5 weight).</li>
            <li><strong>Missing items</strong> receive 0% credit (0.0 weight).</li>
            <li>Composite Score = <code className="font-mono bg-white px-1.5 py-0.5 rounded border border-sky-200 text-sky-800">
              (Required × 0.60) + (Preferred × 0.20) + (Role Map Alignment × 0.20)
            </code></li>
          </ul>
        </div>
      )}
    </div>
  );
};
