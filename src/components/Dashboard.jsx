import React, { useState, useEffect } from 'react';

export default function Dashboard({ onStartExam, onViewHistory, history }) {
  const [currentTime, setCurrentTime] = useState('');
  const [countdown, setCountdown] = useState('--h : --m : --s');
  const [isAvailable, setIsAvailable] = useState(false);
  const [practiceUnlocked, setPracticeUnlocked] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => {
      const now = new Date();
      setCurrentTime(now.toLocaleTimeString('en-US', { hour12: true }) + ' IST');

      const target = new Date();
      target.setHours(20, 0, 0, 0); // 8:00 PM IST

      const diff = target.getTime() - now.getTime();
      if (diff > 0 && !practiceUnlocked) {
        const h = Math.floor(diff / (1000 * 60 * 60));
        const m = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const s = Math.floor((diff % (1000 * 60)) / 1000);
        setCountdown(`${String(h).padStart(2, '0')}h : ${String(m).padStart(2, '0')}m : ${String(s).padStart(2, '0')}s`);
        setIsAvailable(false);
      } else {
        setCountdown('00h : 00m : 00s');
        setIsAvailable(true);
      }
    }, 1000);
    return () => clearInterval(timer);
  }, [practiceUnlocked]);

  // Performance calculations
  const totalTests = history.length;
  let avgScore = '--';
  let bestScore = '--';
  let avgAccuracy = '--';

  if (totalTests > 0) {
    const sumScore = history.reduce((acc, h) => acc + parseFloat(h.score), 0);
    const sumAcc = history.reduce((acc, h) => acc + parseFloat(h.accuracy), 0);
    const maxScore = Math.max(...history.map(h => parseFloat(h.score)));
    avgScore = (sumScore / totalTests).toFixed(2);
    bestScore = maxScore.toFixed(2);
    avgAccuracy = (sumAcc / totalTests).toFixed(1) + '%';
  }

  return (
    <div className="max-w-7xl mx-auto p-4 md:p-6 space-y-6">
      {/* Candidate Profile Bar */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-5">
        <div className="flex items-center gap-4">
          <div className="w-16 h-16 rounded-lg bg-slate-100 border-2 border-slate-300 flex flex-col items-center justify-center text-slate-400 font-bold text-xs shrink-0">
            PHOTO
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-lg font-bold text-slate-900">Aadarsh Thakur</h2>
              <span className="px-2 py-0.5 text-[10px] font-semibold bg-blue-100 text-blue-800 rounded">GENERAL / UR</span>
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-x-4 gap-y-0.5 text-xs text-slate-500 mt-1">
              <div>Roll No: <span className="font-mono font-semibold text-slate-700">MPPSC-2026-489102</span></div>
              <div>Application No: <span className="font-mono font-semibold text-slate-700">APP-7182904</span></div>
              <div>Post: <span className="font-semibold text-slate-700">State Services (Prelims)</span></div>
            </div>
          </div>
        </div>

        <button 
          onClick={onViewHistory}
          className="px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold border border-slate-300 transition"
        >
          View Test History
        </button>
      </div>

      {/* Today's Scheduled Examination Card */}
      <div className="bg-white border-2 border-blue-900/20 rounded-xl p-6 shadow-sm">
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4 mb-5">
          <div className="flex items-center gap-2">
            <span className="px-2.5 py-1 rounded text-xs font-bold bg-blue-100 text-blue-900">
              TODAY'S SCHEDULED EXAMINATION
            </span>
            <span className={`px-2.5 py-1 rounded text-xs font-bold border ${isAvailable ? 'bg-emerald-100 text-emerald-900 border-emerald-300' : 'bg-amber-100 text-amber-900 border-amber-300'}`}>
              {isAvailable ? '🟢 Available Now' : '🕒 Scheduled at 8:00 PM IST'}
            </span>
          </div>
          <div className="text-xs text-slate-500">
            Current IST Time: <span className="font-mono font-bold text-slate-700">{currentTime}</span>
          </div>
        </div>

        <div className="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
          <div className="space-y-2 flex-1">
            <h3 className="text-xl md:text-2xl font-black text-slate-900">
              MPPSC Mock Examination — Test 01
            </h3>
            <p className="text-sm text-slate-600 font-medium">
              General Studies Paper-I (Full Length Mock Examination)
            </p>

            <div className="flex flex-wrap items-center gap-4 text-xs text-slate-600 pt-2">
              <div><b className="text-slate-900">Total Questions:</b> 100 MCQs</div>
              <span>•</span>
              <div><b className="text-slate-900">Maximum Marks:</b> 100.00</div>
              <span>•</span>
              <div><b className="text-slate-900">Duration:</b> 120 Minutes</div>
              <span>•</span>
              <div><b className="text-slate-900">Marking:</b> +1.00 / −0.25</div>
            </div>
          </div>

          <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 w-full lg:w-80 flex flex-col items-center justify-center text-center">
            <div className="text-xs font-medium text-slate-500 uppercase tracking-wider">Time to Test Window</div>
            <div className="font-mono text-2xl font-extrabold text-blue-900 my-1">{countdown}</div>
            <div className="text-[11px] text-slate-500 mb-3">Scheduled Daily at 08:00 PM IST</div>

            <button
              onClick={onStartExam}
              className={`w-full py-2.5 px-4 font-bold text-sm rounded-lg shadow-md transition ${isAvailable ? 'bg-emerald-700 hover:bg-emerald-600 text-white' : 'bg-blue-900 hover:bg-blue-800 text-white'}`}
            >
              Attempt Examination Now
            </button>

            {!isAvailable && (
              <button 
                onClick={() => setPracticeUnlocked(true)}
                className="mt-2 text-[11px] text-blue-700 hover:underline font-semibold"
              >
                Unlock Test Now (Practice Mode)
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Performance Summary Grid */}
      <div>
        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">Candidate Summary</h4>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
            <div className="text-xs text-slate-500">Tests Attempted</div>
            <div className="text-2xl font-bold text-slate-900 mt-1">{totalTests}</div>
          </div>
          <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
            <div className="text-xs text-slate-500">Average Score</div>
            <div className="text-2xl font-bold text-blue-900 mt-1">{avgScore}</div>
          </div>
          <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
            <div className="text-xs text-slate-500">Highest Score</div>
            <div className="text-2xl font-bold text-emerald-600 mt-1">{bestScore}</div>
          </div>
          <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
            <div className="text-xs text-slate-500">Average Accuracy</div>
            <div className="text-2xl font-bold text-purple-600 mt-1">{avgAccuracy}</div>
          </div>
        </div>
      </div>

      {/* Recent History Table */}
      <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
        <div className="flex items-center justify-between mb-4">
          <h4 className="font-bold text-sm text-slate-900">Recent Test Attempts</h4>
          <button onClick={onViewHistory} className="text-xs text-blue-700 hover:underline font-semibold">
            View All →
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 text-slate-600 border-b border-slate-200">
              <tr>
                <th className="p-3">Test No.</th>
                <th className="p-3">Date</th>
                <th className="p-3 text-right">Score /100</th>
                <th className="p-3 text-center">Correct</th>
                <th className="p-3 text-center">Incorrect</th>
                <th className="p-3 text-center">Skipped</th>
                <th className="p-3 text-right">Accuracy</th>
                <th className="p-3 text-right">Time Taken</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {history.length === 0 ? (
                <tr>
                  <td colSpan="8" className="p-6 text-center text-slate-400">
                    No attempts recorded yet. Click "Attempt Examination Now" to take Test 01.
                  </td>
                </tr>
              ) : (
                history.slice(0, 5).map((h, i) => (
                  <tr key={i} className="hover:bg-slate-50 transition">
                    <td className="p-3 font-bold text-blue-950">Test {h.testNo}</td>
                    <td className="p-3 text-slate-600">{h.date}</td>
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
