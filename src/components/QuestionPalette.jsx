import React from 'react';

export default function QuestionPalette({
  questions,
  responses,
  currentQIdx,
  onSelectQuestion,
  onOpenSubmit
}) {
  // Compute counts for the 5 states
  let answered = 0;
  let notAnswered = 0;
  let notVisited = 0;
  let marked = 0;
  let ansMarked = 0;

  Object.values(responses).forEach(r => {
    if (r.state === 'ANSWERED') answered++;
    else if (r.state === 'NOT_ANSWERED') notAnswered++;
    else if (r.state === 'MARKED_FOR_REVIEW') marked++;
    else if (r.state === 'ANSWERED_AND_MARKED') ansMarked++;
    else notVisited++;
  });

  return (
    <div className="w-full lg:w-80 bg-slate-50 flex flex-col shrink-0 border-t lg:border-t-0 overflow-y-auto">
      {/* Candidate Mini Profile */}
      <div className="p-3 bg-white border-b border-slate-200 flex items-center gap-3">
        <div className="w-10 h-10 rounded bg-slate-200 border border-slate-300 flex items-center justify-center text-slate-500 font-bold text-xs shrink-0">
          PHOTO
        </div>
        <div className="overflow-hidden">
          <div className="text-xs font-bold text-slate-800 truncate">Aadarsh Thakur</div>
          <div className="text-[10px] text-slate-500">Roll: MPPSC-2026-489102</div>
        </div>
      </div>

      {/* Legend with exact CBT shapes and colors */}
      <div className="p-3 bg-white border-b border-slate-200 text-[11px] space-y-2">
        <div className="font-bold text-slate-700 text-xs mb-1">Question Status Legend:</div>
        <div className="grid grid-cols-2 gap-2 text-slate-600">
          <div className="flex items-center gap-2">
            <span className="w-5 h-4 bg-emerald-500 rounded text-white text-[9px] font-bold flex items-center justify-center">#</span>
            <span>Answered (<b>{answered}</b>)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-5 h-4 bg-red-500 rounded text-white text-[9px] font-bold flex items-center justify-center">#</span>
            <span>Not Answered (<b>{notAnswered}</b>)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-5 h-4 bg-slate-200 border border-slate-300 rounded text-slate-600 text-[9px] font-bold flex items-center justify-center">#</span>
            <span>Not Visited (<b>{notVisited}</b>)</span>
          </div>
          <div className="flex items-center gap-2">
            <span className="w-4 h-4 bg-purple-600 rounded-full text-white text-[9px] font-bold flex items-center justify-center">#</span>
            <span>Marked (<b>{marked}</b>)</span>
          </div>
        </div>
        <div className="flex items-center gap-2 pt-1 border-t border-slate-100 text-slate-600">
          <span className="relative w-4 h-4 bg-purple-600 rounded-full text-white text-[9px] font-bold flex items-center justify-center">
            #
            <span className="absolute -bottom-0.5 -right-0.5 w-2 h-2 bg-emerald-400 rounded-full border border-white"></span>
          </span>
          <span>Ans. & Marked (<b>{ansMarked}</b>)</span>
        </div>
      </div>

      {/* 100-Question Grid */}
      <div className="flex-1 p-3">
        <div className="text-xs font-bold text-slate-700 mb-2">Questions (1 - 100):</div>
        <div className="grid grid-cols-5 gap-1.5">
          {questions.map((q, idx) => {
            const resp = responses[q.id] || {};
            const isCurrent = idx === currentQIdx;

            let btnClass = "w-[38px] h-[34px] text-xs font-semibold flex items-center justify-center rounded border transition select-none ";
            if (resp.state === 'ANSWERED') {
              btnClass += "bg-emerald-500 text-white border-emerald-600 ";
            } else if (resp.state === 'NOT_ANSWERED') {
              btnClass += "bg-red-500 text-white border-red-600 ";
            } else if (resp.state === 'MARKED_FOR_REVIEW') {
              btnClass += "bg-purple-600 text-white border-purple-700 rounded-full ";
            } else if (resp.state === 'ANSWERED_AND_MARKED') {
              btnClass += "relative bg-purple-600 text-white border-purple-700 rounded-full ";
            } else {
              btnClass += "bg-slate-100 text-slate-700 border-slate-300 ";
            }

            if (isCurrent) {
              btnClass += "ring-2 ring-blue-600 ring-offset-1 font-bold ";
            }

            return (
              <button
                key={q.id}
                onClick={() => onSelectQuestion(idx)}
                className={btnClass}
              >
                {q.id}
                {resp.state === 'ANSWERED_AND_MARKED' && (
                  <span className="absolute bottom-0.5 right-0.5 w-2 h-2 bg-emerald-400 rounded-full border border-white"></span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      {/* Bottom Submit */}
      <div className="p-3 bg-white border-t border-slate-200 shrink-0">
        <button
          onClick={onOpenSubmit}
          className="w-full py-2 bg-blue-900 hover:bg-blue-800 text-white font-bold text-xs rounded shadow transition"
        >
          Final Examination Submit
        </button>
      </div>
    </div>
  );
}
