@echo off
setlocal
cd /d "%~dp0"
set "PYTHON_EXE=py -3.12"
py -3.12 --version >nul 2>&1
if errorlevel 1 (
  python --version >nul 2>&1
  if errorlevel 1 (
    echo Python was not found. Read START_HERE_VI.md for manual setup.
    pause
    exit /b 1
  )
  set "PYTHON_EXE=python"
)
if not exist ".venv\Scripts\python.exe" (
  %PYTHON_EXE% -m venv .venv
  if errorlevel 1 goto failed
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto failed
echo Setup complete. Open run_windows.cmd to start the application.
pause
exit /b 0
:failed
echo Setup failed. Read the error above and START_HERE_VI.md.
pause
exit /b 1
