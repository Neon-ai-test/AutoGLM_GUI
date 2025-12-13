@echo off
echo Starting AutoGLM Desktop Application...
echo.

REM Set UTF-8 encoding
set PYTHONIOENCODING=utf-8

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found, please install Python 3.10 or higher
    echo Download URL: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if in the correct directory
if not exist "autoglm_desktop.py" (
    echo Error: autoglm_desktop.py file not found
    echo Please ensure you are running this script in the AutoGLM project directory
    pause
    exit /b 1
)

REM Start the desktop application
echo Starting AutoGLM Desktop Application...
python autoglm_desktop.py

REM If the application crashes, display error information
if %errorlevel% neq 0 (
    echo.
    echo Application exited abnormally, error code: %errorlevel%
    pause
)