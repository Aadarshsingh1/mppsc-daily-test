import React, { useState, useEffect } from 'react';
import questionsData from './data/questions.json';
import Dashboard from './components/Dashboard';
import ExamHeader from './components/ExamHeader';
import QuestionPanel from './components/QuestionPanel';
import QuestionPalette from './components/QuestionPalette';
import SubmissionModal from './components/SubmissionModal';
import ResultScreen from './components/ResultScreen';
import HistoryScreen from './components/HistoryScreen';

export default function App() {
  const [view, setView] = useState('DASHBOARD'); // 'DASHBOARD' | 'EXAM' | 'RESULT' | 'HISTORY'
  const [currentQIdx, setCurrentQIdx] = useState(0);
  const [language, setLanguage] = useState('both');
  const [responses, setResponses] = useState({});
  const [secondsRemaining, setSecondsRemaining] = useState(120 * 60);
  const [showSubmitModal, setShowSubmitModal] = useState(false);
  const [lastResult, setLastResult] = useState(null);
  const [history, setHistory] = useState([]);

  // Load history & initialize responses
  useEffect(() => {
    const savedHistory = localStorage.getItem('mppsc_exam_history');
    if (savedHistory) {
      try { setHistory(JSON.parse(savedHistory)); } catch(e){}
    }

    const initialResponses = {};
    questionsData.forEach((q, idx) => {
      initialResponses[q.id] = {
        selectedOption: null,
        state: idx === 0 ? 'NOT_ANSWERED' : 'NOT_VISITED'
      };
    });
    setResponses(initialResponses);
  }, []);

  // Timer during exam
  useEffect(() => {
    if (view !== 'EXAM') return;
    const interval = setInterval(() => {
      setSecondsRemaining(prev => {
        if (prev <= 1) {
          clearInterval(interval);
          handleFinalSubmit();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [view]);

  // Option selection
  const handleSelectOption = (optKey) => {
    const qId = questionsData[currentQIdx].id;
    setResponses(prev => ({
      ...prev,
      [qId]: {
        ...prev[qId],
        selectedOption: optKey
      }
    }));
  };

  // Save & Next
  const handleSaveAndNext = () => {
    const qId = questionsData[currentQIdx].id;
    const current = responses[qId];
    const newState = current.selectedOption ? 'ANSWERED' : 'NOT_ANSWERED';

    setResponses(prev => ({
      ...prev,
      [qId]: { ...prev[qId], state: newState }
    }));

    if (currentQIdx < questionsData.length - 1) {
      const nextIdx = currentQIdx + 1;
      setCurrentQIdx(nextIdx);
      const nextId = questionsData[nextIdx].id;
      if (responses[nextId]?.state === 'NOT_VISITED') {
        setResponses(prev => ({
          ...prev,
          [nextId]: { ...prev[nextId], state: 'NOT_ANSWERED' }
        }));
      }
    } else {
      setShowSubmitModal(true);
    }
  };

  // Clear Response
  const handleClearResponse = () => {
    const qId = questionsData[currentQIdx].id;
    setResponses(prev => ({
      ...prev,
      [qId]: {
        ...prev[qId],
        selectedOption: null,
        state: 'NOT_ANSWERED'
      }
    }));
  };

  // Mark for Review & Next
  const handleMarkForReview = () => {
    const qId = questionsData[currentQIdx].id;
    const current = responses[qId];
    const newState = current.selectedOption ? 'ANSWERED_AND_MARKED' : 'MARKED_FOR_REVIEW';

    setResponses(prev => ({
      ...prev,
      [qId]: { ...prev[qId], state: newState }
    }));

    if (currentQIdx < questionsData.length - 1) {
      const nextIdx = currentQIdx + 1;
      setCurrentQIdx(nextIdx);
    } else {
      setShowSubmitModal(true);
    }
  };

  // Previous
  const handlePrevious = () => {
    if (currentQIdx > 0) {
      setCurrentQIdx(prev => prev - 1);
    }
  };

  // Direct jump from palette
  const handleSelectQuestion = (idx) => {
    setCurrentQIdx(idx);
    const qId = questionsData[idx].id;
    if (responses[qId]?.state === 'NOT_VISITED') {
      setResponses(prev => ({
        ...prev,
        [qId]: { ...prev[qId], state: 'NOT_ANSWERED' }
      }));
    }
  };

  // Final Submit
  const handleFinalSubmit = () => {
    setShowSubmitModal(false);

    let correct = 0;
    let incorrect = 0;
    let unattempted = 0;

    questionsData.forEach(q => {
      const sel = responses[q.id]?.selectedOption;
      if (!sel) unattempted++;
      else if (sel === q.correct) correct++;
      else incorrect++;
    });

    const finalScore = (correct * 1.0) - (incorrect * 0.25);
    const attempted = correct + incorrect;
    const accuracy = attempted > 0 ? ((correct / attempted) * 100).toFixed(1) + '%' : '0.0%';
    const timeSpentSec = (120 * 60) - secondsRemaining;
    const timeSpentStr = `${Math.floor(timeSpentSec / 60)}m ${timeSpentSec % 60}s`;

    const record = {
      testNo: "01",
      date: new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }),
      dateTime: new Date().toLocaleString(),
      score: finalScore.toFixed(2),
      correct,
      incorrect,
      unattempted,
      accuracy,
      timeTaken: timeSpentStr,
      responses,
      comparisonNote: history.length > 0 ? `Previous score was ${history[0].score}` : 'First test recorded.'
    };

    const newHistory = [record, ...history];
    setHistory(newHistory);
    localStorage.setItem('mppsc_exam_history', JSON.stringify(newHistory));

    setLastResult(record);
    setView('RESULT');
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800 flex flex-col font-sans">
      {view !== 'EXAM' && (
        <header className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-40">
          <div className="max-w-7xl mx-auto px-4 py-2.5 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-11 h-11 rounded-lg bg-blue-900 flex items-center justify-center text-white font-bold text-lg">
                MP
              </div>
              <div>
                <div className="text-xs uppercase font-bold text-slate-500">Madhya Pradesh Public Service Commission</div>
                <h1 className="text-base md:text-lg font-bold text-blue-950">Online Examination Portal</h1>
              </div>
            </div>
            <div className="text-xs font-semibold bg-blue-50 text-blue-900 border border-blue-200 px-3 py-1.5 rounded-md">
              Candidate: Aadarsh Thakur
            </div>
          </div>
        </header>
      )}

      {view === 'DASHBOARD' && (
        <Dashboard
          onStartExam={() => setView('EXAM')}
          onViewHistory={() => setView('HISTORY')}
          history={history}
        />
      )}

      {view === 'EXAM' && (
        <div className="flex-1 flex flex-col h-screen overflow-hidden">
          <ExamHeader
            secondsRemaining={secondsRemaining}
            onOpenSubmit={() => setShowSubmitModal(true)}
            language={language}
            onChangeLanguage={setLanguage}
          />
          <div className="flex-1 flex flex-col lg:flex-row overflow-hidden">
            <QuestionPanel
              question={questionsData[currentQIdx]}
              response={responses[questionsData[currentQIdx].id] || {}}
              language={language}
              onSelectOption={handleSelectOption}
              onSaveAndNext={handleSaveAndNext}
              onClearResponse={handleClearResponse}
              onMarkForReview={handleMarkForReview}
              onPrevious={handlePrevious}
              hasPrevious={currentQIdx > 0}
            />
            <QuestionPalette
              questions={questionsData}
              responses={responses}
              currentQIdx={currentQIdx}
              onSelectQuestion={handleSelectQuestion}
              onOpenSubmit={() => setShowSubmitModal(true)}
            />
          </div>
          {showSubmitModal && (
            <SubmissionModal
              responses={responses}
              onCancel={() => setShowSubmitModal(false)}
              onConfirm={handleFinalSubmit}
            />
          )}
        </div>
      )}

      {view === 'RESULT' && lastResult && (
        <ResultScreen
          result={lastResult}
          questions={questionsData}
          onReturnDashboard={() => setView('DASHBOARD')}
          onViewHistory={() => setView('HISTORY')}
        />
      )}

      {view === 'HISTORY' && (
        <HistoryScreen
          history={history}
          onReturnDashboard={() => setView('DASHBOARD')}
        />
      )}
    </div>
  );
}
