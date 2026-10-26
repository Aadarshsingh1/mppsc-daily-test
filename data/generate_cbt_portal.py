# -*- coding: utf-8 -*-
import json
import os

bank_path = r"c:\Users\hp\Documents\antigravity\wonderful-noether\data\question_bank.json"
if os.path.exists(bank_path):
    with open(bank_path, "r", encoding="utf-8") as f:
        questions = json.load(f)
else:
    json_path = r"c:\Users\hp\Documents\antigravity\wonderful-noether\data\mppsc_mock_01.json"
    with open(json_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>MPPSC Online Examination Portal — Computer Based Test (CBT)</title>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;500;600;700&display=swap');
    
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #f8fafc;
      color: #0f172a;
    }
    .hindi-text {
      font-family: 'Noto Sans Devanagari', 'Inter', sans-serif;
    }

    /* Official CBT Question Palette State Styles */
    .palette-btn {
      position: relative;
      width: 42px;
      height: 36px;
      font-size: 13px;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      border-radius: 6px;
      transition: all 0.15s ease-in-out;
      border: 1px solid #cbd5e1;
      user-select: none;
      cursor: pointer;
    }
    
    /* State 1: Not Visited */
    .state-not-visited {
      background-color: #f8fafc;
      color: #334155;
      border-color: #cbd5e1;
    }
    .state-not-visited:hover {
      background-color: #e2e8f0;
      border-color: #94a3b8;
    }
    
    /* State 2: Not Answered */
    .state-not-answered {
      background-color: #ef4444;
      color: #ffffff;
      border-color: #dc2626;
      border-radius: 4px 4px 12px 12px; /* classic CBT bookmark shape */
    }
    
    /* State 3: Answered */
    .state-answered {
      background-color: #16a34a;
      color: #ffffff;
      border-color: #15803d;
      border-radius: 12px 12px 4px 4px; /* classic CBT trapezoid shape */
    }
    
    /* State 4: Marked for Review */
    .state-marked-review {
      background-color: #7c3aed;
      color: #ffffff;
      border-color: #6d28d9;
      border-radius: 50%;
    }
    
    /* State 5: Answered and Marked for Review */
    .state-answered-marked {
      background-color: #7c3aed;
      color: #ffffff;
      border-color: #6d28d9;
      border-radius: 50%;
    }
    .state-answered-marked::after {
      content: '';
      position: absolute;
      bottom: 1.5px;
      right: 1.5px;
      width: 10px;
      height: 10px;
      background-color: #22c55e;
      border-radius: 50%;
      border: 1.5px solid #ffffff;
    }

    .palette-btn.active-current {
      outline: 2px solid #2563eb;
      outline-offset: 2px;
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.4);
    }

    /* Custom Scrollbars */
    .custom-scroll::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    .custom-scroll::-webkit-scrollbar-thumb {
      background: #cbd5e1;
      border-radius: 4px;
    }
    .custom-scroll::-webkit-scrollbar-thumb:hover {
      background: #94a3b8;
    }
  </style>
</head>
<body class="min-h-screen bg-slate-50 text-slate-800 flex flex-col antialiased">

  <!-- ============================================================== -->
  <!-- 1. OFFICIAL GOVT PORTAL HEADER (Visible in Dashboard & History) -->
  <!-- ============================================================== -->
  <header id="portalHeader" class="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 py-2.5 flex items-center justify-between">
      <!-- MPPSC Logo & Title -->
      <div class="flex items-center gap-3">
        <div class="w-11 h-11 rounded-lg bg-blue-900 border border-blue-950 flex items-center justify-center text-white font-bold text-lg shadow-sm">
          MP
        </div>
        <div>
          <div class="text-xs uppercase tracking-wider font-bold text-slate-500">Madhya Pradesh Public Service Commission</div>
          <h1 class="text-base md:text-lg font-bold text-blue-950 leading-tight">
            मध्य प्रदेश लोक सेवा आयोग — Online Examination Portal
          </h1>
        </div>
      </div>

      <!-- Live Clock & Candidate Status Pill -->
      <div class="hidden sm:flex items-center gap-4 text-xs">
        <div class="bg-slate-100 border border-slate-200 px-3 py-1.5 rounded-md text-slate-600 font-medium">
          <span class="text-slate-400">Current Time:</span> <span id="portalClock" class="font-mono font-bold text-slate-800">--:--:-- IST</span>
        </div>
        <div class="flex items-center gap-2 bg-blue-50 border border-blue-200 px-3 py-1.5 rounded-md text-blue-900">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="font-semibold">Candidate Portal Active</span>
        </div>
      </div>
    </div>
  </header>

  <!-- ============================================================== -->
  <!-- VIEW 1: CANDIDATE DASHBOARD -->
  <!-- ============================================================== -->
  <main id="viewDashboard" class="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 space-y-6">

    <!-- Candidate Profile Banner -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm flex flex-col md:flex-row items-start md:items-center justify-between gap-5">
      <div class="flex items-center gap-4">
        <!-- Candidate Photo Placeholder -->
        <div class="w-16 h-16 rounded-lg bg-slate-100 border-2 border-slate-300 flex flex-col items-center justify-center text-slate-400 shrink-0 relative overflow-hidden">
          <svg class="w-9 h-9 text-slate-400" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path>
          </svg>
          <span class="text-[9px] uppercase tracking-tighter text-slate-500 font-bold mt-0.5">PHOTO</span>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h2 id="candidateName" class="text-lg font-bold text-slate-900">Aadarsh Thakur</h2>
            <span class="px-2 py-0.5 text-[10px] font-semibold bg-blue-100 text-blue-800 rounded">GENERAL / UR</span>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-3 gap-x-4 gap-y-0.5 text-xs text-slate-500 mt-1">
            <div>Roll No: <span class="font-mono font-semibold text-slate-700">MPPSC-2026-489102</span></div>
            <div>Application No: <span class="font-mono font-semibold text-slate-700">APP-7182904</span></div>
            <div>Post: <span class="font-semibold text-slate-700">State Services (Prelims)</span></div>
          </div>
        </div>
      </div>

      <div class="flex items-center gap-2 self-end md:self-center">
        <button onclick="switchView('HISTORY')" class="px-3.5 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-xs font-semibold border border-slate-300 transition flex items-center gap-1.5">
          <svg class="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          Past Test History
        </button>
      </div>
    </div>

    <!-- Scheduled Test Hero Card (No Unit Lists, Clean Exam Focus) -->
    <div class="bg-white border-2 border-blue-800/20 rounded-xl p-6 shadow-sm relative overflow-hidden">
      <!-- Status Top Bar -->
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-4 mb-5">
        <div class="flex items-center gap-2">
          <span class="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold bg-blue-100 text-blue-900">
            TODAY'S SCHEDULED EXAMINATION
          </span>
          <span id="testStatusBadge" class="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300">
            🕒 Scheduled at 8:00 PM IST
          </span>
        </div>
        <div class="text-xs text-slate-500 font-medium">
          Date: <span id="todayDateStr" class="font-semibold text-slate-800">26 October 2026</span>
        </div>
      </div>

      <!-- Main Test Details -->
      <div class="flex flex-col lg:flex-row items-start lg:items-center justify-between gap-6">
        <div class="space-y-2 flex-1">
          <h3 class="text-xl md:text-2xl font-black text-slate-900">
            MPPSC Mock Examination — Test 01
          </h3>
          <p class="text-sm text-slate-600 font-medium">
            General Studies Paper-I (Full Length Mock Examination)
          </p>

          <!-- Examination Specifications Bar -->
          <div class="flex flex-wrap items-center gap-4 text-xs text-slate-600 pt-2">
            <div class="flex items-center gap-1.5">
              <span class="font-semibold text-slate-900">Total Questions:</span> 100 MCQs
            </div>
            <span class="text-slate-300">•</span>
            <div class="flex items-center gap-1.5">
              <span class="font-semibold text-slate-900">Maximum Marks:</span> 100.00
            </div>
            <span class="text-slate-300">•</span>
            <div class="flex items-center gap-1.5">
              <span class="font-semibold text-slate-900">Duration:</span> 120 Minutes (2.0 Hours)
            </div>
            <span class="text-slate-300">•</span>
            <div class="flex items-center gap-1.5">
              <span class="font-semibold text-slate-900">Marking:</span> +1.00 / −0.25
            </div>
          </div>
        </div>

        <!-- Right Side: Countdown & Action Button -->
        <div class="bg-slate-50 border border-slate-200 rounded-xl p-4 w-full lg:w-80 flex flex-col items-center justify-center text-center">
          <div class="text-xs font-medium text-slate-500 uppercase tracking-wider">Time to Test Window</div>
          <div id="dashboardCountdown" class="font-mono text-2xl font-extrabold text-blue-900 my-1">
            --h : --m : --s
          </div>
          <div id="scheduleNote" class="text-[11px] text-slate-500 mb-3">
            Scheduled Daily at 08:00 PM IST
          </div>

          <!-- Main CTA: Attempt Test Button -->
          <button id="attemptTestBtn" onclick="startExaminationFlow()" class="w-full py-2.5 px-4 bg-blue-900 hover:bg-blue-800 text-white font-bold text-sm rounded-lg shadow-md transition transform active:scale-95 flex items-center justify-center gap-2">
            <span>Attempt Examination Now</span>
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
            </svg>
          </button>

          <!-- Practice Early Access Toggle (Allows practicing anytime during daytime) -->
          <div class="mt-2 text-[11px] text-slate-500 flex items-center gap-1">
            <span>🔒 Locked until 8 PM?</span>
            <button onclick="unlockTestEarly()" class="text-blue-700 underline font-semibold hover:text-blue-900">
              Unlock Test Now (Practice Mode)
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Candidate Performance Statistics Grid -->
    <div>
      <h4 class="text-xs font-bold uppercase tracking-wider text-slate-500 mb-3">Overall Performance Summary</h4>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
          <div class="text-xs font-medium text-slate-500">Tests Attempted</div>
          <div id="statTotalTests" class="text-2xl font-bold text-slate-900 mt-1">0</div>
          <div class="text-[11px] text-slate-400 mt-0.5">Recorded attempts</div>
        </div>
        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
          <div class="text-xs font-medium text-slate-500">Average Score</div>
          <div id="statAvgScore" class="text-2xl font-bold text-blue-900 mt-1">--</div>
          <div class="text-[11px] text-slate-400 mt-0.5">Out of 100 marks</div>
        </div>
        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
          <div class="text-xs font-medium text-slate-500">Highest Score</div>
          <div id="statBestScore" class="text-2xl font-bold text-emerald-600 mt-1">--</div>
          <div class="text-[11px] text-slate-400 mt-0.5">Personal best</div>
        </div>
        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm">
          <div class="text-xs font-medium text-slate-500">Average Accuracy</div>
          <div id="statAvgAccuracy" class="text-2xl font-bold text-purple-600 mt-1">--</div>
          <div class="text-[11px] text-slate-400 mt-0.5">Attempt accuracy</div>
        </div>
      </div>
    </div>

    <!-- Recent History Section -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
      <div class="flex items-center justify-between mb-4">
        <h4 class="font-bold text-sm text-slate-900">Recent Examination Attempts</h4>
        <button onclick="switchView('HISTORY')" class="text-xs text-blue-700 hover:underline font-semibold">
          View Full Table →
        </button>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-50 text-slate-600 border-b border-slate-200">
            <tr>
              <th class="p-3">Test No.</th>
              <th class="p-3">Date</th>
              <th class="p-3 text-right">Score /100</th>
              <th class="p-3 text-center">Correct</th>
              <th class="p-3 text-center">Incorrect</th>
              <th class="p-3 text-center">Skipped</th>
              <th class="p-3 text-right">Accuracy</th>
              <th class="p-3 text-right">Time Taken</th>
            </tr>
          </thead>
          <tbody id="recentHistoryTableBody" class="divide-y divide-slate-100">
            <!-- Dynamically populated or empty state -->
          </tbody>
        </table>
      </div>
    </div>
  </main>

  <!-- ============================================================== -->
  <!-- VIEW 2: REAL EXAMINATION SCREEN (CBT Layout) -->
  <!-- ============================================================== -->
  <div id="viewExamination" class="hidden fixed inset-0 z-50 flex flex-col bg-slate-100 overflow-hidden">

    <!-- CBT Exam Header -->
    <header class="bg-blue-950 text-white px-4 py-2 flex items-center justify-between border-b border-blue-900 shrink-0">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded bg-white text-blue-950 font-black text-sm flex items-center justify-center">
          MP
        </div>
        <div>
          <h2 class="text-sm font-bold tracking-tight">MPPSC Mock Examination — Test 01</h2>
          <div class="text-[11px] text-blue-200">General Studies Paper-I • 100 Questions • +1 / -0.25</div>
        </div>
      </div>

      <!-- Center: Remaining Timer -->
      <div class="flex items-center gap-2 bg-blue-900/80 border border-blue-700/80 px-4 py-1.5 rounded-md">
        <span class="text-xs text-blue-300 font-medium">Time Left:</span>
        <span id="examTimer" class="font-mono text-base md:text-lg font-bold text-amber-300">120:00</span>
      </div>

      <!-- Right: Candidate Info & Submit Button -->
      <div class="flex items-center gap-4">
        <div class="hidden md:flex items-center gap-2 text-right">
          <div>
            <div class="text-xs font-bold text-white">Aadarsh Thakur</div>
            <div class="text-[10px] text-blue-300 font-mono">Roll: MPPSC-2026-489102</div>
          </div>
          <div class="w-8 h-8 rounded bg-blue-800 border border-blue-600 flex items-center justify-center text-xs font-bold text-blue-200">
            AT
          </div>
        </div>

        <button onclick="openSubmitModal()" class="bg-red-600 hover:bg-red-500 text-white font-bold text-xs px-3.5 py-2 rounded shadow transition">
          Submit Exam
        </button>
      </div>
    </header>

    <!-- Sub-header: Subject Name & Language Selector -->
    <div class="bg-white border-b border-slate-200 px-4 py-1.5 flex items-center justify-between text-xs shrink-0">
      <div class="font-semibold text-slate-700">
        Section: <span class="text-blue-950 font-bold">General Studies (सामान्य अध्ययन)</span>
      </div>

      <div class="flex items-center gap-2">
        <span class="text-slate-500">View In:</span>
        <select id="examLangSelect" onchange="changeExamLanguage(this.value)" class="border border-slate-300 rounded px-2 py-1 text-xs bg-slate-50 font-medium text-slate-700 focus:outline-none focus:ring-1 focus:ring-blue-600">
          <option value="both">Bilingual (हिन्दी + English)</option>
          <option value="en">English Only</option>
          <option value="hi">हिन्दी Only</option>
        </select>
      </div>
    </div>

    <!-- CBT Main Body: Split View (Left Question Panel, Right Palette) -->
    <div class="flex-1 flex flex-col lg:flex-row overflow-hidden min-h-0">

      <!-- Left Side: Question Panel -->
      <div class="flex-1 flex flex-col bg-white border-r border-slate-200 overflow-hidden min-h-0">
        <!-- Question Header Strip -->
        <div class="bg-slate-50 border-b border-slate-200 px-5 py-2.5 flex items-center justify-between text-xs shrink-0">
          <div class="font-bold text-slate-800">
            Question No. <span id="currentQNumDisplay" class="text-blue-900 text-sm font-extrabold">1</span> of 100
          </div>
          <div class="flex items-center gap-3 text-slate-500">
            <span>Marks: <span class="font-bold text-emerald-600">+1.00</span></span>
            <span>Negative: <span class="font-bold text-rose-600">-0.25</span></span>
          </div>
        </div>

        <!-- Question & Options Content Area -->
        <div id="qScrollArea" class="flex-1 overflow-y-auto p-4 md:p-6 space-y-4 custom-scroll">
          <!-- Question Text (English) -->
          <div id="qTextEnglish" class="text-slate-900 text-base md:text-lg font-medium leading-relaxed">
            <!-- English Question Injected Here -->
          </div>

          <!-- Question Text (Hindi) -->
          <div id="qTextHindi" class="hindi-text text-slate-800 text-base md:text-lg font-medium leading-relaxed bg-amber-50/50 p-3.5 rounded-lg border border-amber-200/60">
            <!-- Hindi Question Injected Here -->
          </div>

          <!-- 4 Options (A, B, C, D) -->
          <div class="pt-1">
            <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2">Options:</div>
            <div id="cbtOptionsContainer" class="space-y-2.5">
              <!-- Dynamically populated options -->
            </div>
          </div>

          <!-- CBT Action Buttons: APPEAR IMMEDIATELY AT THE END OF THE QUESTION (Directly below Option D) -->
          <div class="pt-4 mt-4 border-t border-slate-200 flex flex-wrap items-center justify-between gap-3 bg-slate-50 p-3.5 rounded-xl border border-slate-200">
            <!-- Left Actions -->
            <div class="flex items-center gap-2">
              <button onclick="handlePreviousQuestion()" id="btnPrev" class="px-4 py-2 bg-white hover:bg-slate-100 text-slate-700 text-xs font-bold rounded-lg border border-slate-300 transition shadow-xs disabled:opacity-40">
                ← Previous
              </button>
              <button onclick="handleClearResponse()" class="px-4 py-2 bg-white hover:bg-rose-50 text-rose-700 text-xs font-bold rounded-lg border border-rose-300 transition shadow-xs">
                Clear Response
              </button>
            </div>

            <!-- Right Actions -->
            <div class="flex items-center gap-2">
              <button onclick="handleMarkForReview()" class="px-4 py-2 bg-purple-100 hover:bg-purple-200 text-purple-900 text-xs font-bold rounded-lg border border-purple-300 transition shadow-xs">
                Mark for Review & Next
              </button>
              <button onclick="handleSaveAndNext()" class="px-6 py-2 bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-black rounded-lg transition shadow-md shadow-emerald-900/15">
                Save & Next →
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Side: Question Palette Panel -->
      <div class="w-full lg:w-80 bg-slate-50 flex flex-col shrink-0 border-t lg:border-t-0 overflow-hidden min-h-0">

        <!-- Candidate Mini Profile -->
        <div class="p-2.5 bg-white border-b border-slate-200 flex items-center gap-3 shrink-0">
          <div class="w-9 h-9 rounded bg-slate-100 border border-slate-300 flex items-center justify-center text-slate-500 font-bold text-xs shrink-0">
            PHOTO
          </div>
          <div class="overflow-hidden">
            <div class="text-xs font-bold text-slate-800 truncate">Aadarsh Thakur</div>
            <div class="text-[10px] text-slate-500">Roll: MPPSC-2026-489102</div>
          </div>
        </div>

        <!-- Official 5 CBT States Legend -->
        <div class="p-2.5 bg-white border-b border-slate-200 text-[11px] space-y-1.5 shrink-0">
          <div class="font-bold text-slate-700 text-[11px] mb-0.5">Question Status Legend:</div>
          <div class="grid grid-cols-2 gap-1.5 text-slate-600">
            <div class="flex items-center gap-1.5">
              <span class="w-5 h-4 bg-emerald-600 rounded text-white text-[9px] font-bold flex items-center justify-center" style="border-radius: 6px 6px 2px 2px;">#</span>
              <span>Answered (<b id="cntAnswered">0</b>)</span>
            </div>
            <div class="flex items-center gap-1.5">
              <span class="w-5 h-4 bg-red-500 rounded text-white text-[9px] font-bold flex items-center justify-center" style="border-radius: 2px 2px 6px 6px;">#</span>
              <span>Not Answered (<b id="cntNotAnswered">0</b>)</span>
            </div>
            <div class="flex items-center gap-1.5">
              <span class="w-5 h-4 bg-slate-100 border border-slate-300 rounded text-slate-700 text-[9px] font-bold flex items-center justify-center">#</span>
              <span>Not Visited (<b id="cntNotVisited">100</b>)</span>
            </div>
            <div class="flex items-center gap-1.5">
              <span class="w-4 h-4 bg-purple-600 rounded-full text-white text-[9px] font-bold flex items-center justify-center">#</span>
              <span>Marked (<b id="cntMarked">0</b>)</span>
            </div>
          </div>
          <div class="flex items-center gap-1.5 pt-1 border-t border-slate-100 text-slate-600">
            <span class="relative w-4 h-4 bg-purple-600 rounded-full text-white text-[9px] font-bold flex items-center justify-center">
              #
              <span class="absolute -bottom-0.5 -right-0.5 w-2 h-2 bg-emerald-400 rounded-full border border-white"></span>
            </span>
            <span>Ans. & Marked for Review (<b id="cntAnsweredMarked">0</b>)</span>
          </div>
        </div>

        <!-- 100-Question Palette Grid (Clean scrollable grid) -->
        <div class="flex-1 overflow-y-auto p-2.5 custom-scroll">
          <div class="text-xs font-bold text-slate-700 mb-2 flex items-center justify-between">
            <span>Questions (1 - 100):</span>
            <span class="text-[10px] text-slate-400 font-normal">Click number to jump</span>
          </div>
          <div id="cbtPaletteGrid" class="grid grid-cols-5 gap-1.5 justify-items-center">
            <!-- 100 Buttons generated via JS with numbers 1 to 100 -->
          </div>
        </div>

        <!-- Bottom Quick Submit Button -->
        <div class="p-2.5 bg-white border-t border-slate-200 shrink-0">
          <button onclick="openSubmitModal()" class="w-full py-2 bg-blue-900 hover:bg-blue-800 text-white font-bold text-xs rounded-lg shadow transition">
            Final Examination Submit
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- VIEW 3: OFFICIAL RESULT & SCORECARD SCREEN -->
  <!-- ============================================================== -->
  <main id="viewResult" class="hidden flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 space-y-6">

    <!-- Scorecard Header Card -->
    <div class="bg-white border-2 border-blue-900 rounded-xl p-6 shadow-sm">
      <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-6 border-b border-slate-200">
        <div>
          <div class="inline-block bg-blue-100 text-blue-900 text-xs font-bold px-3 py-1 rounded mb-2">
            OFFICIAL EXAMINATION SCORECARD
          </div>
          <h2 class="text-2xl font-black text-slate-900">MPPSC Mock Examination — Test 01</h2>
          <p class="text-xs text-slate-500 mt-1">
            Candidate: <b>Aadarsh Thakur</b> • Roll No: <b>MPPSC-2026-489102</b> • Date: <span id="resDateDisplay"></span>
          </p>
        </div>

        <!-- Big Score Box -->
        <div class="bg-slate-50 border-2 border-blue-900 rounded-xl p-5 text-center min-w-[200px]">
          <div class="text-xs font-bold text-slate-500 uppercase tracking-wider">Final Net Score</div>
          <div id="resFinalScore" class="text-4xl font-black text-blue-950 my-1">0.00</div>
          <div class="text-xs text-slate-600 font-semibold">Maximum: 100.00 Marks</div>
        </div>
      </div>

      <!-- Metrics Breakdown Row -->
      <div class="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-6 text-center text-xs">
        <div class="p-3 bg-emerald-50 border border-emerald-200 rounded-lg">
          <div class="text-emerald-700 font-medium">Correct Answers (+1)</div>
          <div id="resCorrectCount" class="text-xl font-bold text-emerald-800 mt-1">0</div>
        </div>
        <div class="p-3 bg-rose-50 border border-rose-200 rounded-lg">
          <div class="text-rose-700 font-medium">Incorrect Answers (-0.25)</div>
          <div id="resIncorrectCount" class="text-xl font-bold text-rose-800 mt-1">0</div>
        </div>
        <div class="p-3 bg-slate-50 border border-slate-200 rounded-lg">
          <div class="text-slate-600 font-medium">Unattempted (0)</div>
          <div id="resUnattemptedCount" class="text-xl font-bold text-slate-800 mt-1">0</div>
        </div>
        <div class="p-3 bg-blue-50 border border-blue-200 rounded-lg">
          <div class="text-blue-700 font-medium">Accuracy</div>
          <div id="resAccuracyPercent" class="text-xl font-bold text-blue-900 mt-1">0%</div>
        </div>
        <div class="p-3 bg-purple-50 border border-purple-200 rounded-lg col-span-2 sm:col-span-1">
          <div class="text-purple-700 font-medium">Time Taken</div>
          <div id="resTimeTakenDisplay" class="text-xl font-bold text-purple-900 mt-1">0m 0s</div>
        </div>
      </div>

      <!-- Return & History Action Buttons -->
      <div class="flex flex-wrap items-center justify-between gap-3 pt-6 mt-6 border-t border-slate-200">
        <div id="resComparisonNote" class="text-xs text-slate-500">
          <!-- Comparison with previous test -->
        </div>
        <div class="flex items-center gap-3">
          <button onclick="switchView('HISTORY')" class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg border border-slate-300 transition">
            View All Test History
          </button>
          <button onclick="switchView('DASHBOARD')" class="px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white text-xs font-bold rounded-lg shadow transition">
            Return to Dashboard
          </button>
        </div>
      </div>
    </div>

    <!-- Question-by-Question Solution Review Section -->
    <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm space-y-4">
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 pb-3">
        <div>
          <h3 class="font-bold text-base text-slate-900">Detailed Question Solutions & Explanations</h3>
          <p class="text-xs text-slate-500">Verify your responses against the official key</p>
        </div>
        <div class="flex items-center gap-1.5 text-xs">
          <button onclick="filterResultSolutions('ALL')" id="resFilter-ALL" class="px-3 py-1.5 rounded-md font-semibold bg-blue-900 text-white transition">All (100)</button>
          <button onclick="filterResultSolutions('CORRECT')" id="resFilter-CORRECT" class="px-3 py-1.5 rounded-md font-semibold bg-slate-100 text-slate-600 hover:bg-slate-200 transition">Correct</button>
          <button onclick="filterResultSolutions('INCORRECT')" id="resFilter-INCORRECT" class="px-3 py-1.5 rounded-md font-semibold bg-slate-100 text-slate-600 hover:bg-slate-200 transition">Incorrect</button>
          <button onclick="filterResultSolutions('UNATTEMPTED')" id="resFilter-UNATTEMPTED" class="px-3 py-1.5 rounded-md font-semibold bg-slate-100 text-slate-600 hover:bg-slate-200 transition">Skipped</button>
        </div>
      </div>

      <!-- Solutions List Container -->
      <div id="resultSolutionsList" class="space-y-4">
        <!-- 100 Solution cards generated by JS -->
      </div>
    </div>
  </main>

  <!-- ============================================================== -->
  <!-- VIEW 4: TEST HISTORY SCREEN -->
  <!-- ============================================================== -->
  <main id="viewHistory" class="hidden flex-1 max-w-7xl w-full mx-auto p-4 md:p-6 space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h2 class="text-xl font-bold text-slate-900">Candidate Examination History</h2>
        <p class="text-xs text-slate-500">Chronological record of completed MPPSC mock tests</p>
      </div>
      <button onclick="switchView('DASHBOARD')" class="px-4 py-2 bg-blue-900 hover:bg-blue-800 text-white text-xs font-bold rounded-lg shadow transition">
        ← Back to Dashboard
      </button>
    </div>

    <!-- History Table -->
    <div class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs">
          <thead class="bg-slate-50 text-slate-700 font-bold border-b border-slate-200">
            <tr>
              <th class="p-3.5">Test No.</th>
              <th class="p-3.5">Date & Time</th>
              <th class="p-3.5 text-right">Score /100</th>
              <th class="p-3.5 text-center text-emerald-700">Correct</th>
              <th class="p-3.5 text-center text-rose-700">Incorrect</th>
              <th class="p-3.5 text-center text-slate-600">Unattempted</th>
              <th class="p-3.5 text-right text-blue-900">Accuracy</th>
              <th class="p-3.5 text-right">Time Taken</th>
            </tr>
          </thead>
          <tbody id="fullHistoryTableBody" class="divide-y divide-slate-100">
            <!-- Dynamically populated -->
          </tbody>
        </table>
      </div>
    </div>
  </main>

  <!-- ============================================================== -->
  <!-- MODAL: FINAL SUBMISSION CONFIRMATION (Official CBT Style) -->
  <!-- ============================================================== -->
  <div id="submissionModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-4 hidden">
    <div class="bg-white border border-slate-300 rounded-xl max-w-lg w-full p-6 shadow-2xl space-y-4">
      <div class="flex items-center gap-3 border-b border-slate-200 pb-3">
        <div class="w-10 h-10 rounded-full bg-amber-100 text-amber-700 flex items-center justify-center font-bold text-lg">
          ⚠️
        </div>
        <div>
          <h3 class="font-bold text-base text-slate-900">Confirm Examination Submission</h3>
          <p class="text-xs text-slate-500">Please review your question response summary</p>
        </div>
      </div>

      <!-- Summary Statistics Table -->
      <div class="bg-slate-50 border border-slate-200 rounded-lg p-3 text-xs space-y-2">
        <div class="grid grid-cols-2 gap-2">
          <div class="flex justify-between p-2 bg-white rounded border border-slate-200">
            <span class="text-slate-600">Total Questions:</span>
            <span class="font-bold text-slate-900">100</span>
          </div>
          <div class="flex justify-between p-2 bg-emerald-50 rounded border border-emerald-200">
            <span class="text-emerald-800">Answered:</span>
            <span id="modalAnsCount" class="font-bold text-emerald-800">0</span>
          </div>
          <div class="flex justify-between p-2 bg-rose-50 rounded border border-rose-200">
            <span class="text-rose-800">Not Answered:</span>
            <span id="modalNotAnsCount" class="font-bold text-rose-800">0</span>
          </div>
          <div class="flex justify-between p-2 bg-purple-50 rounded border border-purple-200">
            <span class="text-purple-800">Marked for Review:</span>
            <span id="modalMarkedCount" class="font-bold text-purple-800">0</span>
          </div>
          <div class="flex justify-between p-2 bg-purple-50 rounded border border-purple-200 col-span-2">
            <span class="text-purple-800">Answered & Marked for Review:</span>
            <span id="modalAnsMarkedCount" class="font-bold text-purple-800">0</span>
          </div>
          <div class="flex justify-between p-2 bg-slate-100 rounded border border-slate-200 col-span-2">
            <span class="text-slate-600">Not Visited:</span>
            <span id="modalNotVisitedCount" class="font-bold text-slate-700">100</span>
          </div>
        </div>
      </div>

      <p class="text-xs text-slate-600 leading-relaxed">
        <b>Are you sure you want to submit?</b> Once confirmed, you will not be able to revisit or modify any answers.
      </p>

      <div class="flex items-center justify-end gap-3 pt-2 border-t border-slate-200">
        <button onclick="closeSubmitModal()" class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-lg border border-slate-300 transition">
          Return to Examination
        </button>
        <button onclick="submitExaminationConfirmed()" class="px-4 py-2 bg-red-600 hover:bg-red-500 text-white text-xs font-bold rounded-lg shadow transition">
          Yes, Submit Examination
        </button>
      </div>
    </div>
  </div>

  <!-- ============================================================== -->
  <!-- JAVASCRIPT: APPLICATION LOGIC & STATE ENGINE -->
  <!-- ============================================================== -->
  <script>
    const examQuestions = """ + json.dumps(questions, ensure_ascii=False) + """;

    // Question State Enum
    const Q_STATE = {
      NOT_VISITED: 'NOT_VISITED',
      NOT_ANSWERED: 'NOT_ANSWERED',
      ANSWERED: 'ANSWERED',
      MARKED_FOR_REVIEW: 'MARKED_FOR_REVIEW',
      ANSWERED_AND_MARKED: 'ANSWERED_AND_MARKED'
    };

    // Global Application State
    let appState = {
      currentView: 'DASHBOARD', // 'DASHBOARD', 'EXAMINATION', 'RESULT', 'HISTORY'
      currentQIdx: 0,
      examLanguage: 'both', // 'both', 'en', 'hi'
      responses: {}, // { qId: { selectedOption: 'A'|'B'|'C'|'D'|null, state: Q_STATE } }
      examSecondsRemaining: 120 * 60, // 120 minutes = 7200s
      examTimerInterval: null,
      examStartTime: null,
      examSubmitted: false,
      isPracticeUnlocked: false,
      history: []
    };

    // Initialize Application
    window.addEventListener('DOMContentLoaded', () => {
      loadHistoryFromStorage();
      initQuestionsState();
      startPortalClock();
      updateDashboardCounts();
      renderDashboardHistory();
      renderPalette();
      renderQuestion();
    });

    // Initialize Question States
    function initQuestionsState() {
      // Try restoring saved ongoing session if available
      const savedResponses = localStorage.getItem('mppsc_cbt_session_responses');
      if (savedResponses) {
        try {
          appState.responses = JSON.parse(savedResponses);
          return;
        } catch(e){}
      }

      examQuestions.forEach((q, idx) => {
        appState.responses[q.id] = {
          selectedOption: null,
          state: idx === 0 ? Q_STATE.NOT_ANSWERED : Q_STATE.NOT_VISITED
        };
      });
    }

    // Live Clock & 8:00 PM Scheduler
    function startPortalClock() {
      function update() {
        const now = new Date();
        const timeStr = now.toLocaleTimeString('en-US', { hour12: true });
        const clockEl = document.getElementById('portalClock');
        if (clockEl) clockEl.innerText = timeStr + ' IST';

        // Check 8:00 PM (20:00:00 IST)
        const target = new Date();
        target.setHours(20, 0, 0, 0); // 8:00 PM

        let diffMs = target.getTime() - now.getTime();
        const countdownEl = document.getElementById('dashboardCountdown');
        const statusBadge = document.getElementById('testStatusBadge');
        const attemptBtn = document.getElementById('attemptTestBtn');

        if (diffMs > 0 && !appState.isPracticeUnlocked) {
          // Before 8:00 PM
          const hrs = Math.floor(diffMs / (1000 * 60 * 60));
          const mins = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60));
          const secs = Math.floor((diffMs % (1000 * 60)) / 1000);
          countdownEl.innerText = `${String(hrs).padStart(2, '0')}h : ${String(mins).padStart(2, '0')}m : ${String(secs).padStart(2, '0')}s`;
          statusBadge.className = "inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold bg-amber-100 text-amber-900 border border-amber-300";
          statusBadge.innerText = "🕒 Locked — Opens at 8:00 PM IST";
          attemptBtn.disabled = true;
          attemptBtn.className = "w-full py-2.5 px-4 bg-slate-200 text-slate-500 font-bold text-sm rounded-lg cursor-not-allowed flex items-center justify-center gap-2 shadow-none select-none";
          attemptBtn.innerHTML = `<span>🔒 Test Locked (Unlocks at 8:00 PM IST)</span>`;
        } else {
          // Available (Either 8:00 PM reached or unlocked for practice)
          countdownEl.innerText = "00h : 00m : 00s";
          statusBadge.className = "inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold bg-emerald-100 text-emerald-900 border border-emerald-300";
          statusBadge.innerText = "🟢 Available Now (Test Active)";
          attemptBtn.disabled = false;
          attemptBtn.className = "w-full py-2.5 px-4 bg-emerald-700 hover:bg-emerald-600 text-white font-bold text-sm rounded-lg shadow-md transition transform active:scale-95 flex items-center justify-center gap-2 cursor-pointer";
          attemptBtn.innerHTML = `<span>Attempt Examination Now</span><svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>`;
        }
      }
      update();
      setInterval(update, 1000);
    }

    function unlockTestEarly() {
      appState.isPracticeUnlocked = true;
      alert("Practice Mode Active: You can now attempt the examination immediately!");
      const statusBadge = document.getElementById('testStatusBadge');
      statusBadge.className = "inline-flex items-center px-2.5 py-1 rounded-md text-xs font-bold bg-emerald-100 text-emerald-900 border border-emerald-300";
      statusBadge.innerText = "🟢 Available Now (Practice Mode)";
    }

    // View Navigation
    function switchView(targetView) {
      appState.currentView = targetView;
      const views = ['viewDashboard', 'viewExamination', 'viewResult', 'viewHistory'];
      views.forEach(v => {
        const el = document.getElementById(v);
        if (el) el.classList.add('hidden');
      });

      const header = document.getElementById('portalHeader');
      if (targetView === 'EXAMINATION') {
        if (header) header.classList.add('hidden');
        document.getElementById('viewExamination').classList.remove('hidden');
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
        if (header) header.classList.remove('hidden');
        if (targetView === 'DASHBOARD') document.getElementById('viewDashboard').classList.remove('hidden');
        if (targetView === 'RESULT') document.getElementById('viewResult').classList.remove('hidden');
        if (targetView === 'HISTORY') document.getElementById('viewHistory').classList.remove('hidden');
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Start Examination Flow
    function startExaminationFlow() {
      const now = new Date();
      const target = new Date();
      target.setHours(20, 0, 0, 0); // 8:00 PM IST
      if (now < target && !appState.isPracticeUnlocked) {
        alert("The examination is scheduled for 8:00 PM IST. The test window will automatically unlock at 8:00 PM.");
        return;
      }
      switchView('EXAMINATION');
      appState.examStartTime = new Date();
      startExamCountdown();
      renderQuestion();
      updatePaletteCounts();
    }

    // Exam Countdown Timer
    function startExamCountdown() {
      if (appState.examTimerInterval) clearInterval(appState.examTimerInterval);
      appState.examTimerInterval = setInterval(() => {
        if (appState.examSubmitted) return;
        if (appState.examSecondsRemaining > 0) {
          appState.examSecondsRemaining--;
          updateExamTimerDisplay();
        } else {
          clearInterval(appState.examTimerInterval);
          alert("Time Expired! The examination is being submitted automatically.");
          submitExaminationConfirmed();
        }
      }, 1000);
    }

    function updateExamTimerDisplay() {
      const mins = Math.floor(appState.examSecondsRemaining / 60);
      const secs = appState.examSecondsRemaining % 60;
      const display = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
      const el = document.getElementById('examTimer');
      if (el) el.innerText = display;

      if (appState.examSecondsRemaining < 300) {
        el.className = "font-mono text-base md:text-lg font-bold text-red-400 animate-pulse";
      } else if (appState.examSecondsRemaining < 900) {
        el.className = "font-mono text-base md:text-lg font-bold text-amber-300";
      }
    }

    // Change Language
    function changeExamLanguage(lang) {
      appState.examLanguage = lang;
      renderQuestion();
    }

    // Render Question & Options
    function renderQuestion() {
      const q = examQuestions[appState.currentQIdx];
      const qNum = appState.currentQIdx + 1;
      const qId = q.id;

      // Reset scroll to top of question area
      const qScroll = document.getElementById('qScrollArea');
      if (qScroll) qScroll.scrollTop = 0;

      // Update question number
      document.getElementById('currentQNumDisplay').innerText = qNum;

      // Question texts
      const enEl = document.getElementById('qTextEnglish');
      const hiEl = document.getElementById('qTextHindi');

      if (appState.examLanguage === 'both') {
        enEl.style.display = 'block';
        hiEl.style.display = 'block';
        enEl.innerHTML = `<span class="text-blue-900 font-bold mr-1.5">Q${qNum}.</span> ${q.question_en}`;
        hiEl.innerHTML = `<span class="text-amber-800 font-bold mr-1.5">प्र. ${qNum}.</span> ${q.question_hi}`;
      } else if (appState.examLanguage === 'hi') {
        enEl.style.display = 'none';
        hiEl.style.display = 'block';
        hiEl.innerHTML = `<span class="text-amber-800 font-bold mr-1.5">प्र. ${qNum}.</span> ${q.question_hi}`;
      } else {
        enEl.style.display = 'block';
        hiEl.style.display = 'none';
        enEl.innerHTML = `<span class="text-blue-900 font-bold mr-1.5">Q${qNum}.</span> ${q.question_en}`;
      }

      // Render Options
      const container = document.getElementById('cbtOptionsContainer');
      container.innerHTML = '';

      const resp = appState.responses[qId];
      const letters = ['A', 'B', 'C', 'D'];

      letters.forEach((optKey, idx) => {
        const isChecked = resp.selectedOption === optKey;
        const optEn = q.options_en[idx];
        const optHi = q.options_hi[idx];

        const label = document.createElement('label');
        label.className = `p-3.5 rounded-lg border cursor-pointer transition flex items-start gap-3 select-none ${
          isChecked ? 'bg-blue-50/70 border-blue-600 shadow-xs' : 'bg-white border-slate-200 hover:border-slate-300 hover:bg-slate-50'
        }`;

        let optText = '';
        if (appState.examLanguage === 'both') {
          optText = `
            <div class="flex-1 text-xs md:text-sm">
              <div class="font-medium text-slate-800">${optEn}</div>
              <div class="hindi-text text-slate-600 mt-0.5">${optHi}</div>
            </div>
          `;
        } else if (appState.examLanguage === 'hi') {
          optText = `<div class="hindi-text flex-1 text-xs md:text-sm font-medium text-slate-800">${optHi}</div>`;
        } else {
          optText = `<div class="flex-1 text-xs md:text-sm font-medium text-slate-800">${optEn}</div>`;
        }

        label.innerHTML = `
          <input type="radio" name="cbtOptionGroup" value="${optKey}" ${isChecked ? 'checked' : ''} class="mt-1 w-4 h-4 text-blue-600 border-slate-300 focus:ring-blue-500 cursor-pointer" onchange="onOptionSelected('${optKey}')">
          <span class="w-5 h-5 rounded-full bg-slate-100 border border-slate-300 text-slate-700 text-[11px] font-bold flex items-center justify-center shrink-0 mt-0.5">${optKey}</span>
          ${optText}
        `;
        container.appendChild(label);
      });

      // Update Prev button disabled
      document.getElementById('btnPrev').disabled = appState.currentQIdx === 0;

      updatePaletteItem(qId);
      updatePaletteCounts();
    }

    // Option selected by radio
    function onOptionSelected(optKey) {
      const qId = examQuestions[appState.currentQIdx].id;
      appState.responses[qId].selectedOption = optKey;
      saveSessionToStorage();
    }

    // 1. SAVE & NEXT ACTION
    function handleSaveAndNext() {
      const qId = examQuestions[appState.currentQIdx].id;
      const resp = appState.responses[qId];

      if (resp.selectedOption) {
        resp.state = Q_STATE.ANSWERED;
      } else {
        resp.state = Q_STATE.NOT_ANSWERED;
      }

      saveSessionToStorage();
      moveToNextQuestion();
    }

    // 2. CLEAR RESPONSE ACTION
    function handleClearResponse() {
      const qId = examQuestions[appState.currentQIdx].id;
      appState.responses[qId].selectedOption = null;
      appState.responses[qId].state = Q_STATE.NOT_ANSWERED;
      saveSessionToStorage();
      renderQuestion();
    }

    // 3. MARK FOR REVIEW & NEXT ACTION
    function handleMarkForReview() {
      const qId = examQuestions[appState.currentQIdx].id;
      const resp = appState.responses[qId];

      if (resp.selectedOption) {
        resp.state = Q_STATE.ANSWERED_AND_MARKED;
      } else {
        resp.state = Q_STATE.MARKED_FOR_REVIEW;
      }

      saveSessionToStorage();
      moveToNextQuestion();
    }

    // 4. PREVIOUS ACTION
    function handlePreviousQuestion() {
      if (appState.currentQIdx > 0) {
        appState.currentQIdx--;
        visitQuestion(appState.currentQIdx);
      }
    }

    function moveToNextQuestion() {
      if (appState.currentQIdx < examQuestions.length - 1) {
        appState.currentQIdx++;
        visitQuestion(appState.currentQIdx);
      } else {
        openSubmitModal();
      }
    }

    function visitQuestion(idx) {
      appState.currentQIdx = idx;
      const qId = examQuestions[idx].id;
      if (appState.responses[qId].state === Q_STATE.NOT_VISITED) {
        appState.responses[qId].state = Q_STATE.NOT_ANSWERED;
      }
      renderQuestion();
      renderPalette();
    }

    function jumpToQuestionPalette(idx) {
      visitQuestion(idx);
    }

    // Palette Generation
    function renderPalette() {
      const grid = document.getElementById('cbtPaletteGrid');
      grid.innerHTML = '';

      examQuestions.forEach((q, idx) => {
        const btn = document.createElement('button');
        btn.id = 'palBtn-' + q.id;
        btn.innerText = (idx + 1);
        btn.title = 'Question ' + (idx + 1);
        btn.onclick = () => jumpToQuestionPalette(idx);
        applyPaletteStyle(btn, q.id, idx);
        grid.appendChild(btn);
      });
    }

    function applyPaletteStyle(btn, qId, idx) {
      const resp = appState.responses[qId];
      const isCurrent = idx === appState.currentQIdx;

      let cls = "palette-btn ";
      if (resp.state === Q_STATE.ANSWERED) cls += "state-answered ";
      else if (resp.state === Q_STATE.NOT_ANSWERED) cls += "state-not-answered ";
      else if (resp.state === Q_STATE.MARKED_FOR_REVIEW) cls += "state-marked-review ";
      else if (resp.state === Q_STATE.ANSWERED_AND_MARKED) cls += "state-answered-marked ";
      else cls += "state-not-visited ";

      if (isCurrent) cls += "active-current ";

      btn.className = cls;
    }

    function updatePaletteItem(qId) {
      const idx = appState.currentQIdx;
      const btn = document.getElementById('palBtn-' + qId);
      if (btn) applyPaletteStyle(btn, qId, idx);
    }

    function updatePaletteCounts() {
      let ans = 0, notAns = 0, notVis = 0, marked = 0, ansMarked = 0;

      Object.values(appState.responses).forEach(r => {
        if (r.state === Q_STATE.ANSWERED) ans++;
        else if (r.state === Q_STATE.NOT_ANSWERED) notAns++;
        else if (r.state === Q_STATE.MARKED_FOR_REVIEW) marked++;
        else if (r.state === Q_STATE.ANSWERED_AND_MARKED) ansMarked++;
        else notVis++;
      });

      document.getElementById('cntAnswered').innerText = ans;
      document.getElementById('cntNotAnswered').innerText = notAns;
      document.getElementById('cntNotVisited').innerText = notVis;
      document.getElementById('cntMarked').innerText = marked;
      document.getElementById('cntAnsweredMarked').innerText = ansMarked;

      // Update Modal Counts
      document.getElementById('modalAnsCount').innerText = ans;
      document.getElementById('modalNotAnsCount').innerText = notAns;
      document.getElementById('modalMarkedCount').innerText = marked;
      document.getElementById('modalAnsMarkedCount').innerText = ansMarked;
      document.getElementById('modalNotVisitedCount').innerText = notVis;
    }

    // Modal Control
    function openSubmitModal() {
      updatePaletteCounts();
      document.getElementById('submissionModal').classList.remove('hidden');
    }

    function closeSubmitModal() {
      document.getElementById('submissionModal').classList.add('hidden');
    }

    // Final Submission Logic & Result Calculation
    function submitExaminationConfirmed() {
      appState.examSubmitted = true;
      if (appState.examTimerInterval) clearInterval(appState.examTimerInterval);
      closeSubmitModal();

      // Clear ongoing session
      localStorage.removeItem('mppsc_cbt_session_responses');

      // Calculate Scores strictly under requested practice rules
      let correct = 0;
      let incorrect = 0;
      let unattempted = 0;

      examQuestions.forEach(q => {
        const resp = appState.responses[q.id];
        // Note: In official CBT, both ANSWERED and ANSWERED_AND_MARKED have answers evaluated
        const sel = resp.selectedOption;
        if (!sel) {
          unattempted++;
        } else if (sel === q.correct) {
          correct++;
        } else {
          incorrect++;
        }
      });

      const finalScore = (correct * 1.0) - (incorrect * 0.25);
      const attempted = correct + incorrect;
      const accuracy = attempted > 0 ? ((correct / attempted) * 100).toFixed(1) : "0.0";
      const timeSpentSec = (120 * 60) - appState.examSecondsRemaining;
      const timeSpentStr = `${Math.floor(timeSpentSec / 60)}m ${timeSpentSec % 60}s`;

      // Save to Test History
      const attemptRecord = {
        testNo: "01",
        date: new Date().toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }),
        dateTime: new Date().toLocaleString(),
        score: finalScore.toFixed(2),
        correct: correct,
        incorrect: incorrect,
        unattempted: unattempted,
        accuracy: accuracy + "%",
        timeTaken: timeSpentStr,
        timestamp: Date.now()
      };

      appState.history.unshift(attemptRecord);
      saveHistoryToStorage();

      // Populate Result Screen
      document.getElementById('resDateDisplay').innerText = attemptRecord.dateTime;
      document.getElementById('resFinalScore').innerText = finalScore.toFixed(2);
      document.getElementById('resCorrectCount').innerText = correct;
      document.getElementById('resIncorrectCount').innerText = incorrect;
      document.getElementById('resUnattemptedCount').innerText = unattempted;
      document.getElementById('resAccuracyPercent').innerText = accuracy + "%";
      document.getElementById('resTimeTakenDisplay').innerText = timeSpentStr;

      // Comparison note
      const compNote = document.getElementById('resComparisonNote');
      if (appState.history.length > 1) {
        const prev = appState.history[1];
        const diff = (finalScore - parseFloat(prev.score)).toFixed(2);
        const sign = diff >= 0 ? "+" : "";
        compNote.innerText = `Compared to previous test: ${sign}${diff} marks (${prev.score} on ${prev.date})`;
      } else {
        compNote.innerText = `First test recorded in history. Keep practicing daily!`;
      }

      // Render solutions
      renderResultSolutions('ALL');
      updateDashboardCounts();
      renderDashboardHistory();

      switchView('RESULT');
    }

    // Render Solutions
    let currentSolutionFilter = 'ALL';

    function filterResultSolutions(mode) {
      currentSolutionFilter = mode;
      ['ALL', 'CORRECT', 'INCORRECT', 'UNATTEMPTED'].forEach(m => {
        const btn = document.getElementById('resFilter-' + m);
        if (m === mode) {
          btn.className = "px-3 py-1.5 rounded-md font-semibold bg-blue-900 text-white transition";
        } else {
          btn.className = "px-3 py-1.5 rounded-md font-semibold bg-slate-100 text-slate-600 hover:bg-slate-200 transition";
        }
      });
      renderResultSolutions(mode);
    }

    function renderResultSolutions(mode) {
      const container = document.getElementById('resultSolutionsList');
      container.innerHTML = '';

      examQuestions.forEach((q, idx) => {
        const resp = appState.responses[q.id];
        const userChoice = resp.selectedOption;
        const isCorrect = userChoice === q.correct;
        const isSkipped = !userChoice;

        if (mode === 'CORRECT' && !isCorrect) return;
        if (mode === 'INCORRECT' && (isCorrect || isSkipped)) return;
        if (mode === 'UNATTEMPTED' && !isSkipped) return;

        let badge = '';
        let cardBorder = 'border-slate-200';

        if (isSkipped) {
          badge = '<span class="px-2.5 py-0.5 rounded text-[11px] font-bold bg-slate-100 text-slate-600 border border-slate-300">Unattempted (0 Marks)</span>';
        } else if (isCorrect) {
          badge = '<span class="px-2.5 py-0.5 rounded text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-300">Correct (+1.00 Mark)</span>';
          cardBorder = 'border-emerald-300 bg-emerald-50/20';
        } else {
          badge = '<span class="px-2.5 py-0.5 rounded text-[11px] font-bold bg-rose-100 text-rose-800 border border-rose-300">Incorrect (−0.25 Marks)</span>';
          cardBorder = 'border-rose-300 bg-rose-50/20';
        }

        const card = document.createElement('div');
        card.className = `p-4 rounded-xl border ${cardBorder} bg-white space-y-3`;

        const letters = ['A', 'B', 'C', 'D'];
        let optionsHtml = '';
        letters.forEach((l, optIdx) => {
          let optStyle = 'border-slate-200 bg-slate-50 text-slate-700';
          if (l === q.correct) {
            optStyle = 'border-emerald-500 bg-emerald-50 text-emerald-900 font-bold';
          } else if (userChoice === l && !isCorrect) {
            optStyle = 'border-rose-500 bg-rose-50 text-rose-900 font-semibold';
          }

          optionsHtml += `
            <div class="p-2.5 rounded-lg border ${optStyle} flex items-start gap-2 text-xs">
              <span class="font-bold shrink-0">${l}.</span>
              <div class="flex-1">
                <div>${q.options_en[optIdx]}</div>
                <div class="hindi-text text-slate-500 mt-0.5">${q.options_hi[optIdx]}</div>
              </div>
            </div>
          `;
        });

        let sourceBadge = '';
        if (q.source_type === 'PYQ_VERIFIED' && q.pyq_metadata) {
          sourceBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-900 border border-amber-300">🏛️ ${q.pyq_metadata.exam} ${q.pyq_metadata.year} (${q.pyq_metadata.paper})</span>`;
        } else {
          sourceBadge = `<span class="px-2 py-0.5 rounded text-[10px] font-semibold bg-blue-50 text-blue-800 border border-blue-200">✨ Verified Exam Practice</span>`;
        }

        card.innerHTML = `
          <div class="flex items-center justify-between border-b border-slate-100 pb-2">
            <div class="flex items-center gap-2">
              <span class="font-bold text-xs text-blue-950">Question ${idx + 1}</span>
              ${sourceBadge}
            </div>
            <div>${badge}</div>
          </div>
          <div class="text-xs md:text-sm font-medium text-slate-800">${q.question_en}</div>
          <div class="hindi-text text-xs md:text-sm text-slate-600">${q.question_hi}</div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
            ${optionsHtml}
          </div>

          <div class="bg-blue-50/70 border border-blue-200 rounded-lg p-3 text-xs space-y-1.5 mt-2">
            <div class="font-bold text-blue-900">Official Correct Answer: Option (${q.correct})</div>
            <div class="text-slate-700 leading-relaxed">${q.explanation_en}</div>
            <div class="hindi-text text-slate-600 leading-relaxed pt-1 border-t border-blue-100">${q.explanation_hi}</div>
          </div>
        `;
        container.appendChild(card);
      });
    }

    // Persistence: Local Storage
    function saveSessionToStorage() {
      localStorage.setItem('mppsc_cbt_session_responses', JSON.stringify(appState.responses));
    }

    function saveHistoryToStorage() {
      localStorage.setItem('mppsc_exam_history', JSON.stringify(appState.history));
    }

    function loadHistoryFromStorage() {
      const saved = localStorage.getItem('mppsc_exam_history');
      if (saved) {
        try { appState.history = JSON.parse(saved); } catch(e){}
      }
    }

    // Dashboard Statistics Updates
    function updateDashboardCounts() {
      const history = appState.history;
      document.getElementById('statTotalTests').innerText = history.length;

      if (history.length > 0) {
        let totalScore = 0;
        let totalAccuracy = 0;
        let best = -999;

        history.forEach(h => {
          const s = parseFloat(h.score);
          totalScore += s;
          totalAccuracy += parseFloat(h.accuracy);
          if (s > best) best = s;
        });

        document.getElementById('statAvgScore').innerText = (totalScore / history.length).toFixed(2);
        document.getElementById('statBestScore').innerText = best.toFixed(2);
        document.getElementById('statAvgAccuracy').innerText = (totalAccuracy / history.length).toFixed(1) + '%';
      } else {
        document.getElementById('statAvgScore').innerText = '--';
        document.getElementById('statBestScore').innerText = '--';
        document.getElementById('statAvgAccuracy').innerText = '--';
      }
    }

    function renderDashboardHistory() {
      const tbodyRecent = document.getElementById('recentHistoryTableBody');
      const tbodyFull = document.getElementById('fullHistoryTableBody');

      if (!tbodyRecent || !tbodyFull) return;

      tbodyRecent.innerHTML = '';
      tbodyFull.innerHTML = '';

      if (appState.history.length === 0) {
        const emptyRow = `
          <tr>
            <td colspan="8" class="p-6 text-center text-slate-400">
              No examination attempts recorded yet. Attempt Test 01 to start your history log.
            </td>
          </tr>
        `;
        tbodyRecent.innerHTML = emptyRow;
        tbodyFull.innerHTML = emptyRow;
        return;
      }

      appState.history.forEach((h, idx) => {
        const rowHtml = `
          <tr class="hover:bg-slate-50 transition">
            <td class="p-3 font-bold text-blue-950">Test ${h.testNo}</td>
            <td class="p-3 text-slate-600">${h.date}</td>
            <td class="p-3 text-right font-extrabold text-blue-900">${h.score}</td>
            <td class="p-3 text-center text-emerald-600 font-bold">${h.correct}</td>
            <td class="p-3 text-center text-rose-600 font-bold">${h.incorrect}</td>
            <td class="p-3 text-center text-slate-500">${h.unattempted}</td>
            <td class="p-3 text-right font-semibold text-purple-700">${h.accuracy}</td>
            <td class="p-3 text-right text-slate-500">${h.timeTaken}</td>
          </tr>
        `;
        if (idx < 5) tbodyRecent.innerHTML += rowHtml;
        tbodyFull.innerHTML += rowHtml;
      });
    }
  </script>
</body>
</html>
"""

output_path = r"c:\Users\hp\Documents\antigravity\wonderful-noether\mppsc_cbt_portal.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_content)

artifact_path = r"C:\Users\hp\.gemini\antigravity\brain\64f902af-bbcc-4039-8dbe-53e6635bff0f\mppsc_cbt_portal.html"
with open(artifact_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("Professional CBT Examination Portal successfully built!")
