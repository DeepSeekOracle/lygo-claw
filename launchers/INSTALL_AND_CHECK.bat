@echo off
title LYGO-Claw Install and Check
cd /d "%~dp0.."
where python >nul 2>&1
if errorlevel 1 (
  echo Install Python 3.11+ from python.org with Add to PATH.
  pause
  exit /b 1
)
python -m pip install -e ".[dev]"
if errorlevel 1 pause & exit /b 1
python scripts\self_check.py
if errorlevel 1 pause & exit /b 1
echo.
echo OK - use TRY_GATEWAY.bat or: lygo-claw gateway "hello"
pause