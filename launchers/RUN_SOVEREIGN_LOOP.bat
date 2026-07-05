@echo off
title LYGO-Claw Sovereign Loop
cd /d "%~dp0.."
set LYGO_CLAW_ROOT=%CD%
set LYGO_STACK_ROOT=I:\E Drive\lygo-protocol-stack
set LYGO_BUILDER_KEY_ROOT=E:\LYGO_BUILDER_KEY
set LYGO_BRAIN_VAULT=E:\LYGO_BUILDER_KEY\data\memory_mycelium\vault
set PYTHONPATH=%CD%\src
python -m lygo_claw.cli sovereign-loop
pause