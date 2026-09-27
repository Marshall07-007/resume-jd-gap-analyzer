import React from 'react';
import { ArrowRight, Loader2, Trash2, Filter } from 'lucide-react';

interface JDInputProps {
  jdText: string;
  onJdTextChange: (text: string) => void;
  targetRole: string;
  onTargetRoleChange: (role: string) => void;
  onAnalyze: () => void;
  loading: boolean;
  canAnalyze: boolean;
}

export const JDInput: React.FC<JDInputProps> = ({
  jdText,
  onJdTextChange,
  targetRole,
  onTargetRoleChange,
  onAnalyze,
  loading,
  canAnalyze,
}) => {
  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-4">
        <div>
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <span className="flex items-center justify-center w-6 h-6 rounded-md bg-indigo-100 text-indigo-700 text-xs font-bold">2</span>
            Paste Job Description
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">Target job requirements, skills, and qualifications</p>
        </div>

        {/* Role Target Filter */}
        <div className="flex items-center gap-1.5">
          <label className="text-xs font-medium text-slate-500 flex items-center gap-1">
            <Filter className="w-3 h-3 text-slate-400" />
            <span className="hidden sm:inline">Role Corpus:</span>
          </label>
          <select
            value={targetRole}
            onChange={(e) => onTargetRoleChange(e.target.value)}
            className="text-xs font-semibold bg-slate-100 border border-slate-200 text-slate-700 rounded-lg px-2.5 py-1 focus:outline-none focus:ring-1 focus:ring-indigo-500"
          >
            <option value="">Auto-Detect Category</option>
            <option value="frontend">Frontend Developer</option>
            <option value="data">Data Analyst</option>
            <option value="qa">QA Engineer</option>
            <option value="support">Technical Support</option>
          </select>
        </div>
      </div>

      {/* Main Textarea */}
      <div className="flex-1 flex flex-col relative">
        <textarea
          value={jdText}
          onChange={(e) => onJdTextChange(e.target.value)}
          placeholder="Paste the complete job description here (Role title, required skills, preferred qualifications, responsibilities)..."
          className="w-full flex-1 min-h-[220px] p-4 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent text-xs text-slate-800 placeholder:text-slate-400 font-sans leading-relaxed bg-slate-50/50 resize-none transition-all"
        />

        {/* Bottom bar inside textarea card */}
        <div className="flex items-center justify-between pt-2.5 px-1">
          <span className="text-xs text-slate-400 font-mono">
            {jdText.length} characters
          </span>

          {jdText && (
            <button
              type="button"
              onClick={() => onJdTextChange('')}
              className="text-xs text-rose-500 hover:text-rose-700 flex items-center gap-1 transition-colors cursor-pointer"
            >
              <Trash2 className="w-3.5 h-3.5" />
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Primary Analyze Action Button */}
      <div className="mt-4 pt-3 border-t border-slate-100">
        <button
          type="button"
          onClick={onAnalyze}
          disabled={!canAnalyze || loading}
          className={`w-full py-3 px-4 rounded-xl font-bold text-sm shadow-md transition-all flex items-center justify-center space-x-2 ${
            canAnalyze && !loading
              ? 'bg-gradient-to-r from-sky-600 to-indigo-600 hover:from-sky-700 hover:to-indigo-700 text-white shadow-sky-500/20 active:scale-[0.99] cursor-pointer'
              : 'bg-slate-200 text-slate-400 cursor-not-allowed shadow-none'
          }`}
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin text-white" />
              <span>Analyzing Resume ↔ JD Gap...</span>
            </>
          ) : (
            <>
              <span>Analyze Resume</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </div>
    </div>
  );
};
