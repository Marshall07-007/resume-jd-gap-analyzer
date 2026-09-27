import React, { useRef, useState, useEffect } from 'react';
import {
  UploadCloud,
  CheckCircle2,
  AlertCircle,
  X,
  Loader2,
  Sparkles,
  ChevronDown,
  ChevronUp
} from 'lucide-react';
import { api } from '../services/api';
import { StructuredResume, ResumeUploadResponse } from '../types';

interface ResumeUploaderProps {
  structuredResume: StructuredResume | null;
  onStructuredResumeChange: (data: StructuredResume | null) => void;
  rawResumeText: string;
  onRawResumeTextChange: (text: string) => void;
}

export const ResumeUploader: React.FC<ResumeUploaderProps> = ({
  structuredResume,
  onStructuredResumeChange,
  rawResumeText,
  onRawResumeTextChange,
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [fileMeta, setFileMeta] = useState<{ name: string; size: string; type: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [showJsonPreview, setShowJsonPreview] = useState(false);
  const [activeTab, setActiveTab] = useState<'upload' | 'text'>('upload');

  // Keep internal fileMeta in sync with external resume state
  useEffect(() => {
    if (!structuredResume && !rawResumeText.trim()) {
      setFileMeta(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
    } else if (structuredResume && !fileMeta) {
      setFileMeta({
        name: structuredResume.personal?.name ? `${structuredResume.personal.name}'s Resume` : 'Loaded Structured Resume',
        size: `${structuredResume.skills.length} skills extracted`,
        type: 'PARSED',
      });
    }
  }, [structuredResume, rawResumeText]);

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
  };

  const handleFile = async (file: File) => {
    setError(null);
    const validExtensions = ['.pdf', '.docx'];
    const fileName = file.name.toLowerCase();
    const isValid = validExtensions.some(ext => fileName.endsWith(ext));

    if (!isValid) {
      setError('Please upload a valid .pdf or .docx document.');
      return;
    }

    if (file.size > 10 * 1024 * 1024) {
      setError('File exceeds 10MB maximum limit.');
      return;
    }

    try {
      setLoading(true);
      const res: ResumeUploadResponse = await api.uploadResume(file);
      setFileMeta({
        name: res.file_name,
        size: formatFileSize(res.file_size_bytes),
        type: res.file_type,
      });
      onStructuredResumeChange(res.structured);
      onRawResumeTextChange(res.structured.raw_text || '');
    } catch (err: any) {
      const msg = err.response?.data?.detail || err.message || 'Failed to extract resume content.';
      setError(msg);
      setFileMeta(null);
      onStructuredResumeChange(null);
      onRawResumeTextChange('');
    } finally {
      setLoading(false);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleClear = () => {
    setFileMeta(null);
    setError(null);
    onStructuredResumeChange(null);
    onRawResumeTextChange('');
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleTextParse = async (text: string) => {
    onRawResumeTextChange(text);
    if (!text.trim()) {
      onStructuredResumeChange(null);
      setFileMeta(null);
      return;
    }
    try {
      setLoading(true);
      const res = await api.parseResumeText(text);
      onStructuredResumeChange(res);
      setFileMeta({
        name: 'Pasted / Direct Resume Input',
        size: `${text.length} chars`,
        type: 'TEXT',
      });
    } catch (err: any) {
      console.warn('Text parsing warning:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 flex flex-col h-full">
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-slate-100 mb-4">
        <div>
          <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <span className="flex items-center justify-center w-6 h-6 rounded-md bg-sky-100 text-sky-700 text-xs font-bold">1</span>
            Upload Your Resume
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">Supports PDF or Word DOCX documents</p>
        </div>

        {/* Tab Toggle */}
        <div className="flex items-center bg-slate-100 p-1 rounded-lg text-xs font-medium text-slate-600">
          <button
            type="button"
            onClick={() => setActiveTab('upload')}
            className={`px-2.5 py-1 rounded-md transition-all cursor-pointer ${
              activeTab === 'upload' ? 'bg-white text-slate-900 shadow-xs font-semibold' : 'hover:text-slate-900'
            }`}
          >
            File Upload
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('text')}
            className={`px-2.5 py-1 rounded-md transition-all cursor-pointer ${
              activeTab === 'text' ? 'bg-white text-slate-900 shadow-xs font-semibold' : 'hover:text-slate-900'
            }`}
          >
            Paste Text
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="mb-4 p-3 rounded-xl bg-rose-50 border border-rose-200 text-xs text-rose-700 flex items-start gap-2 animate-in fade-in">
          <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
          <div className="flex-1 font-medium">{error}</div>
          <button onClick={() => setError(null)} className="text-rose-400 hover:text-rose-700 cursor-pointer">
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* Upload View */}
      {activeTab === 'upload' && (
        <div className="flex-1 flex flex-col justify-center">
          {!fileMeta && !loading && (
            <div
              onDragOver={(e) => e.preventDefault()}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className="border-2 border-dashed border-slate-300 hover:border-sky-500 bg-slate-50/60 hover:bg-sky-50/40 rounded-xl p-8 text-center cursor-pointer transition-all flex flex-col items-center justify-center group"
            >
              <input
                type="file"
                ref={fileInputRef}
                className="hidden"
                accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
              />
              <div className="w-12 h-12 rounded-full bg-white shadow-xs border border-slate-200 flex items-center justify-center text-slate-500 group-hover:text-sky-600 group-hover:border-sky-200 group-hover:scale-110 transition-all mb-3">
                <UploadCloud className="w-6 h-6" />
              </div>
              <p className="text-sm font-semibold text-slate-800">
                Click to upload <span className="text-slate-500 font-normal">or drag & drop</span>
              </p>
              <p className="text-xs text-slate-500 mt-1">PDF or DOCX (max 10MB)</p>
            </div>
          )}

          {/* Loading state */}
          {loading && (
            <div className="p-8 rounded-xl bg-slate-50 border border-slate-200 flex flex-col items-center justify-center text-center space-y-3">
              <Loader2 className="w-8 h-8 text-sky-600 animate-spin" />
              <div className="space-y-1">
                <p className="text-sm font-semibold text-slate-800">Extracting & Structuring Document</p>
                <p className="text-xs text-slate-500">Running PyMuPDF / python-docx parser & skill normalizer...</p>
              </div>
            </div>
          )}

          {/* Loaded File Details Card */}
          {fileMeta && !loading && (
            <div className="space-y-3">
              <div className="p-4 rounded-xl bg-sky-50/60 border border-sky-200 flex items-center justify-between">
                <div className="flex items-center space-x-3 overflow-hidden">
                  <div className="w-10 h-10 rounded-lg bg-sky-600 text-white flex items-center justify-center shrink-0 shadow-xs font-bold text-xs uppercase">
                    {fileMeta.type}
                  </div>
                  <div className="overflow-hidden">
                    <p className="text-sm font-semibold text-slate-900 truncate" title={fileMeta.name}>
                      {fileMeta.name}
                    </p>
                    <div className="flex items-center gap-2 text-xs text-slate-500 mt-0.5">
                      <span>{fileMeta.size}</span>
                      <span>•</span>
                      <span className="text-emerald-700 font-medium flex items-center gap-1">
                        <CheckCircle2 className="w-3.5 h-3.5" /> Structured JSON Ready
                      </span>
                    </div>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={handleClear}
                  className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition-colors cursor-pointer"
                  title="Remove and upload different file"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Paste Text View */}
      {activeTab === 'text' && (
        <div className="flex-1 flex flex-col space-y-2">
          <textarea
            value={rawResumeText}
            onChange={(e) => handleTextParse(e.target.value)}
            placeholder="Paste your raw resume text here (Skills, Projects, Experience, Education)..."
            rows={8}
            className="w-full flex-1 p-3.5 rounded-xl border border-slate-200 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent text-xs font-mono bg-slate-50 resize-none"
          />
          <div className="flex justify-between items-center text-xs text-slate-500">
            <span>{rawResumeText.length} characters</span>
            {rawResumeText && (
              <button
                type="button"
                onClick={handleClear}
                className="text-xs text-rose-600 hover:underline cursor-pointer"
              >
                Clear
              </button>
            )}
          </div>
        </div>
      )}

      {/* Extracted Structured Preview Accordion */}
      {structuredResume && (
        <div className="mt-4 pt-3 border-t border-slate-100">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-700 flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-sky-600" />
              Extracted Information Preview
            </span>
            <button
              type="button"
              onClick={() => setShowJsonPreview(!showJsonPreview)}
              className="text-xs text-sky-600 hover:text-sky-700 font-medium flex items-center gap-0.5 cursor-pointer"
            >
              {showJsonPreview ? 'Hide JSON' : 'Inspect JSON'}
              {showJsonPreview ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
            </button>
          </div>

          {/* Quick Stats Chips */}
          <div className="grid grid-cols-3 gap-2 mt-2">
            <div className="p-2 rounded-lg bg-slate-50 border border-slate-100 text-center">
              <span className="text-[10px] text-slate-500 font-medium block">Skills Extracted</span>
              <span className="text-xs font-bold text-sky-700">{structuredResume.skills.length}</span>
            </div>
            <div className="p-2 rounded-lg bg-slate-50 border border-slate-100 text-center">
              <span className="text-[10px] text-slate-500 font-medium block">Projects</span>
              <span className="text-xs font-bold text-indigo-700">{structuredResume.projects.length}</span>
            </div>
            <div className="p-2 rounded-lg bg-slate-50 border border-slate-100 text-center">
              <span className="text-[10px] text-slate-500 font-medium block">Education</span>
              <span className="text-xs font-bold text-emerald-700">{structuredResume.education.length}</span>
            </div>
          </div>

          {/* Collapsible Extracted Skills List */}
          {structuredResume.skills.length > 0 && !showJsonPreview && (
            <div className="mt-2.5 flex flex-wrap gap-1.5 max-h-24 overflow-y-auto pr-1">
              {structuredResume.skills.map((skill, idx) => (
                <span
                  key={idx}
                  className="px-2 py-0.5 rounded-md text-[11px] font-medium bg-slate-100 text-slate-700 border border-slate-200"
                >
                  {skill}
                </span>
              ))}
            </div>
          )}

          {/* Structured JSON Modal/Drawer Code */}
          {showJsonPreview && (
            <pre className="mt-2 p-3 bg-slate-900 text-slate-200 rounded-lg text-[10px] font-mono max-h-48 overflow-auto">
              {JSON.stringify(
                {
                  personal: structuredResume.personal,
                  skills: structuredResume.skills,
                  projects: structuredResume.projects,
                  education: structuredResume.education,
                  experience: structuredResume.experience,
                },
                null,
                2
              )}
            </pre>
          )}
        </div>
      )}
    </div>
  );
};
