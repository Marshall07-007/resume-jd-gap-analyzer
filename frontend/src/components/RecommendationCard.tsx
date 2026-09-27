import React, { useState } from 'react';
import { Lightbulb, ChevronRight, CheckSquare, ShieldCheck, Tag } from 'lucide-react';
import { RecommendationItem, RecommendationSourceType } from '../types';

interface RecommendationCardProps {
  recommendations: RecommendationItem[];
}

export const RecommendationCard: React.FC<RecommendationCardProps> = ({ recommendations }) => {
  const [expandedId, setExpandedId] = useState<number | null>(1);

  const getSourceBadge = (sourceType: RecommendationSourceType) => {
    switch (sourceType) {
      case 'JD_REQUIRED':
        return (
          <span className="px-2.5 py-1 rounded-md text-[11px] font-bold bg-rose-50 text-rose-700 border border-rose-200 flex items-center gap-1">
            <Tag className="w-3 h-3" />
            SOURCE: JD REQUIRED
          </span>
        );
      case 'JD_PREFERRED':
        return (
          <span className="px-2.5 py-1 rounded-md text-[11px] font-bold bg-indigo-50 text-indigo-700 border border-indigo-200 flex items-center gap-1">
            <Tag className="w-3 h-3" />
            SOURCE: JD PREFERRED
          </span>
        );
      case 'ROLE_SKILL_MAP':
        return (
          <span className="px-2.5 py-1 rounded-md text-[11px] font-bold bg-sky-50 text-sky-700 border border-sky-200 flex items-center gap-1">
            <Tag className="w-3 h-3" />
            SOURCE: ROLE SKILL MAP
          </span>
        );
    }
  };

  const getPriorityBadge = (priority: 'high' | 'medium' | 'low') => {
    switch (priority) {
      case 'high':
        return (
          <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full bg-rose-100 text-rose-800">
            High Priority
          </span>
        );
      case 'medium':
        return (
          <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full bg-amber-100 text-amber-800">
            Medium Priority
          </span>
        );
      case 'low':
        return (
          <span className="text-[10px] font-extrabold uppercase px-2 py-0.5 rounded-full bg-slate-100 text-slate-700">
            Optimization
          </span>
        );
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-slate-100">
        <div>
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-amber-500/10 text-amber-600 flex items-center justify-center font-bold">
              <Lightbulb className="w-4 h-4" />
            </div>
            <h2 className="text-base sm:text-lg font-bold text-slate-900">
              3 Traceable Recommendations
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Concrete actions directly grounded in employer requirements and industry standards.
          </p>
        </div>

        <div className="flex items-center gap-1 text-xs text-emerald-700 font-medium bg-emerald-50 px-3 py-1.5 rounded-lg border border-emerald-200">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          <span>100% Traceable Evidence</span>
        </div>
      </div>

      {/* 3 Action Cards */}
      <div className="space-y-4">
        {recommendations.map((rec, idx) => {
          const isExpanded = expandedId === rec.id;
          return (
            <div
              key={rec.id}
              className={`rounded-xl border transition-all duration-200 overflow-hidden ${
                isExpanded
                  ? 'border-sky-300 bg-sky-50/30 shadow-xs'
                  : 'border-slate-200 bg-white hover:border-slate-300'
              }`}
            >
              {/* Header Bar */}
              <div
                onClick={() => setExpandedId(isExpanded ? null : rec.id)}
                className="p-4 sm:p-5 flex items-start sm:items-center justify-between gap-4 cursor-pointer"
              >
                <div className="flex items-start gap-3.5">
                  <span className="flex items-center justify-center w-7 h-7 rounded-full bg-slate-900 text-white text-xs font-bold shrink-0 mt-0.5 sm:mt-0">
                    {idx + 1}
                  </span>
                  <div>
                    <div className="flex flex-wrap items-center gap-2 mb-1">
                      {getSourceBadge(rec.source_type)}
                      {getPriorityBadge(rec.priority)}
                    </div>
                    <h3 className="text-sm font-bold text-slate-900 leading-snug">
                      {rec.suggestion}
                    </h3>
                  </div>
                </div>

                <div className="shrink-0 text-slate-400">
                  <ChevronRight
                    className={`w-5 h-5 transition-transform duration-200 ${
                      isExpanded ? 'rotate-90 text-sky-600' : ''
                    }`}
                  />
                </div>
              </div>

              {/* Expandable Traceability & Action Steps */}
              {isExpanded && (
                <div className="px-5 pb-5 pt-1 space-y-4 border-t border-sky-100 text-xs text-slate-700">
                  {/* Traceable Evidence Box */}
                  <div className="p-3 rounded-lg bg-white border border-sky-200 space-y-1">
                    <span className="font-bold text-sky-900 text-[11px] uppercase tracking-wider block">
                      Grounded Evidence:
                    </span>
                    <blockquote className="italic text-slate-600 font-mono text-[11px] bg-slate-50 p-2 rounded border border-slate-200">
                      {rec.source_text}
                    </blockquote>
                    <p className="text-[11px] text-slate-600 mt-1">
                      <strong>Why this matters:</strong> {rec.reason}
                    </p>
                  </div>

                  {/* Step-by-step checklist */}
                  {rec.actionable_steps && rec.actionable_steps.length > 0 && (
                    <div className="space-y-2">
                      <span className="font-bold text-slate-800 text-[11px] uppercase tracking-wider block">
                        Action Steps:
                      </span>
                      <div className="space-y-1.5">
                        {rec.actionable_steps.map((step, sIdx) => (
                          <div key={sIdx} className="flex items-start gap-2 bg-white/80 p-2 rounded-lg border border-slate-100">
                            <CheckSquare className="w-3.5 h-3.5 text-sky-600 shrink-0 mt-0.5" />
                            <span className="text-slate-700 font-medium">{step}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
