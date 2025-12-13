# AutoGLM Desktop Application Startup Script (PowerShell Version)

Write-Host "Starting AutoGLM Desktop Application..." -ForegroundColor Green
Write-Host ""

# Set UTF-8 encoding
$env:PYTHONIOENCODING = "utf-8"

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python version: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found, please install Python 3.10 or higher" -ForegroundColor Red
    Write-Host "Download URL: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if in the correct directory
if (-not (Test-Path "autoglm_desktop.py")) {
    Write-Host "Error: autoglm_desktop.py file not found" -ForegroundColor Red
    Write-Host "Please ensure you are running this script in the AutoGLM project directory" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Start the desktop application
Write-Host "Starting AutoGLM Desktop Application..." -ForegroundColor Green
try {
    python autoglm_desktop.py
} catch {
    Write-Host "Application exited abnormally: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}