@echo off
setlocal enabledelayedexpansion
title LYGO CLAW Launch

set "USB=%~dp0"
if "%USB:~-1%"=="\" set "USB=%USB:~0,-1%"

echo ================================================
echo  LYGO CLAW Standalone USB Launch
echo  USB: %USB%
echo ================================================
echo.

echo [1/5] Stopping conflicting node/ollama processes...
taskkill /F /IM node.exe >nul 2>&1
taskkill /F /IM ollama.exe >nul 2>&1
timeout /t 2 /nobreak >nul

echo [2/5] Starting portable USB Ollama...
start "LYGO Ollama" /MIN cmd /c ""%USB%\LYGO_Ollama_USB_Boot.bat""

echo [3/5] Waiting for Ollama warm-up...
timeout /t 6 /nobreak >nul

echo [4/5] Starting isolated LYGO CLAW Gateway...
start "LYGO CLAW Gateway" cmd /k ""%USB%\LYGO_Gateway.cmd""

echo [5/5] Waiting for gateway, then opening dashboards...
timeout /t 12 /nobreak >nul
start "" "%USB%\dashboard\lygo-claw.html"
if exist "%USB%\dashboard\control-ui\index.html" start "" "%USB%\dashboard\control-ui\index.html"

echo.
echo LYGO CLAW launch complete.
echo   Gateway: ws://127.0.0.1:18789
echo   Ollama:  http://127.0.0.1:11434
echo   Token:   lygo-usb-standalone-token
echo.
endlocal