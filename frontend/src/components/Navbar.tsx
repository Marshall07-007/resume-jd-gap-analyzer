import React, { useEffect, useState } from 'react';
import { FileSearch, Sparkles } from 'lucide-react';
import { api } from '../services/api';

interface NavbarProps {
  onLoadDemo: () => void;
  onReset: () => void;
  hasResults: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({ onLoadDemo, onReset, hasResults }) => {
  const [apiOnline, setApiOnline] = useState<boolean | null>(null);

  useEffect(() => {
    api.checkHealth()
      .then(() => setApiOnline(true))
      .catch(() => setApiOnline(false));
  }, []);

  return (
    <header className="sticky top-0 z-40 bg-white/90 backdrop-blur-md border-b border-slate-200 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        {/* Brand */}
        <div className="flex items-center space-x-3 cursor-pointer" onClick={onReset}>
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-600 to-indigo-600 flex items-center justify-center text-white shadow-md shadow-sky-500/20">
            <FileSearch className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-extrabold text-slate-900 tracking-tight text-lg">
                Resume <span className="text-sky-600">↔</span> JD Gap Analyzer
              </span>
              <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-sky-100 text-sky-700 border border-sky-200">
                S-2 Internship Edition
              </span>
            </div>
            <p className="text-xs text-slate-500 hidden sm:block">Explainable career readiness & skill gap intelligence</p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex items-center space-x-3">
          {/* API Health Pill */}
          <div className="hidden md:flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 border border-slate-200 text-slate-600">
            {apiOnline === true ? (
              <>
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                <span className="text-emerald-700">API Connected</span>
              </>
            ) : apiOnline === false ? (
              <>
                <span className="w-2 h-2 rounded-full bg-rose-500" />
                <span className="text-rose-700">API Offline</span>
              </>
            ) : (
              <span>Connecting...</span>
            )}
          </div>

          {/* Quick Demo Button */}
          <button
            onClick={onLoadDemo}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-50 text-indigo-700 hover:bg-indigo-100 border border-indigo-200 transition-colors shadow-sm cursor-pointer"
            title="Load standard sample resume and frontend JD"
          >
            <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
            <span>Try Demo</span>
          </button>

          {hasResults && (
            <button
              onClick={onReset}
              className="px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-100 text-slate-700 hover:bg-slate-200 transition-colors cursor-pointer"
            >
              New Analysis
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
