# MPPSC Daily Mock Test & Online Examination Platform

A professional, automated MPPSC (Madhya Pradesh Public Service Commission) Computer-Based Test (CBT) platform with real-time 8:00 PM examination delivery, authentic PYQ engine, and automated cloud email dispatcher.

---

## 🌟 Key Features

1. **Authentic CBT Portal Layout (`mppsc_cbt_portal.html`)**:
   - Designed to match official TCS iON / NTA competitive exam software.
   - Real-time 8:00 PM IST lock & auto-unlock mechanism with countdown timer.
   - Official 5 question states (Not Visited, Not Answered, Answered, Marked for Review, Answered & Marked for Review).
   - 120-minute countdown timer with automatic submission on expiry.
   - Comprehensive post-submission review with bilingual explanations for all 100 questions.
   - Verified MPPSC PYQ attributions (2018–2023) and topic tags.
   - Persistent `localStorage` candidate history tracking.

2. **Automated Cloud Dispatcher (7:58 PM IST Daily)**:
   - GitHub Actions workflow runs every day at **7:58 PM IST** (14:28 UTC) completely in the cloud.
   - Delivers the test 2 minutes before the test window opens to the candidate's inbox.
   - Works 24/7 even if your personal computer is turned off.

3. **MPPSC Question Quality & Deduplication Engine (`engine/`)**:
   - 10-Unit syllabus blueprint coverage (MP History, Geography, Polity, National GS, ICT, Commissions).
   - Exact and semantic duplicate detection (Jaccard similarity index).
   - Strict scoring validation: `+1.00 Correct`, `-0.25 Incorrect`, `0.00 Unattempted` (Total: 100 Marks).

---

## 🔐 Setting Up GitHub Secrets (For 7:58 PM Cloud Email Dispatch)

To enable GitHub's cloud servers to dispatch the daily test emails when your computer is shut down:

1. In your GitHub repository (`Aadarshsingh1/mppsc-daily-test`), click **Settings** $\rightarrow$ **Secrets and variables** $\rightarrow$ **Actions**.
2. Click **New repository secret** and add these three secrets:
   - `SENDER_EMAIL` : `aadarshthakurt@gmail.com`
   - `SENDER_APP_PASSWORD` : Your 16-character Google App Password (`rfessayoqziarmgd`)
   - `RECIPIENT_EMAIL` : `sharmaaastha073@gmail.com`

---

## 🌐 Enabling GitHub Pages (Live Web Portal)

1. In your repository, go to **Settings** $\rightarrow$ **Pages**.
2. Under **Build and deployment** $\rightarrow$ **Source**, choose **GitHub Actions**.
3. Your live online test portal will be available at:
   `https://Aadarshsingh1.github.io/mppsc-daily-test/`

---

## 🧪 Running Automated Tests

```bash
python -m unittest tests.test_suite -v
```
All 15 unit and integration tests verify scoring, deduplication, question validation, and IST time boundaries.
