# -*- coding: utf-8 -*-
"""
Daily MPPSC Mock Test Dispatcher
Automated daily test generator & email sender for MPPSC preparation.
"""
import os
import sys
import json
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(WORKSPACE_DIR, "email_config.json")
LOG_FILE = os.path.join(WORKSPACE_DIR, "daily_dispatch.log")

def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {msg}"
    print(formatted)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted + "\n")

def load_config():
    # 1. First check environment variables (ideal for GitHub Actions / Cloud deployment)
    if os.environ.get("SENDER_EMAIL") and os.environ.get("SENDER_APP_PASSWORD"):
        return {
            "sender_email": os.environ.get("SENDER_EMAIL"),
            "sender_app_password": os.environ.get("SENDER_APP_PASSWORD"),
            "recipient_email": os.environ.get("RECIPIENT_EMAIL", "sharmaaastha073@gmail.com"),
            "portal_url": os.environ.get("PORTAL_PUBLIC_URL", "")
        }

    # 2. Fallback to local email_config.json
    if not os.path.exists(CONFIG_FILE):
        log(f"Error: Configuration file '{CONFIG_FILE}' not found.")
        return None
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            cfg = json.load(f)
            cfg.setdefault("portal_url", "")
            return cfg
    except Exception as e:
        log(f"Error reading configuration file: {e}")
        return None

def send_test_email():
    config = load_config()
    if not config:
        return False

    sender_email = config.get("sender_email", "").strip()
    sender_password = config.get("sender_app_password", "").strip().replace(" ", "")
    recipient_email = config.get("recipient_email", "sharmaaastha073@gmail.com").strip()

    if not sender_email or "YOUR_GMAIL" in sender_email:
        log("Error: Please set your sender_email in email_config.json")
        return False

    if not sender_password or "YOUR_16_DIGIT" in sender_password:
        log("Error: Please set your 16-digit Google App Password in email_config.json")
        return False

    # Check for test HTML file (prioritize full CBT portal)
    test_html_file = os.path.join(WORKSPACE_DIR, "mppsc_cbt_portal.html")
    if not os.path.exists(test_html_file):
        test_html_file = os.path.join(WORKSPACE_DIR, "mppsc_mock_test_01.html")
    if not os.path.exists(test_html_file):
        log(f"Error: Test file not found at {test_html_file}")
        return False

    today_str = datetime.now().strftime("%d %B %Y")
    subject = f"🎯 Daily MPPSC Mock Test — {today_str} (Window: 8:00 PM IST)"

    # Create Multipart Email
    msg = MIMEMultipart()
    msg['From'] = f"MPPSC Exam Prep <{sender_email}>"
    msg['To'] = recipient_email
    msg['Subject'] = subject

    portal_url = config.get("portal_url", "").strip()
    online_button_html = ""
    if portal_url:
        online_button_html = f"""
        <div style="text-align: center; margin: 20px 0;">
          <a href="{portal_url}" class="btn" style="background-color: #15803d; color: #ffffff; padding: 14px 28px; text-decoration: none; border-radius: 8px; font-weight: bold; font-size: 15px; display: inline-block;">
            🌐 Click to Open Online Examination Portal
          </a>
          <p style="font-size: 11px; color: #64748b; margin-top: 6px;">Link automatically unlocks at 8:00 PM IST</p>
        </div>
        """

    # HTML Email Body
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .header {{ background: #1e3a8a; color: white; padding: 20px; border-radius: 8px 8px 0 0; text-align: center; }}
        .content {{ padding: 20px; border: 1px solid #e2e8f0; border-top: none; border-radius: 0 0 8px 8px; }}
        .card {{ background: #f8fafc; border: 1px solid #cbd5e1; padding: 15px; border-radius: 6px; margin: 15px 0; }}
        .btn {{ display: inline-block; background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; font-weight: bold; margin-top: 10px; }}
        .footer {{ font-size: 12px; color: #64748b; margin-top: 20px; text-align: center; }}
      </style>
    </head>
    <body>
      <div class="header">
        <h2>Madhya Pradesh Public Service Commission (MPPSC)</h2>
        <p>Daily Practice Mock Test — General Studies Paper 1</p>
      </div>
      <div class="content">
        <p>Hello,</p>
        <p>Your daily MPPSC Mock Test for <strong>{today_str}</strong> has been delivered at <strong>7:58 PM IST</strong> (2 minutes early) so you can prepare your workspace before the test window opens at <strong>8:00 PM IST</strong>.</p>
        
        {online_button_html}

        <div class="card">
          <h3 style="margin-top:0; color: #1e3a8a;">📋 Test Structure:</h3>
          <ul>
            <li><strong>Total Questions:</strong> 100 MCQs (Bilingual: हिन्दी & English)</li>
            <li><strong>Duration:</strong> 120 Minutes</li>
            <li><strong>Marking Scheme:</strong> Correct: +1.00 | Incorrect: -0.25 | Unattempted: 0.00</li>
            <li><strong>Syllabus Coverage:</strong> Complete 10 Units (MP History, Indian History, MP Geography, World/Ind Geography, MP Polity/Econ, Indian Constitution, Sci-Tech, Current Affairs, ICT/AI, Commissions).</li>
          </ul>
        </div>

        <p><strong>Two Ways to Attempt:</strong></p>
        <ol>
          <li><strong>Option A (Online):</strong> Click the green portal button above (if link provided).</li>
          <li><strong>Option B (Direct File):</strong> Download the attached <code>mppsc_cbt_portal.html</code> and double-click to open in any web browser on your phone or laptop.</li>
        </ol>

        <p class="footer">
          Generated automatically by your Daily MPPSC Exam Trainer system. Best wishes for your exam preparation!
        </p>
      </div>
    </body>
    </html>
    """
    msg.attach(MIMEText(html_body, 'html'))

    # Attach the HTML Mock Test file
    try:
        with open(test_html_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename=mppsc_mock_test_{datetime.now().strftime('%Y%m%d')}.html",
            )
            msg.attach(part)
    except Exception as e:
        log(f"Error attaching file: {e}")
        return False

    # Send Email via Gmail SMTP
    try:
        log(f"Connecting to Gmail SMTP server for {sender_email}...")
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=30)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [recipient_email], msg.as_string())
        server.quit()
        log(f"SUCCESS: Daily MPPSC Mock Test successfully emailed to {recipient_email}!")
        return True
    except Exception as e:
        log(f"Error sending email via SMTP: {e}")
        return False

if __name__ == "__main__":
    success = send_test_email()
    sys.exit(0 if success else 1)
