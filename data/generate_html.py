# -*- coding: utf-8 -*-
import json
import os

json_path = r"c:\Users\hp\Documents\antigravity\wonderful-noether\data\mppsc_mock_01.json"
with open(json_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MPPSC Prelims Mock Test 01 — General Studies Paper 1</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    :root {
      --bg: #0f172a;
      --card-bg: #1e293b;
      --border-color: #334155;
      --accent: #3b82f6;
      --accent-hover: #2563eb;
      --text: #f8fafc;
      --text-muted: #94a3b8;
    }
    body {
      font-family: system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
      background-color: var(--bg);
      color: var(--text);
    }
    .custom-scroll::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .custom-scroll::-webkit-scrollbar-thumb {
      background: #475569;
      border-radius: 4px;
    }
  </style>
</head>
<body class="min-h-screen bg-slate-950 text-slate-100 flex flex-col">

  <!-- Top Navigation Bar -->
  <header class="sticky top-0 z-40 bg-slate-900/90 backdrop-blur border-b border-slate-800 px-4 py-3 shadow-md">
    <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3">
      <!-- Title & Branding -->
      <div class="flex items-center gap-3">
        <div class="h-10 w-10 rounded-xl bg-gradient-to-tr from-amber-500 to-red-600 flex items-center justify-center font-bold text-white shadow-lg shadow-orange-500/20">
          MP
        </div>
        <div>
          <h1 class="font-bold text-base md:text-lg text-white leading-tight">MPPSC Prelims Mock Test 01</h1>
          <p class="text-xs text-slate-400">General Studies Paper-I • 100 MCQs • +1 / -0.25 Marking</p>
        </div>
      </div>

      <!-- Live Counters & Timer -->
      <div class="flex items-center gap-3 md:gap-6">
        <!-- Timer -->
        <div class="flex items-center gap-2 bg-slate-800/90 border border-slate-700 px-3 py-1.5 rounded-lg">
          <svg class="w-4 h-4 text-amber-400 animate-pulse" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <span id="timerDisplay" class="font-mono font-bold text-amber-400 text-sm md:text-base">120:00</span>
          <button id="toggleTimerBtn" class="text-xs text-slate-400 hover:text-white px-1">⏸</button>
        </div>

        <!-- Answered Counter -->
        <div class="hidden sm:flex items-center gap-2 text-xs bg-slate-800 px-3 py-1.5 rounded-lg border border-slate-700">
          <span class="text-slate-400">Answered:</span>
          <span id="answeredCount" class="font-bold text-emerald-400 text-sm">0</span>
          <span class="text-slate-500">/ 100</span>
        </div>

        <!-- Language Switcher -->
        <div class="flex items-center bg-slate-800 border border-slate-700 rounded-lg p-0.5 text-xs">
          <button onclick="setLanguage('both')" id="langBothBtn" class="px-2 py-1 rounded bg-blue-600 font-medium text-white transition">Both</button>
          <button onclick="setLanguage('hi')" id="langHiBtn" class="px-2 py-1 rounded text-slate-300 hover:text-white transition">हिन्दी</button>
          <button onclick="setLanguage('en')" id="langEnBtn" class="px-2 py-1 rounded text-slate-300 hover:text-white transition">English</button>
        </div>

        <!-- Submit Button -->
        <button id="submitTestTopBtn" onclick="openSubmitModal()" class="bg-gradient-to-r from-red-600 to-rose-600 hover:from-red-500 hover:to-rose-500 text-white font-medium text-xs md:text-sm px-4 py-2 rounded-lg shadow-lg shadow-red-900/30 transition transform active:scale-95">
          Submit Test
        </button>
      </div>
    </div>
  </header>

  <!-- Main Content Layout -->
  <main class="flex-1 max-w-7xl w-full mx-auto p-3 md:p-6 grid grid-cols-1 lg:grid-cols-4 gap-6">

    <!-- Left / Center: Question Area (Takes 3 Cols on lg) -->
    <div id="testArea" class="lg:col-span-3 flex flex-col space-y-4">

      <!-- Unit Selector Pills -->
      <div class="bg-slate-900/80 border border-slate-800 rounded-xl p-2.5 flex items-center gap-1.5 overflow-x-auto custom-scroll text-xs">
        <span class="text-slate-400 font-semibold px-2 shrink-0">Units:</span>
        <button onclick="filterUnit('All')" id="unitBtn-All" class="unit-filter-btn px-2.5 py-1 rounded-lg bg-blue-600 text-white shrink-0 font-medium transition">All Units</button>
        <button onclick="filterUnit('Unit 1')" id="unitBtn-Unit 1" class="unit-filter-btn px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 shrink-0 transition">U1: MP Hist</button>
        <button onclick="filterUnit('Unit 2')" id="unitBtn-Unit 2" class="unit-filter-btn px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 shrink-0 transition">U2: Ind Hist</button>
        <button onclick="filterUnit('Unit 3')" id="unitBtn-Unit 3" class="unit-filter-btn px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 shrink-0 transition">U3: MP Geog</button>
        <button onclick="filterUnit('Unit 4')" id="unitBtn-Unit 4" class="unit-filter-btn px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 shrink-0 transition">U4: World/Ind Geog</button>
        <button onclick="filterUnit('Unit 5')" id="unitBtn-Unit 5" class="unit-filter-btn px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 shrink-0 transition">U5: MP Polity/Econ</button>
        <button onclick="filterUnit('Unit 6')" id="unitBtn-Unit 6" class="unit-filter-btn px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 shrink-0 transition">U6: Ind Polity/Econ</button>
        <button onclick="filterUnit('Unit 7')" id="unitBtn-Unit 7" class="unit-filter-btn px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 shrink-0 transition">U7: Sci/Tech</button>
        <button onclick="filterUnit('Unit 8')" id="unitBtn-Unit 8" class="unit-filter-btn px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 shrink-0 transition">U8: Current/Sports</button>
        <button onclick="filterUnit('Unit 9')" id="unitBtn-Unit 9" class="unit-filter-btn px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 shrink-0 transition">U9: ICT/AI</button>
        <button onclick="filterUnit('Unit 10')" id="unitBtn-Unit 10" class="unit-filter-btn px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 shrink-0 transition">U10: Commissions</button>
      </div>

      <!-- Question Card Container -->
      <div id="questionCard" class="bg-slate-900 border border-slate-800 rounded-2xl p-5 md:p-7 shadow-xl flex-1 flex flex-col justify-between">
        <!-- Header of Question Card -->
        <div>
          <div class="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
            <div class="flex items-center gap-2">
              <span id="qBadge" class="bg-blue-900/60 text-blue-300 border border-blue-700 text-xs px-2.5 py-1 rounded-full font-bold">
                Question 1 of 100
              </span>
              <span id="unitBadge" class="text-xs text-slate-400 bg-slate-800/80 px-2.5 py-1 rounded-full border border-slate-700">
                Unit 1: MP History, Culture & Literature
              </span>
            </div>
            <div class="flex items-center gap-2">
              <button id="flagBtn" onclick="toggleFlag()" class="text-xs flex items-center gap-1.5 px-3 py-1 rounded-lg border border-slate-700 text-slate-400 hover:text-amber-400 hover:border-amber-500/50 transition">
                <span id="flagIcon">🏳️</span>
                <span id="flagText">Review Later</span>
              </button>
            </div>
          </div>

          <!-- Question Texts (English & Hindi) -->
          <div class="space-y-4 mb-6">
            <div id="qTextEn" class="text-base md:text-lg font-medium text-slate-100 leading-relaxed">
              <!-- English text -->
            </div>
            <div id="qTextHi" class="text-base md:text-lg font-medium text-amber-200/90 leading-relaxed bg-slate-800/40 p-3 rounded-xl border border-slate-800">
              <!-- Hindi text -->
            </div>
          </div>

          <!-- Options List -->
          <div id="optionsContainer" class="space-y-3">
            <!-- 4 Options dynamically injected -->
          </div>
        </div>

        <!-- Bottom Action Bar for Current Question -->
        <div class="border-t border-slate-800 pt-5 mt-6 flex flex-wrap items-center justify-between gap-3">
          <div class="flex items-center gap-2">
            <button onclick="prevQuestion()" id="prevBtn" class="flex items-center gap-1.5 px-4 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 rounded-xl text-sm font-medium transition text-slate-200 disabled:opacity-40">
              ← Previous
            </button>
            <button onclick="nextQuestion()" id="nextBtn" class="flex items-center gap-1.5 px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-xl text-sm font-medium transition text-white shadow-md shadow-blue-900/30">
              Next →
            </button>
          </div>

          <div class="flex items-center gap-2">
            <button onclick="clearResponse()" class="text-xs text-rose-400 hover:text-rose-300 px-3 py-2 rounded-lg hover:bg-rose-950/40 border border-transparent hover:border-rose-900/50 transition">
              Clear Choice
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Right Side: Question Palette & Overview -->
    <div class="lg:col-span-1 space-y-4">
      <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
        <h3 class="font-bold text-sm text-slate-200 mb-3 flex items-center justify-between">
          <span>Question Palette</span>
          <span class="text-xs text-slate-400 font-normal">100 MCQs</span>
        </h3>

        <!-- Status Legend -->
        <div class="grid grid-cols-2 gap-2 text-xs mb-3 pb-3 border-b border-slate-800 text-slate-300">
          <div class="flex items-center gap-1.5">
            <span class="w-3 h-3 rounded bg-emerald-500"></span>
            <span>Answered (<span id="legendAnswered">0</span>)</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="w-3 h-3 rounded bg-amber-500"></span>
            <span>Flagged (<span id="legendFlagged">0</span>)</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="w-3 h-3 rounded bg-slate-700"></span>
            <span>Unanswered (<span id="legendUnanswered">100</span>)</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="w-3 h-3 rounded ring-2 ring-blue-400 bg-slate-800"></span>
            <span>Current</span>
          </div>
        </div>

        <!-- 100-Question Grid Buttons -->
        <div id="paletteGrid" class="grid grid-cols-5 sm:grid-cols-10 lg:grid-cols-5 gap-1.5 max-h-[380px] overflow-y-auto p-1 custom-scroll">
          <!-- 100 numbered buttons generated by JS -->
        </div>

        <!-- Quick Submit in Sidebar -->
        <div class="mt-4 pt-3 border-t border-slate-800">
          <button onclick="openSubmitModal()" class="w-full py-2.5 px-4 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 font-semibold text-xs md:text-sm text-white rounded-xl shadow-lg transition">
            Review & Final Submit
          </button>
        </div>
      </div>
    </div>
  </main>

  <!-- Submit Confirmation Modal -->
  <div id="submitModal" class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4 hidden">
    <div class="bg-slate-900 border border-slate-700 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
      <div class="flex items-center gap-3 text-amber-400">
        <svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
        </svg>
        <h3 class="text-lg font-bold text-white">Confirm Test Submission</h3>
      </div>
      <p class="text-sm text-slate-300">
        Are you ready to submit your test? Answers cannot be changed once submitted.
      </p>

      <div class="bg-slate-800/80 rounded-xl p-3 grid grid-cols-3 gap-2 text-center text-xs">
        <div class="p-2 bg-slate-900/60 rounded-lg">
          <div class="text-slate-400">Attempted</div>
          <div id="modalAttempted" class="text-base font-bold text-emerald-400">0</div>
        </div>
        <div class="p-2 bg-slate-900/60 rounded-lg">
          <div class="text-slate-400">Flagged</div>
          <div id="modalFlagged" class="text-base font-bold text-amber-400">0</div>
        </div>
        <div class="p-2 bg-slate-900/60 rounded-lg">
          <div class="text-slate-400">Unattempted</div>
          <div id="modalUnattempted" class="text-base font-bold text-rose-400">100</div>
        </div>
      </div>

      <div class="flex items-center justify-end gap-3 pt-2">
        <button onclick="closeSubmitModal()" class="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium rounded-xl transition">
          Return to Test
        </button>
        <button onclick="finalizeSubmission()" class="px-4 py-2 bg-red-600 hover:bg-red-500 text-white text-xs font-semibold rounded-xl shadow-lg transition">
          Confirm & Submit Now
        </button>
      </div>
    </div>
  </div>

  <!-- Results Dashboard View (Hidden until submission) -->
  <div id="resultsDashboard" class="hidden max-w-7xl w-full mx-auto p-4 md:p-6 space-y-6">
    <!-- Score Hero Card -->
    <div class="bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 border border-slate-700 rounded-3xl p-6 md:p-8 shadow-2xl relative overflow-hidden">
      <div class="flex flex-col md:flex-row items-center justify-between gap-6 relative z-10">
        <div class="space-y-2 text-center md:text-left">
          <div class="inline-block bg-blue-900/50 text-blue-300 border border-blue-700/60 text-xs px-3 py-1 rounded-full font-semibold">
            MPPSC Prelims Mock Test 01 • Evaluation Report
          </div>
          <h2 class="text-2xl md:text-3xl font-extrabold text-white">Your Examination Performance</h2>
          <p class="text-xs md:text-sm text-slate-300 max-w-xl">
            Calculated under requested marking rules: <span class="text-emerald-400 font-semibold">+1 for correct</span>, <span class="text-rose-400 font-semibold">-0.25 for incorrect</span>, and <span class="text-slate-400 font-semibold">0 for skipped</span>.
          </p>
        </div>

        <!-- Big Score Badge -->
        <div class="bg-slate-950/80 border border-slate-700/80 rounded-2xl p-5 text-center min-w-[180px] shadow-inner">
          <div class="text-xs text-slate-400 uppercase tracking-wider font-semibold">Final Score</div>
          <div id="finalScoreVal" class="text-4xl md:text-5xl font-black text-amber-400 my-1">0.00</div>
          <div class="text-xs text-slate-400">Out of 100.00 Marks</div>
        </div>
      </div>

      <!-- Key Metrics Row -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 pt-6 border-t border-slate-800 text-center">
        <div class="bg-slate-900/60 border border-slate-800 rounded-xl p-3">
          <div class="text-xs text-slate-400">Accuracy</div>
          <div id="resAccuracy" class="text-xl font-bold text-blue-400 mt-1">0%</div>
        </div>
        <div class="bg-slate-900/60 border border-slate-800 rounded-xl p-3">
          <div class="text-xs text-slate-400">Correct (+1)</div>
          <div id="resCorrect" class="text-xl font-bold text-emerald-400 mt-1">0</div>
        </div>
        <div class="bg-slate-900/60 border border-slate-800 rounded-xl p-3">
          <div class="text-xs text-slate-400">Incorrect (-0.25)</div>
          <div id="resIncorrect" class="text-xl font-bold text-rose-400 mt-1">0</div>
        </div>
        <div class="bg-slate-900/60 border border-slate-800 rounded-xl p-3">
          <div class="text-xs text-slate-400">Unattempted</div>
          <div id="resUnattempted" class="text-xl font-bold text-slate-400 mt-1">0</div>
        </div>
      </div>

      <!-- Action Button: Copy Summary for Assistant -->
      <div class="mt-6 flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-slate-800">
        <span class="text-xs text-slate-400">Save or send your test result to track historical progress:</span>
        <button onclick="copySubmissionString()" id="copySummaryBtn" class="flex items-center gap-2 px-4 py-2 bg-slate-800 hover:bg-slate-700 text-white rounded-xl text-xs font-semibold border border-slate-600 transition">
          📋 Copy Score Summary for AI Assistant
        </button>
      </div>
    </div>

    <!-- Syllabus Unit-by-Unit Performance Table -->
    <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
      <h3 class="text-base font-bold text-white mb-3 flex items-center gap-2">
        <span>📊 Syllabus Unit-wise Performance Analysis</span>
      </h3>
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-800/80 text-slate-300 border-b border-slate-700">
            <tr>
              <th class="p-3">Syllabus Unit (GS Paper 1)</th>
              <th class="p-3 text-center">Questions</th>
              <th class="p-3 text-center text-emerald-400">Correct</th>
              <th class="p-3 text-center text-rose-400">Incorrect</th>
              <th class="p-3 text-center text-slate-400">Skipped</th>
              <th class="p-3 text-center text-amber-400">Unit Score</th>
              <th class="p-3 text-center text-blue-400">Accuracy</th>
            </tr>
          </thead>
          <tbody id="unitAnalysisTableBody" class="divide-y divide-slate-800">
            <!-- Injected by JS -->
          </tbody>
        </table>
      </div>
    </div>

    <!-- Solutions & Explanations Header -->
    <div class="flex flex-wrap items-center justify-between gap-3 pt-4">
      <h3 class="text-lg font-bold text-white flex items-center gap-2">
        <span>📖 Question-by-Question Detailed Solutions (100 Questions)</span>
      </h3>
      <div class="flex items-center gap-1.5 text-xs">
        <button onclick="filterReview('all')" id="revFilter-all" class="px-3 py-1.5 rounded-lg bg-blue-600 text-white font-medium">All (100)</button>
        <button onclick="filterReview('correct')" id="revFilter-correct" class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white">Correct</button>
        <button onclick="filterReview('incorrect')" id="revFilter-incorrect" class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white">Incorrect</button>
        <button onclick="filterReview('unattempted')" id="revFilter-unattempted" class="px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white">Skipped</button>
      </div>
    </div>

    <!-- Questions Detailed Review List -->
    <div id="solutionsList" class="space-y-4">
      <!-- 100 review cards injected by JS -->
    </div>
  </div>

  <script>
    const questionsData = """ + json.dumps(questions, ensure_ascii=False) + """;

    // State Variables
    let currentQIndex = 0;
    let userAnswers = {}; // { qId: 'A' | 'B' | 'C' | 'D' }
    let flaggedQuestions = new Set();
    let currentLang = 'both'; // 'both', 'hi', 'en'
    let currentUnitFilter = 'All';
    let filteredIndices = questionsData.map((_, i) => i);
    let isSubmitted = false;

    // Timer variables
    let totalSeconds = 120 * 60; // 120 minutes
    let timerRunning = true;
    let timerInterval = null;

    // Initialize
    window.addEventListener('DOMContentLoaded', () => {
      // Load cached state if exists
      const savedAnswers = localStorage.getItem('mppsc_mock_01_answers');
      if (savedAnswers) {
        try { userAnswers = JSON.parse(savedAnswers); } catch(e){}
      }
      buildPalette();
      renderQuestion();
      updateCounters();
      startTimer();
    });

    // Timer logic
    function startTimer() {
      if (timerInterval) clearInterval(timerInterval);
      timerInterval = setInterval(() => {
        if (!timerRunning || isSubmitted) return;
        if (totalSeconds > 0) {
          totalSeconds--;
          updateTimerDisplay();
        } else {
          clearInterval(timerInterval);
          alert('Time has expired! Submitting test automatically.');
          finalizeSubmission();
        }
      }, 1000);
    }

    function updateTimerDisplay() {
      const mins = Math.floor(totalSeconds / 60);
      const secs = totalSeconds % 60;
      const display = String(mins).padStart(2, '0') + ':' + String(secs).padStart(2, '0');
      document.getElementById('timerDisplay').innerText = display;
    }

    document.getElementById('toggleTimerBtn').addEventListener('click', () => {
      timerRunning = !timerRunning;
      document.getElementById('toggleTimerBtn').innerText = timerRunning ? '⏸' : '▶';
    });

    // Language switcher
    function setLanguage(lang) {
      currentLang = lang;
      ['both', 'hi', 'en'].forEach(l => {
        const btn = document.getElementById('lang' + l.charAt(0).toUpperCase() + l.slice(1) + 'Btn');
        if (l === lang) {
          btn.className = "px-2 py-1 rounded bg-blue-600 font-medium text-white transition";
        } else {
          btn.className = "px-2 py-1 rounded text-slate-300 hover:text-white transition";
        }
      });
      renderQuestion();
    }

    // Unit Filter
    function filterUnit(unit) {
      currentUnitFilter = unit;
      document.querySelectorAll('.unit-filter-btn').forEach(btn => {
        if (btn.id === 'unitBtn-' + unit) {
          btn.className = "unit-filter-btn px-2.5 py-1 rounded-lg bg-blue-600 text-white shrink-0 font-medium transition";
        } else {
          btn.className = "unit-filter-btn px-2.5 py-1 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 shrink-0 transition";
        }
      });

      if (unit === 'All') {
        filteredIndices = questionsData.map((_, i) => i);
      } else {
        filteredIndices = questionsData
          .map((q, idx) => ({ q, idx }))
          .filter(item => item.q.unit.startsWith(unit))
          .map(item => item.idx);
      }

      if (!filteredIndices.includes(currentQIndex)) {
        currentQIndex = filteredIndices[0] || 0;
      }
      renderQuestion();
    }

    // Question Rendering
    function renderQuestion() {
      const q = questionsData[currentQIndex];
      const qId = q.id;

      // Update badges
      document.getElementById('qBadge').innerText = `Question ${qId} of 100`;
      document.getElementById('unitBadge').innerText = q.unit;

      // Update question text based on language
      const qEn = document.getElementById('qTextEn');
      const qHi = document.getElementById('qTextHi');

      if (currentLang === 'both') {
        qEn.style.display = 'block';
        qHi.style.display = 'block';
        qEn.innerHTML = `<span class="text-blue-400 font-bold mr-1">Q${qId}.</span> ${q.question_en}`;
        qHi.innerHTML = `<span class="text-amber-400 font-bold mr-1">प्र. ${qId}.</span> ${q.question_hi}`;
      } else if (currentLang === 'hi') {
        qEn.style.display = 'none';
        qHi.style.display = 'block';
        qHi.innerHTML = `<span class="text-amber-400 font-bold mr-1">प्र. ${qId}.</span> ${q.question_hi}`;
      } else {
        qEn.style.display = 'block';
        qHi.style.display = 'none';
        qEn.innerHTML = `<span class="text-blue-400 font-bold mr-1">Q${qId}.</span> ${q.question_en}`;
      }

      // Render 4 Options
      const optionsContainer = document.getElementById('optionsContainer');
      optionsContainer.innerHTML = '';

      const letters = ['A', 'B', 'C', 'D'];
      letters.forEach((optKey, idx) => {
        const isSelected = userAnswers[qId] === optKey;
        const optEn = q.options_en[idx];
        const optHi = q.options_hi[idx];

        const optDiv = document.createElement('div');
        optDiv.className = `p-3.5 rounded-xl border cursor-pointer transition flex items-start gap-3 select-none ${
          isSelected
            ? 'bg-blue-900/40 border-blue-500 shadow-md shadow-blue-950/50'
            : 'bg-slate-800/60 border-slate-700 hover:border-slate-600 hover:bg-slate-800'
        }`;
        optDiv.onclick = () => selectOption(qId, optKey);

        let content = '';
        if (currentLang === 'both') {
          content = `
            <div class="flex-1">
              <div class="text-sm font-medium ${isSelected ? 'text-blue-200' : 'text-slate-200'}">${optEn}</div>
              <div class="text-xs ${isSelected ? 'text-blue-300' : 'text-amber-200/80'} mt-0.5">${optHi}</div>
            </div>
          `;
        } else if (currentLang === 'hi') {
          content = `<div class="flex-1 text-sm font-medium ${isSelected ? 'text-blue-200' : 'text-amber-200'}">${optHi}</div>`;
        } else {
          content = `<div class="flex-1 text-sm font-medium ${isSelected ? 'text-blue-200' : 'text-slate-200'}">${optEn}</div>`;
        }

        optDiv.innerHTML = `
          <div class="w-6 h-6 rounded-full flex items-center justify-center font-bold text-xs shrink-0 mt-0.5 ${
            isSelected ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300'
          }">${optKey}</div>
          ${content}
        `;
        optionsContainer.appendChild(optDiv);
      });

      // Update Review flag button state
      const isFlagged = flaggedQuestions.has(qId);
      const flagBtn = document.getElementById('flagBtn');
      if (isFlagged) {
        flagBtn.className = "text-xs flex items-center gap-1.5 px-3 py-1 rounded-lg border border-amber-500 bg-amber-950/40 text-amber-300 transition";
        document.getElementById('flagIcon').innerText = "🚩";
        document.getElementById('flagText').innerText = "Flagged";
      } else {
        flagBtn.className = "text-xs flex items-center gap-1.5 px-3 py-1 rounded-lg border border-slate-700 text-slate-400 hover:text-amber-400 transition";
        document.getElementById('flagIcon').innerText = "🏳️";
        document.getElementById('flagText').innerText = "Review Later";
      }

      // Prev/Next buttons
      document.getElementById('prevBtn').disabled = currentQIndex === 0;
      document.getElementById('nextBtn').innerText = currentQIndex === questionsData.length - 1 ? 'Review All' : 'Next →';

      updatePaletteCurrent();
    }

    function selectOption(qId, optKey) {
      userAnswers[qId] = optKey;
      localStorage.setItem('mppsc_mock_01_answers', JSON.stringify(userAnswers));
      renderQuestion();
      updateCounters();
      updatePaletteItem(qId);
    }

    function clearResponse() {
      const qId = questionsData[currentQIndex].id;
      delete userAnswers[qId];
      localStorage.setItem('mppsc_mock_01_answers', JSON.stringify(userAnswers));
      renderQuestion();
      updateCounters();
      updatePaletteItem(qId);
    }

    function toggleFlag() {
      const qId = questionsData[currentQIndex].id;
      if (flaggedQuestions.has(qId)) {
        flaggedQuestions.delete(qId);
      } else {
        flaggedQuestions.add(qId);
      }
      renderQuestion();
      updateCounters();
      updatePaletteItem(qId);
    }

    function nextQuestion() {
      if (currentQIndex < questionsData.length - 1) {
        currentQIndex++;
        renderQuestion();
      } else {
        openSubmitModal();
      }
    }

    function prevQuestion() {
      if (currentQIndex > 0) {
        currentQIndex--;
        renderQuestion();
      }
    }

    function jumpToQuestion(idx) {
      currentQIndex = idx;
      renderQuestion();
    }

    // Palette Generation
    function buildPalette() {
      const grid = document.getElementById('paletteGrid');
      grid.innerHTML = '';
      questionsData.forEach((q, idx) => {
        const btn = document.createElement('button');
        btn.id = 'palBtn-' + q.id;
        btn.className = getPaletteClass(q.id, idx);
        btn.innerText = q.id;
        btn.onclick = () => jumpToQuestion(idx);
        grid.appendChild(btn);
      });
    }

    function getPaletteClass(qId, idx) {
      const isCurrent = idx === currentQIndex;
      const isAnswered = !!userAnswers[qId];
      const isFlagged = flaggedQuestions.has(qId);

      let base = "h-8 rounded-lg text-xs font-semibold flex items-center justify-center transition ";

      if (isCurrent) base += "ring-2 ring-blue-400 font-bold ";

      if (isFlagged) {
        base += "bg-amber-600 text-white";
      } else if (isAnswered) {
        base += "bg-emerald-600 text-white";
      } else {
        base += "bg-slate-800 text-slate-300 hover:bg-slate-700";
      }
      return base;
    }

    function updatePaletteItem(qId) {
      const idx = qId - 1;
      const btn = document.getElementById('palBtn-' + qId);
      if (btn) btn.className = getPaletteClass(qId, idx);
    }

    function updatePaletteCurrent() {
      questionsData.forEach((q, idx) => {
        updatePaletteItem(q.id);
      });
    }

    function updateCounters() {
      const answeredCount = Object.keys(userAnswers).length;
      const flaggedCount = flaggedQuestions.size;
      const unattemptedCount = questionsData.length - answeredCount;

      document.getElementById('answeredCount').innerText = answeredCount;
      document.getElementById('legendAnswered').innerText = answeredCount;
      document.getElementById('legendFlagged').innerText = flaggedCount;
      document.getElementById('legendUnanswered').innerText = unattemptedCount;
    }

    // Submission Modal
    function openSubmitModal() {
      const answeredCount = Object.keys(userAnswers).length;
      document.getElementById('modalAttempted').innerText = answeredCount;
      document.getElementById('modalFlagged').innerText = flaggedQuestions.size;
      document.getElementById('modalUnattempted').innerText = 100 - answeredCount;
      document.getElementById('submitModal').classList.remove('hidden');
    }

    function closeSubmitModal() {
      document.getElementById('submitModal').classList.add('hidden');
    }

    // Finalize Submission & Compute Results
    function finalizeSubmission() {
      isSubmitted = true;
      closeSubmitModal();

      // Calculation of MPPSC Test Score
      let correctCount = 0;
      let incorrectCount = 0;
      let unattemptedCount = 0;

      // Unit wise tracking
      const unitStats = {};

      questionsData.forEach(q => {
        const u = q.unit;
        if (!unitStats[u]) {
          unitStats[u] = { total: 0, correct: 0, incorrect: 0, unattempted: 0 };
        }
        unitStats[u].total++;

        const userAns = userAnswers[q.id];
        if (!userAns) {
          unattemptedCount++;
          unitStats[u].unattempted++;
        } else if (userAns === q.correct) {
          correctCount++;
          unitStats[u].correct++;
        } else {
          incorrectCount++;
          unitStats[u].incorrect++;
        }
      });

      // Requested Marking: +1 correct, -0.25 incorrect
      const finalScore = (correctCount * 1.0) - (incorrectCount * 0.25);
      const attempted = correctCount + incorrectCount;
      const accuracy = attempted > 0 ? ((correctCount / attempted) * 100).toFixed(1) : "N/A";

      // Hide test UI, show dashboard
      document.getElementById('testArea').classList.add('hidden');
      document.getElementById('paletteGrid').parentElement.classList.add('hidden');
      document.getElementById('submitTestTopBtn').classList.add('hidden');
      document.getElementById('resultsDashboard').classList.remove('hidden');

      // Populate Hero Cards
      document.getElementById('finalScoreVal').innerText = finalScore.toFixed(2);
      document.getElementById('resAccuracy').innerText = accuracy === "N/A" ? "N/A" : accuracy + "%";
      document.getElementById('resCorrect').innerText = correctCount;
      document.getElementById('resIncorrect').innerText = incorrectCount;
      document.getElementById('resUnattempted').innerText = unattemptedCount;

      // Populate Unit-wise Table
      const tbody = document.getElementById('unitAnalysisTableBody');
      tbody.innerHTML = '';
      Object.keys(unitStats).forEach(uName => {
        const s = unitStats[uName];
        const uScore = (s.correct * 1.0) - (s.incorrect * 0.25);
        const uAtt = s.correct + s.incorrect;
        const uAcc = uAtt > 0 ? ((s.correct / uAtt) * 100).toFixed(1) + '%' : 'N/A';

        const row = document.createElement('tr');
        row.className = "hover:bg-slate-800/40 transition";
        row.innerHTML = `
          <td class="p-3 font-medium text-slate-200">${uName}</td>
          <td class="p-3 text-center text-slate-400">${s.total}</td>
          <td class="p-3 text-center text-emerald-400 font-semibold">${s.correct}</td>
          <td class="p-3 text-center text-rose-400 font-semibold">${s.incorrect}</td>
          <td class="p-3 text-center text-slate-400">${s.unattempted}</td>
          <td class="p-3 text-center text-amber-400 font-bold">${uScore.toFixed(2)}</td>
          <td class="p-3 text-center text-blue-400 font-medium">${uAcc}</td>
        `;
        tbody.appendChild(row);
      });

      // Render 100 Detailed Solutions
      renderSolutions('all');

      // Scroll to results top
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Solutions rendering
    let currentReviewFilter = 'all';

    function filterReview(mode) {
      currentReviewFilter = mode;
      ['all', 'correct', 'incorrect', 'unattempted'].forEach(m => {
        const btn = document.getElementById('revFilter-' + m);
        if (m === mode) {
          btn.className = "px-3 py-1.5 rounded-lg bg-blue-600 text-white font-medium";
        } else {
          btn.className = "px-3 py-1.5 rounded-lg bg-slate-800 text-slate-300 hover:text-white";
        }
      });
      renderSolutions(mode);
    }

    function renderSolutions(mode) {
      const list = document.getElementById('solutionsList');
      list.innerHTML = '';

      questionsData.forEach(q => {
        const userAns = userAnswers[q.id];
        const isCorrect = userAns === q.correct;
        const isSkipped = !userAns;

        if (mode === 'correct' && !isCorrect) return;
        if (mode === 'incorrect' && (isCorrect || isSkipped)) return;
        if (mode === 'unattempted' && !isSkipped) return;

        let statusBadge = '';
        let borderClass = 'border-slate-800';

        if (isSkipped) {
          statusBadge = '<span class="bg-slate-800 text-slate-400 px-2.5 py-0.5 rounded-full text-xs font-semibold">Skipped (0)</span>';
        } else if (isCorrect) {
          statusBadge = '<span class="bg-emerald-950 text-emerald-400 border border-emerald-800 px-2.5 py-0.5 rounded-full text-xs font-semibold">Correct (+1)</span>';
          borderClass = 'border-emerald-900/40';
        } else {
          statusBadge = '<span class="bg-rose-950 text-rose-400 border border-rose-800 px-2.5 py-0.5 rounded-full text-xs font-semibold">Incorrect (-0.25)</span>';
          borderClass = 'border-rose-900/40';
        }

        const card = document.createElement('div');
        card.className = `bg-slate-900 border ${borderClass} rounded-2xl p-5 shadow-lg space-y-3`;

        const letters = ['A', 'B', 'C', 'D'];
        let optionsHtml = '';
        letters.forEach((l, idx) => {
          let optStyle = 'border-slate-800 bg-slate-800/40 text-slate-300';
          if (l === q.correct) {
            optStyle = 'border-emerald-600 bg-emerald-950/40 text-emerald-200 font-semibold';
          } else if (userAns === l && !isCorrect) {
            optStyle = 'border-rose-600 bg-rose-950/40 text-rose-200';
          }

          optionsHtml += `
            <div class="p-2.5 rounded-xl border ${optStyle} flex items-start gap-2 text-xs">
              <span class="font-bold shrink-0">${l}.</span>
              <div class="flex-1">
                <div>${q.options_en[idx]}</div>
                <div class="text-slate-400 mt-0.5">${q.options_hi[idx]}</div>
              </div>
            </div>
          `;
        });

        card.innerHTML = `
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800 pb-2">
            <div class="flex items-center gap-2">
              <span class="font-bold text-sm text-white">Q${q.id}</span>
              <span class="text-xs text-slate-400 bg-slate-800 px-2 py-0.5 rounded">${q.unit}</span>
            </div>
            <div>${statusBadge}</div>
          </div>

          <div class="space-y-1.5 text-sm">
            <div class="font-medium text-slate-100">${q.question_en}</div>
            <div class="text-amber-200/90 text-xs">${q.question_hi}</div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
            ${optionsHtml}
          </div>

          <div class="bg-blue-950/40 border border-blue-900/60 rounded-xl p-3.5 space-y-1.5 mt-2 text-xs">
            <div class="font-bold text-blue-300 flex items-center gap-1.5">
              <span>💡 Official Answer Key: Option ${q.correct}</span>
            </div>
            <div class="text-slate-300 leading-relaxed">${q.explanation_en}</div>
            <div class="text-amber-200/80 leading-relaxed pt-1 border-t border-blue-900/40">${q.explanation_hi}</div>
          </div>
        `;
        list.appendChild(card);
      });
    }

    // Export / Copy String
    function copySubmissionString() {
      let correct = 0, incorrect = 0, unattempted = 0;
      questionsData.forEach(q => {
        const a = userAnswers[q.id];
        if (!a) unattempted++;
        else if (a === q.correct) correct++;
        else incorrect++;
      });
      const score = ((correct * 1.0) - (incorrect * 0.25)).toFixed(2);
      const acc = (correct + incorrect) > 0 ? (((correct / (correct + incorrect)) * 100).toFixed(1) + "%") : "N/A";

      const summary = `MPPSC Mock Test 01 Result | Date: ${new Date().toLocaleDateString()} | Score: ${score}/100 | Correct: ${correct} | Incorrect: ${incorrect} | Unattempted: ${unattempted} | Accuracy: ${acc}`;
      navigator.clipboard.writeText(summary).then(() => {
        const btn = document.getElementById('copySummaryBtn');
        btn.innerText = "✅ Result Copied to Clipboard!";
        setTimeout(() => {
          btn.innerText = "📋 Copy Score Summary for AI Assistant";
        }, 3000);
      });
    }
  </script>
</body>
</html>
"""

output_html_path = r"C:\Users\hp\.gemini\antigravity\brain\64f902af-bbcc-4039-8dbe-53e6635bff0f\mppsc_mock_test_01.html"
with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(html_template)

# Also copy to workspace for user's permanent record
workspace_html_path = r"c:\Users\hp\Documents\antigravity\wonderful-noether\mppsc_mock_test_01.html"
with open(workspace_html_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print("Generated interactive mock test artifact successfully!")
