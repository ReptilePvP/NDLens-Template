@echo off
title OpenLens - Full Application Launcher
color 0B

echo.
echo ================================================================
echo                    🔍 OpenLens Full Launcher 🔍
echo ================================================================
echo.
echo Starting OpenLens API server and web interface...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "main.py" (
    echo ❌ main.py not found
    pause
    exit /b 1
)

if not exist "try_interface.html" (
    echo ❌ try_interface.html not found
    pause
    exit /b 1
)

echo ✅ Python found and required files detected
echo.
echo 🚀 Starting OpenLens Full Application...
echo.
echo 📝 Note: This will open two services:
echo    - API Server: http://127.0.0.1:8000
echo    - Web Interface: http://127.0.0.1:3000/try_interface.html
echo.
echo ⚠️  To stop the application, close this window or press Ctrl+C
echo.

REM Start the full application
python start_openlens_full.py

echo.
echo 👋 OpenLens has been stopped
pause
