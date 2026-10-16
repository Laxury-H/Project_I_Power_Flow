@echo off
setlocal
cd /d "%~dp0\.."
echo Starting PowerFlow Studio Web App on port 8050...
if exist ".venv\Scripts\python.exe" (
  ".venv\Scripts\python.exe" web_app\run_app.py
) else (
  python web_app\run_app.py
)
pause
