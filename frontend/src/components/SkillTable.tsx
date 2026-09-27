import React from 'react';
import { CheckCircle2, Clock, XCircle, PlusCircle, Search } from 'lucide-react';
import { SkillGapItem, SkillStatus } from '../types';

interface SkillTableProps {
  items: SkillGapItem[];
}

export const SkillTable: React.FC<SkillTableProps> = ({ items }) => {
  const [searchTerm, setSearchTerm] = React.useState('');

  const filteredItems = items.filter(
    (item) =>
      item.skill.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.resume_evidence.toLowerCase().includes(searchTerm.toLowerCase()) ||
      item.jd_evidence.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStatusBadge = (status: SkillStatus) => {
    switch (status) {
      case 'matched':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
            Matched
          </span>
        );
      case 'partial':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-amber-100 text-amber-800 border border-amber-200">
            <Clock className="w-3.5 h-3.5 text-amber-600" />
            Partial
          </span>
        );
      case 'missing':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-rose-100 text-rose-800 border border-rose-200">
            <XCircle className="w-3.5 h-3.5 text-rose-600" />
            Missing
          </span>
        );
      case 'bonus':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-bold bg-purple-100 text-purple-800 border border-purple-200">
            <PlusCircle className="w-3.5 h-3.5 text-purple-600" />
            Bonus
          </span>
        );
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
      {/* Table Header Controls */}
      <div className="p-4 sm:p-6 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-base font-bold text-slate-900">Skill Gap Analysis Matrix</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Traceable line-by-line comparison against Job Description and role corpus
          </p>
        </div>

        {/* Quick Search */}
        <div className="relative w-full sm:w-64">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Filter skills or evidence..."
            className="w-full pl-9 pr-3 py-1.5 text-xs rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500"
          />
        </div>
      </div>

      {/* Table Element */}
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="bg-slate-50/80 border-b border-slate-200/80 text-[11px] font-bold text-slate-500 uppercase tracking-wider">
              <th className="py-3 px-4 sm:px-6">Skill</th>
              <th className="py-3 px-4">Status</th>
              <th className="py-3 px-4 sm:px-6">Resume Evidence</th>
              <th className="py-3 px-4 sm:px-6">JD / Corpus Source</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 text-xs text-slate-700 font-normal">
            {filteredItems.length === 0 ? (
              <tr>
                <td colSpan={4} className="py-8 text-center text-slate-400 text-xs">
                  No skills matched your search criteria.
                </td>
              </tr>
            ) : (
              filteredItems.map((item, idx) => (
                <tr
                  key={idx}
                  className="hover:bg-slate-50/80 transition-colors"
                >
                  {/* Skill Name */}
                  <td className="py-3.5 px-4 sm:px-6 font-bold text-slate-900 whitespace-nowrap">
                    {item.skill}
                  </td>

                  {/* Status Badge */}
                  <td className="py-3.5 px-4 whitespace-nowrap">
                    {getStatusBadge(item.status)}
                  </td>

                  {/* Resume Evidence */}
                  <td className="py-3.5 px-4 sm:px-6 max-w-xs sm:max-w-md">
                    <span className="font-medium text-slate-800">{item.resume_evidence}</span>
                    {item.explanation && item.status === 'partial' && (
                      <span className="block text-[11px] text-amber-700 mt-0.5 font-normal italic">
                        {item.explanation}
                      </span>
                    )}
                  </td>

                  {/* JD / Corpus Source */}
                  <td className="py-3.5 px-4 sm:px-6 max-w-xs">
                    <div className="space-y-0.5">
                      <span className="inline-block px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-600 border border-slate-200">
                        {item.source}
                      </span>
                      <p className="text-[11px] text-slate-500 truncate" title={item.jd_evidence}>
                        {item.jd_evidence}
                      </p>
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};
