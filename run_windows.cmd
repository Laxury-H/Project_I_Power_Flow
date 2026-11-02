@echo off
chcp 65001 >nul
title PowerFlow - Do an 1
cd /d "%~dp0"
set "PY=python"
if exist ".venv\Scripts\python.exe" set "PY=.venv\Scripts\python.exe"
"%PY%" app.py
if errorlevel 1 pause