@echo off
echo AutoGLM Desktop Application - Enhanced Version
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python not found, please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Check if CustomTkinter is installed
python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing CustomTkinter...
    python -m pip install customtkinter
    if %errorlevel% neq 0 (
        echo Error: Failed to install CustomTkinter
        pause
        exit /b 1
    )
)

REM Start the application
echo Starting AutoGLM Desktop Application...
python autoglm_desktop_enhanced.py

if %errorlevel% neq 0 (
    echo.
    echo Application exited with error code: %errorlevel%
    pause
)