@echo off
title LYGO-Claw Try Gateway
cd /d "%~dp0.."
set PYTHONPATH=%CD%\src
python -m lygo_claw.cli gateway "Hello from LYGO-Claw - quick test"
pause