import React, { useState } from 'react';

export default function ResultScreen({ result, questions, onReturnDashboard, onViewHistory }) {
  const [filter, setFilter] = useState('ALL'); // 'ALL', 'CORRECT', 'INCORRECT', 'UNATTEMPTED'

  const filteredQuestions = questions.filter(q => {
    const userChoice = result.responses[q.id]?.selectedOption;
    const isCorrect = userChoice === q.correct;
    const isSkipped = !userChoice;

    if (filter === 'CORRECT') return isCorrect;
    if (filter === 'INCORRECT') return !isCorrect && !isSkipped;
    if (filter === 'UNATTEMPTED') return isSkipped;
    return true;
  });

  return (
    <div className="max-w-7xl mx-auto p-4 md:p-6 space-y-6">
      {/* Official Scorecard Box */}
      <div className="bg-white border-2 border-blue-900 rounded-xl p-6 shadow-sm">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-6 border-b border-slate-200">
          <div>
            <div className="inline-block bg-blue-100 text-blue-900 text-xs font-bold px-3 py-1 rounded mb-2">
              OFFICIAL EXAMINATION SCORECARD
            </div>
            <h2 className="text-2xl font-black text-slate-900">MPPSC Mock Examination — Test 01</h2>
            <p className="text-xs text-slate-500 mt-1">
              Candidate: <b>Aadarsh Thakur</b> • Roll No: <b>MPPSC-2026-489102</b> • Date: {result.date}
            </p>
          </div>

          <div className="bg-slate-50 border-2 border-blue-900 rounded-xl p-5 text-center min-w-[200px]">
            <div className="text-xs font-bold text-slate-500 uppercase tracking-wider">Final Net Score</div>
            <div className="text-4xl font-black text-blue-950 my-1">{result.score}</div>
            <div className="text-xs text-slate-600 font-semibold">Maximum: 100.00 Marks</div>
          </div>
        </div>

        {/* Metrics Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-6 text-center text-xs">
          <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-lg">
            <div className="text-emerald-700 font-medium">Correct Answers (+1)</div>
            <div className="text-xl font-bold text-emerald-800 mt-1">{result.correct}</div>
          </div>
          <div className="p-3 bg-rose-50 border border-rose-200 rounded-lg">
            <div className="text-rose-700 font-medium">Incorrect Answers (-0.25)</div>
            <div className="text-xl font-bold text-rose-800 mt-1">{result.incorrect}</div>
          </div>
          <div className="p-3 bg-slate-50 border border-slate-200 rounded-lg">
            <div className="text-slate-600 font-medium">Unattempted (0)</div>
            <div className="text-xl font-bold text-slate-800 mt-1">{result.unattempted}</div>
          </div>
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="text-blue-700 font-medium">Accuracy</div>
            <div className="text-xl font-bold text-blue-900 mt-1">{result.accuracy}</div>
          </div>
          <div className="p-3 bg-purple-50 border border-purple-200 rounded-lg col-span-2 sm:col-span-1">
            <div className="text-purple-700 font-medium">Time Taken</div>
            <div className="text-xl font-bold text-purple-900 mt-1">{result.timeTaken}</div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-wrap items-center justify-between gap-3 pt-6 mt-6 border-t border-slate-200">
          <div className="text-xs text-slate-500">{result.comparisonNote}</div>
          <div className="flex items-center gap-3">
            <button
              onClick={onViewHistory}
              className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg border border-slate-300 transition"
            >
              View All Test History
            </button>
            <button
              onClick={onReturnDashboard}
              className="px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white text-xs font-bold rounded-lg shadow transition"
            >
              Return to Dashboard
            </button>
          </div>
        </div>
      </div>

      {/* Question Solutions List */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 pb-3">
          <div>
            <h3 className="font-bold text-base text-slate-900">Detailed Question Solutions & Explanations</h3>
            <p className="text-xs text-slate-500">Verify your responses against the official key</p>
          </div>
          <div className="flex items-center gap-1.5 text-xs">
            {['ALL', 'CORRECT', 'INCORRECT', 'UNATTEMPTED'].map(m => (
              <button
                key={m}
                onClick={() => setFilter(m)}
                className={`px-3 py-1.5 rounded-md font-semibold transition ${
                  filter === m ? 'bg-blue-900 text-white' : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {m === 'ALL' ? 'All (100)' : m.charAt(0) + m.slice(1).toLowerCase()}
              </button>
            ))}
          </div>
        </div>

        <div className="space-y-4">
          {filteredQuestions.map(q => {
            const userChoice = result.responses[q.id]?.selectedOption;
            const isCorrect = userChoice === q.correct;
            const isSkipped = !userChoice;
            const letters = ['A', 'B', 'C', 'D'];

            return (
              <div 
                key={q.id}
                className={`p-4 rounded-xl border ${isCorrect ? 'border-emerald-300 bg-emerald-50/20' : isSkipped ? 'border-slate-200' : 'border-rose-300 bg-rose-50/20'} space-y-3`}
              >
                <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                  <span className="font-bold text-xs text-blue-950">Question {q.id}</span>
                  <div>
                    {isSkipped && <span className="px-2.5 py-0.5 rounded text-[11px] font-bold bg-slate-100 text-slate-600 border border-slate-300">Unattempted</span>}
                    {isCorrect && <span className="px-2.5 py-0.5 rounded text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">Correct (+1.00)</span>}
                    {!isCorrect && !isSkipped && <span className="px-2.5 py-0.5 rounded text-[11px] font-bold bg-rose-100 text-rose-800 border border-rose-300">Incorrect (-0.25)</span>}
                  </div>
                </div>

                <div className="text-xs md:text-sm font-medium text-slate-800">{q.question_en}</div>
                <div className="text-xs md:text-sm text-slate-600">{q.question_hi}</div>

                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                  {letters.map((l, idx) => {
                    let optStyle = 'border-slate-200 bg-slate-50 text-slate-700';
                    if (l === q.correct) {
                      optStyle = 'border-emerald-500 bg-emerald-50 text-emerald-900 font-bold';
                    } else if (userChoice === l && !isCorrect) {
                      optStyle = 'border-rose-500 bg-rose-50 text-rose-900 font-semibold';
                    }

                    return (
                      <div key={l} className={`p-2.5 rounded-lg border ${optStyle} flex items-start gap-2 text-xs`}>
                        <span className="font-bold shrink-0">{l}.</span>
                        <div className="flex-1">
                          <div>{q.options_en[idx]}</div>
                          <div className="text-slate-500 mt-0.5">{q.options_hi[idx]}</div>
                        </div>
                      </div>
                    );
                  })}
                </div>

                <div className="bg-blue-50/70 border border-blue-200 rounded-lg p-3 text-xs space-y-1.5 mt-2">
                  <div className="font-bold text-blue-900">Official Correct Answer: Option ({q.correct})</div>
                  <div className="text-slate-700 leading-relaxed">{q.explanation_en}</div>
                  <div className="text-slate-600 leading-relaxed pt-1 border-t border-blue-100">{q.explanation_hi}</div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
