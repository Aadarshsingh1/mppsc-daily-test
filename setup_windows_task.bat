@echo off
echo ========================================================
echo Setting up Daily MPPSC Test Dispatch at 7:58 PM IST
echo ========================================================
schtasks /create /tn "DailyMPPSCTest" /tr "python \"%~dp0send_daily_test.py\"" /sc daily /st 19:58 /f
if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Windows Task 'DailyMPPSCTest' successfully registered!
    echo It will trigger every day automatically at 7:58 PM (19:58) IST.
) else (
    echo.
    echo [NOTE] If this failed, please right-click this script and select 'Run as Administrator'.
)
pause
