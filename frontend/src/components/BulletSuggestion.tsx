import React, { useState } from 'react';
import {
  Wand2,
  Check,
  X,
  Edit3,
  ShieldAlert,
  Loader2,
  Sparkles
} from 'lucide-react';
import { api } from '../services/api';
import { StructuredResume, BulletRewriteResponse } from '../types';

interface BulletSuggestionProps {
  structuredResume: StructuredResume | null;
  detectedRole: string;
}

export const BulletSuggestion: React.FC<BulletSuggestionProps> = ({
  structuredResume,
  detectedRole,
}) => {
  // Candidate bullets extracted from projects and experience
  const candidateBullets: string[] = [];
  if (structuredResume) {
    for (const p of structuredResume.projects) {
      if (p.description) {
        candidateBullets.push(p.description);
      }
    }
    for (const e of structuredResume.experience) {
      for (const r of e.responsibilities) {
        if (r) candidateBullets.push(r);
      }
    }
  }

  const [selectedBullet, setSelectedBullet] = useState<string>(
    candidateBullets[0] || 'Created a website using React.'
  );
  const [customInput, setCustomInput] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [suggestion, setSuggestion] = useState<BulletRewriteResponse | null>(null);
  const [editMode, setEditMode] = useState(false);
  const [editedText, setEditedText] = useState('');
  const [acceptedBullet, setAcceptedBullet] = useState<string | null>(null);
  const [rejected, setRejected] = useState(false);

  const handleGenerateRewrite = async (bulletToRewrite: string) => {
    if (!bulletToRewrite.trim()) return;
    setLoading(true);
    setRejected(false);
    setAcceptedBullet(null);
    setEditMode(false);
    try {
      const res = await api.rewriteBullet(bulletToRewrite, detectedRole);
      setSuggestion(res);
      setEditedText(res.suggested_bullet);
    } catch (err) {
      console.error('Failed to rewrite bullet:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAccept = () => {
    setAcceptedBullet(editedText || suggestion?.suggested_bullet || '');
    setEditMode(false);
  };

  const handleReject = () => {
    setRejected(true);
    setAcceptedBullet(null);
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 sm:p-8 space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-4 border-b border-slate-100">
        <div>
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-lg bg-indigo-500/10 text-indigo-600 flex items-center justify-center font-bold">
              <Wand2 className="w-4 h-4" />
            </div>
            <h2 className="text-base sm:text-lg font-bold text-slate-900">
              Improve Resume Bullet <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-700 ml-2">Stretch Feature</span>
            </h2>
          </div>
          <p className="text-xs text-slate-500 mt-1">
            Transform passive descriptions into action-oriented statements with zero metric fabrication.
          </p>
        </div>

        {/* Safety Badge */}
        <div className="flex items-center gap-1.5 text-xs text-amber-800 font-medium bg-amber-50 px-3 py-1.5 rounded-lg border border-amber-200">
          <ShieldAlert className="w-4 h-4 text-amber-600 shrink-0" />
          <span>No Fabricated Numbers / Claims</span>
        </div>
      </div>

      {/* Bullet Selection / Input */}
      <div className="space-y-3">
        <label className="text-xs font-bold text-slate-700 block">
          Select or Type a Resume Bullet:
        </label>

        {candidateBullets.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {candidateBullets.slice(0, 3).map((b, i) => (
              <button
                key={i}
                type="button"
                onClick={() => {
                  setSelectedBullet(b);
                  handleGenerateRewrite(b);
                }}
                className={`text-left text-xs p-2.5 rounded-xl border transition-all max-w-md truncate cursor-pointer ${
                  selectedBullet === b
                    ? 'border-indigo-500 bg-indigo-50 text-indigo-900 font-medium'
                    : 'border-slate-200 bg-slate-50 hover:bg-slate-100 text-slate-700'
                }`}
              >
                "{b}"
              </button>
            ))}
          </div>
        )}

        <div className="flex gap-2">
          <input
            type="text"
            value={customInput}
            onChange={(e) => setCustomInput(e.target.value)}
            placeholder="Or type a custom bullet point (e.g. Created a website using React)..."
            className="flex-1 p-2.5 text-xs rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
          <button
            type="button"
            onClick={() => {
              if (customInput) {
                setSelectedBullet(customInput);
                handleGenerateRewrite(customInput);
              }
            }}
            disabled={!customInput || loading}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-slate-200 text-white rounded-xl text-xs font-bold transition-colors flex items-center gap-1.5 shrink-0 cursor-pointer"
          >
            {loading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Sparkles className="w-3.5 h-3.5" />}
            <span>Enhance</span>
          </button>
        </div>
      </div>

      {/* Side-by-Side Comparison */}
      {suggestion && (
        <div className="p-5 rounded-2xl bg-slate-50 border border-slate-200 space-y-4 animate-in fade-in">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Original Bullet */}
            <div className="p-4 rounded-xl bg-white border border-slate-200 space-y-1.5">
              <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">
                Original Bullet
              </span>
              <p className="text-xs text-slate-700 font-medium leading-relaxed">
                "{suggestion.original_bullet}"
              </p>
            </div>

            {/* Suggested Bullet */}
            <div className="p-4 rounded-xl bg-indigo-50/50 border border-indigo-200 space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold uppercase tracking-wider text-indigo-700 block">
                  Suggested Rewrite
                </span>
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-800">
                  Verb: {suggestion.action_verb_improved}
                </span>
              </div>

              {editMode ? (
                <textarea
                  value={editedText}
                  onChange={(e) => setEditedText(e.target.value)}
                  rows={3}
                  className="w-full p-2 text-xs rounded-lg border border-indigo-300 focus:outline-none focus:ring-1 focus:ring-indigo-500 bg-white"
                />
              ) : (
                <p className="text-xs text-slate-900 font-semibold leading-relaxed">
                  "{editedText || suggestion.suggested_bullet}"
                </p>
              )}
            </div>
          </div>

          {/* Action Confirmation Buttons: Accept, Reject, Edit */}
          <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={handleAccept}
                className="px-3.5 py-1.5 rounded-lg text-xs font-bold bg-emerald-600 hover:bg-emerald-700 text-white flex items-center gap-1.5 shadow-xs transition-colors cursor-pointer"
              >
                <Check className="w-3.5 h-3.5" />
                <span>Accept Suggestion</span>
              </button>

              <button
                type="button"
                onClick={() => setEditMode(!editMode)}
                className="px-3.5 py-1.5 rounded-lg text-xs font-bold bg-slate-200 hover:bg-slate-300 text-slate-700 flex items-center gap-1.5 transition-colors cursor-pointer"
              >
                <Edit3 className="w-3.5 h-3.5" />
                <span>{editMode ? 'Done Editing' : 'Edit Suggestion'}</span>
              </button>

              <button
                type="button"
                onClick={handleReject}
                className="px-3.5 py-1.5 rounded-lg text-xs font-bold bg-rose-100 hover:bg-rose-200 text-rose-700 flex items-center gap-1.5 transition-colors cursor-pointer"
              >
                <X className="w-3.5 h-3.5" />
                <span>Reject</span>
              </button>
            </div>

            {/* Status Notifications */}
            {acceptedBullet && (
              <span className="text-xs font-bold text-emerald-700 bg-emerald-100 px-3 py-1 rounded-lg flex items-center gap-1">
                <Check className="w-3.5 h-3.5" /> Suggestion Accepted!
              </span>
            )}

            {rejected && (
              <span className="text-xs font-bold text-slate-500 bg-slate-200 px-3 py-1 rounded-lg">
                Suggestion Rejected
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
