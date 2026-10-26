import React from 'react';

export default function QuestionPanel({
  question,
  response,
  language,
  onSelectOption,
  onSaveAndNext,
  onClearResponse,
  onMarkForReview,
  onPrevious,
  hasPrevious
}) {
  const letters = ['A', 'B', 'C', 'D'];

  return (
    <div className="flex-1 flex flex-col bg-white overflow-y-auto border-r border-slate-200">
      {/* Question Header Strip */}
      <div className="bg-slate-50 border-b border-slate-200 px-5 py-2.5 flex items-center justify-between text-xs">
        <div className="font-bold text-slate-800">
          Question No. <span className="text-blue-900 text-sm">{question.id}</span> of 100
        </div>
        <div className="flex items-center gap-3 text-slate-500">
          <span>Marks: <span className="font-bold text-emerald-600">+1.00</span></span>
          <span>Negative: <span className="font-bold text-rose-600">-0.25</span></span>
        </div>
      </div>

      {/* Main Question & Options Area */}
      <div className="flex-1 p-5 md:p-7 space-y-5">
        {(language === 'both' || language === 'en') && (
          <div className="text-slate-900 text-base md:text-lg font-medium leading-relaxed">
            <span className="text-blue-900 font-bold mr-1.5">Q{question.id}.</span> {question.question_en}
          </div>
        )}

        {(language === 'both' || language === 'hi') && (
          <div className="text-slate-800 text-base md:text-lg font-medium leading-relaxed bg-amber-50/50 p-4 rounded-lg border border-amber-200/60">
            <span className="text-amber-800 font-bold mr-1.5">प्र. {question.id}.</span> {question.question_hi}
          </div>
        )}

        {/* Options */}
        <div className="pt-2">
          <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">Options:</div>
          <div className="space-y-3">
            {letters.map((key, idx) => {
              const isChecked = response.selectedOption === key;
              return (
                <label 
                  key={key}
                  className={`p-3.5 rounded-lg border cursor-pointer transition flex items-start gap-3 select-none ${
                    isChecked ? 'bg-blue-50/70 border-blue-600 shadow-xs' : 'bg-white border-slate-200 hover:border-slate-300 hover:bg-slate-50'
                  }`}
                >
                  <input
                    type="radio"
                    name={`q-${question.id}`}
                    value={key}
                    checked={isChecked}
                    onChange={() => onSelectOption(key)}
                    className="mt-1 w-4 h-4 text-blue-600 border-slate-300 focus:ring-blue-500 cursor-pointer"
                  />
                  <span className="w-5 h-5 rounded-full bg-slate-100 border border-slate-300 text-slate-700 text-[11px] font-bold flex items-center justify-center shrink-0 mt-0.5">
                    {key}
                  </span>
                  <div className="flex-1 text-xs md:text-sm">
                    {(language === 'both' || language === 'en') && (
                      <div className="font-medium text-slate-800">{question.options_en[idx]}</div>
                    )}
                    {(language === 'both' || language === 'hi') && (
                      <div className="text-slate-600 mt-0.5">{question.options_hi[idx]}</div>
                    )}
                  </div>
                </label>
              );
            })}
          </div>
        </div>
      </div>

      {/* Action Buttons Strip */}
      <div className="bg-slate-50 border-t border-slate-200 px-4 py-3 flex flex-wrap items-center justify-between gap-3 shrink-0">
        <div className="flex items-center gap-2">
          <button
            onClick={onPrevious}
            disabled={!hasPrevious}
            className="px-4 py-2 bg-white hover:bg-slate-100 text-slate-700 text-xs font-semibold rounded border border-slate-300 transition shadow-sm disabled:opacity-40"
          >
            Previous
          </button>
          <button
            onClick={onClearResponse}
            className="px-4 py-2 bg-white hover:bg-rose-50 text-rose-700 text-xs font-semibold rounded border border-rose-300 transition shadow-sm"
          >
            Clear Response
          </button>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={onMarkForReview}
            className="px-4 py-2 bg-purple-100 hover:bg-purple-200 text-purple-900 text-xs font-bold rounded border border-purple-300 transition shadow-sm"
          >
            Mark for Review & Next
          </button>
          <button
            onClick={onSaveAndNext}
            className="px-5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold rounded transition shadow-md shadow-emerald-900/10"
          >
            Save & Next
          </button>
        </div>
      </div>
    </div>
  );
}
