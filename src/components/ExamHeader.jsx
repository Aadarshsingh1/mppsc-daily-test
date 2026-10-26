import React from 'react';

export default function ExamHeader({ secondsRemaining, onOpenSubmit, language, onChangeLanguage }) {
  const mins = Math.floor(secondsRemaining / 60);
  const secs = secondsRemaining % 60;
  const timeDisplay = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

  let timerColor = 'text-amber-300';
  if (secondsRemaining < 300) timerColor = 'text-red-400 animate-pulse';
  else if (secondsRemaining < 900) timerColor = 'text-amber-300';

  return (
    <div className="bg-blue-950 text-white shrink-0 border-b border-blue-900">
      <div className="px-4 py-2 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-white text-blue-950 font-black text-sm flex items-center justify-center">
            MP
          </div>
          <div>
            <h2 className="text-sm font-bold tracking-tight">MPPSC Mock Examination — Test 01</h2>
            <div className="text-[11px] text-blue-200">General Studies Paper-I • 100 MCQs • +1 / -0.25</div>
          </div>
        </div>

        {/* Center Countdown Clock */}
        <div className="flex items-center gap-2 bg-blue-900/80 border border-blue-700/80 px-4 py-1.5 rounded-md">
          <span className="text-xs text-blue-300 font-medium">Time Left:</span>
          <span className={`font-mono text-base md:text-lg font-bold ${timerColor}`}>{timeDisplay}</span>
        </div>

        {/* Right Action */}
        <div className="flex items-center gap-3">
          <div className="hidden sm:flex items-center gap-2 text-right">
            <div>
              <div className="text-xs font-bold text-white">Aadarsh Thakur</div>
              <div className="text-[10px] text-blue-300 font-mono">Roll: MPPSC-2026-489102</div>
            </div>
            <div className="w-8 h-8 rounded bg-blue-800 border border-blue-600 flex items-center justify-center text-xs font-bold text-blue-200">
              AT
            </div>
          </div>

          <button
            onClick={onOpenSubmit}
            className="bg-red-600 hover:bg-red-500 text-white font-bold text-xs px-3.5 py-2 rounded shadow transition"
          >
            Submit Exam
          </button>
        </div>
      </div>

      {/* Sub-strip with Language Toggle */}
      <div className="bg-white text-slate-800 border-t border-slate-200 px-4 py-1.5 flex items-center justify-between text-xs">
        <div className="font-semibold text-slate-700">
          Section: <span className="text-blue-950 font-bold">General Studies (सामान्य अध्ययन)</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-slate-500">View In:</span>
          <select 
            value={language}
            onChange={(e) => onChangeLanguage(e.target.value)}
            className="border border-slate-300 rounded px-2 py-1 text-xs bg-slate-50 font-medium text-slate-700 focus:outline-none"
          >
            <option value="both">Bilingual (हिन्दी + English)</option>
            <option value="en">English Only</option>
            <option value="hi">हिन्दी Only</option>
          </select>
        </div>
      </div>
    </div>
  );
}
