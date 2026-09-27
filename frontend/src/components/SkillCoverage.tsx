import React from 'react';
import { CheckCircle, Clock, XCircle, PlusCircle } from 'lucide-react';
import { SkillGapItem } from '../types';

interface SkillCoverageProps {
  matched: SkillGapItem[];
  partial: SkillGapItem[];
  missing: SkillGapItem[];
  bonus: SkillGapItem[];
  selectedFilter: string;
  onFilterChange: (filter: string) => void;
}

export const SkillCoverage: React.FC<SkillCoverageProps> = ({
  matched,
  partial,
  missing,
  bonus,
  selectedFilter,
  onFilterChange,
}) => {
  return (
    <div className="space-y-4">
      {/* Category Pills Filter Bar */}
      <div className="flex flex-wrap items-center gap-2">
        <button
          onClick={() => onFilterChange('all')}
          className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all cursor-pointer ${
            selectedFilter === 'all'
              ? 'bg-slate-900 text-white shadow-sm'
              : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-50'
          }`}
        >
          All Skills ({matched.length + partial.length + missing.length + bonus.length})
        </button>

        <button
          onClick={() => onFilterChange('matched')}
          className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer ${
            selectedFilter === 'matched'
              ? 'bg-emerald-600 text-white shadow-sm'
              : 'bg-emerald-50 text-emerald-700 border border-emerald-200 hover:bg-emerald-100'
          }`}
        >
          <CheckCircle className="w-3.5 h-3.5" />
          <span>Matched ({matched.length})</span>
        </button>

        <button
          onClick={() => onFilterChange('partial')}
          className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer ${
            selectedFilter === 'partial'
              ? 'bg-amber-600 text-white shadow-sm'
              : 'bg-amber-50 text-amber-800 border border-amber-200 hover:bg-amber-100'
          }`}
        >
          <Clock className="w-3.5 h-3.5" />
          <span>Partial ({partial.length})</span>
        </button>

        <button
          onClick={() => onFilterChange('missing')}
          className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer ${
            selectedFilter === 'missing'
              ? 'bg-rose-600 text-white shadow-sm'
              : 'bg-rose-50 text-rose-700 border border-rose-200 hover:bg-rose-100'
          }`}
        >
          <XCircle className="w-3.5 h-3.5" />
          <span>Missing ({missing.length})</span>
        </button>

        {bonus.length > 0 && (
          <button
            onClick={() => onFilterChange('bonus')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold flex items-center gap-1.5 transition-all cursor-pointer ${
              selectedFilter === 'bonus'
                ? 'bg-purple-600 text-white shadow-sm'
                : 'bg-purple-50 text-purple-700 border border-purple-200 hover:bg-purple-100'
            }`}
          >
            <PlusCircle className="w-3.5 h-3.5" />
            <span>Bonus ({bonus.length})</span>
          </button>
        )}
      </div>

      {/* Grid of Highlighted Skill Badges */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        {/* Matched Summary */}
        {(selectedFilter === 'all' || selectedFilter === 'matched') &&
          matched.map((item, idx) => (
            <div
              key={`m-${idx}`}
              className="p-3.5 rounded-xl bg-white border border-emerald-100 shadow-xs hover:border-emerald-300 transition-all space-y-1.5"
            >
              <div className="flex items-center justify-between">
                <span className="font-bold text-xs text-slate-900 flex items-center gap-1.5">
                  <CheckCircle className="w-4 h-4 text-emerald-600 shrink-0" />
                  {item.skill}
                </span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 uppercase tracking-wider">
                  Matched
                </span>
              </div>
              <p className="text-[11px] text-slate-500 leading-tight">
                {item.resume_evidence}
              </p>
            </div>
          ))}

        {/* Partial Summary */}
        {(selectedFilter === 'all' || selectedFilter === 'partial') &&
          partial.map((item, idx) => (
            <div
              key={`p-${idx}`}
              className="p-3.5 rounded-xl bg-white border border-amber-200 shadow-xs hover:border-amber-400 transition-all space-y-1.5"
            >
              <div className="flex items-center justify-between">
                <span className="font-bold text-xs text-slate-900 flex items-center gap-1.5">
                  <Clock className="w-4 h-4 text-amber-500 shrink-0" />
                  {item.skill}
                </span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-100 text-amber-800 uppercase tracking-wider">
                  Partial
                </span>
              </div>
              <p className="text-[11px] text-amber-900 font-medium leading-tight">
                {item.explanation || 'Related skill present, but specific technology not explicitly proven.'}
              </p>
              <p className="text-[10px] text-slate-500">
                Evidence: {item.resume_evidence}
              </p>
            </div>
          ))}

        {/* Missing Summary */}
        {(selectedFilter === 'all' || selectedFilter === 'missing') &&
          missing.map((item, idx) => (
            <div
              key={`x-${idx}`}
              className="p-3.5 rounded-xl bg-white border border-rose-100 shadow-xs hover:border-rose-300 transition-all space-y-1.5"
            >
              <div className="flex items-center justify-between">
                <span className="font-bold text-xs text-slate-900 flex items-center gap-1.5">
                  <XCircle className="w-4 h-4 text-rose-500 shrink-0" />
                  {item.skill}
                </span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-100 text-rose-800 uppercase tracking-wider">
                  Missing
                </span>
              </div>
              <p className="text-[11px] text-rose-900/80 leading-tight">
                Source: {item.source} ({item.jd_evidence})
              </p>
            </div>
          ))}

        {/* Bonus Summary */}
        {(selectedFilter === 'all' || selectedFilter === 'bonus') &&
          bonus.map((item, idx) => (
            <div
              key={`b-${idx}`}
              className="p-3.5 rounded-xl bg-white border border-purple-100 shadow-xs hover:border-purple-300 transition-all space-y-1.5"
            >
              <div className="flex items-center justify-between">
                <span className="font-bold text-xs text-slate-900 flex items-center gap-1.5">
                  <PlusCircle className="w-4 h-4 text-purple-600 shrink-0" />
                  {item.skill}
                </span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-purple-100 text-purple-800 uppercase tracking-wider">
                  Bonus Strength
                </span>
              </div>
              <p className="text-[11px] text-slate-500 leading-tight">
                {item.resume_evidence}
              </p>
            </div>
          ))}
      </div>
    </div>
  );
};
