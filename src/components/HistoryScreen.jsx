import React from 'react';

export default function HistoryScreen({ history, onReturnDashboard }) {
  return (
    <div className="max-w-7xl mx-auto p-4 md:p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-slate-900">Candidate Examination History</h2>
          <p className="text-xs text-slate-500">Chronological record of completed MPPSC mock tests</p>
        </div>
        <button
          onClick={onReturnDashboard}
          className="px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white text-xs font-bold rounded-lg shadow transition"
        >
          ← Back to Dashboard
        </button>
      </div>

      <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-700 font-bold border-b border-slate-200">
              <tr>
                <th className="p-3.5">Test No.</th>
                <th className="p-3.5">Date & Time</th>
                <th className="p-3.5 text-right">Score /100</th>
                <th className="p-3.5 text-center text-emerald-700">Correct</th>
                <th className="p-3.5 text-center text-rose-700">Incorrect</th>
                <th className="p-3.5 text-center text-slate-600">Unattempted</th>
                <th className="p-3.5 text-right text-blue-900">Accuracy</th>
                <th className="p-3.5 text-right">Time Taken</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {history.length === 0 ? (
                <tr>
                  <td colSpan="8" className="p-6 text-center text-slate-400">
                    No examination records found.
                  </td>
                </tr>
              ) : (
                history.map((h, i) => (
                  <tr key={i} className="hover:bg-slate-50 transition">
                    <td className="p-3 font-bold text-blue-950">Test {h.testNo}</td>
                    <td className="p-3 text-slate-600">{h.dateTime || h.date}</td>
                    <td className="p-3 text-right font-extrabold text-blue-900">{h.score}</td>
                    <td className="p-3 text-center text-emerald-600 font-bold">{h.correct}</td>
                    <td className="p-3 text-center text-rose-600 font-bold">{h.incorrect}</td>
                    <td className="p-3 text-center text-slate-500">{h.unattempted}</td>
                    <td className="p-3 text-right font-semibold text-purple-700">{h.accuracy}</td>
                    <td className="p-3 text-right text-slate-500">{h.timeTaken}</td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
