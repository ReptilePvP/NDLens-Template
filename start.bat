@echo off
title OpenLens Application
color 0B

echo.
echo ================================================================
echo                    🔍 OpenLens Application 🔍
echo ================================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo ✅ Python found
echo 🚀 Starting OpenLens...
echo.

REM Start the application
python start.py

echo.
echo 👋 OpenLens has been stopped
pause
