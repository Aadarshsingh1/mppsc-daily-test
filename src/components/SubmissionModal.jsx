import React from 'react';

export default function SubmissionModal({ responses, onCancel, onConfirm }) {
  let ans = 0;
  let notAns = 0;
  let notVisited = 0;
  let marked = 0;
  let ansMarked = 0;

  Object.values(responses).forEach(r => {
    if (r.state === 'ANSWERED') ans++;
    else if (r.state === 'NOT_ANSWERED') notAns++;
    else if (r.state === 'MARKED_FOR_REVIEW') marked++;
    else if (r.state === 'ANSWERED_AND_MARKED') ansMarked++;
    else notVisited++;
  });

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white border border-slate-300 rounded-xl max-w-lg w-full p-6 shadow-2xl space-y-4">
        <div className="flex items-center gap-3 border-b border-slate-200 pb-3">
          <div className="w-10 h-10 rounded-full bg-amber-100 text-amber-700 flex items-center justify-center font-bold text-lg">
            ⚠️
          </div>
          <div>
            <h3 className="font-bold text-base text-slate-900">Confirm Examination Submission</h3>
            <p className="text-xs text-slate-500">Please review your question response summary</p>
          </div>
        </div>

        <div className="bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs space-y-2">
          <div className="grid grid-cols-2 gap-2">
            <div className="flex justify-between p-2 bg-white rounded border border-slate-200">
              <span className="text-slate-600">Total Questions:</span>
              <span className="font-bold text-slate-900">100</span>
            </div>
            <div className="flex justify-between p-2 bg-emerald-50 rounded border border-emerald-200">
              <span className="text-emerald-800">Answered:</span>
              <span className="font-bold text-emerald-800">{ans}</span>
            </div>
            <div className="flex justify-between p-2 bg-rose-50 rounded border border-rose-200">
              <span className="text-rose-800">Not Answered:</span>
              <span className="font-bold text-rose-800">{notAns}</span>
            </div>
            <div className="flex justify-between p-2 bg-purple-50 rounded border border-purple-200">
              <span className="text-purple-800">Marked for Review:</span>
              <span className="font-bold text-purple-800">{marked}</span>
            </div>
            <div className="flex justify-between p-2 bg-purple-50 rounded border border-purple-200 col-span-2">
              <span className="text-purple-800">Answered & Marked for Review:</span>
              <span className="font-bold text-purple-800">{ansMarked}</span>
            </div>
            <div className="flex justify-between p-2 bg-slate-100 rounded border border-slate-200 col-span-2">
              <span className="text-slate-600">Not Visited:</span>
              <span className="font-bold text-slate-700">{notVisited}</span>
            </div>
          </div>
        </div>

        <p className="text-xs text-slate-600 leading-relaxed">
          <b>Are you sure you want to submit?</b> Once confirmed, you will not be able to revisit or modify any answers.
        </p>

        <div className="flex items-center justify-end gap-3 pt-2 border-t border-slate-200">
          <button
            onClick={onCancel}
            className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg border border-slate-300 transition"
          >
            Return to Examination
          </button>
          <button
            onClick={onConfirm}
            className="px-4 py-2 bg-red-600 hover:bg-red-500 text-white text-xs font-bold rounded-lg shadow transition"
          >
            Yes, Submit Examination
          </button>
        </div>
      </div>
    </div>
  );
}
