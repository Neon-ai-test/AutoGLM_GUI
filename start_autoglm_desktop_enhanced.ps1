# AutoGLM Desktop Application Startup Script (PowerShell Version)

Write-Host "AutoGLM Desktop Application - Enhanced Version" -ForegroundColor Green
Write-Host ""

# Set UTF-8 encoding
$env:PYTHONIOENCODING = "utf-8"

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python version: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python not found, please install Python 3.7 or higher" -ForegroundColor Red
    Write-Host "Download URL: https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if CustomTkinter is installed
try {
    python -c "import customtkinter" 2>&1 | Out-Null
    Write-Host "CustomTkinter is already installed" -ForegroundColor Green
} catch {
    Write-Host "Installing CustomTkinter..." -ForegroundColor Yellow
    try {
        python -m pip install customtkinter
        Write-Host "CustomTkinter installed successfully" -ForegroundColor Green
    } catch {
        Write-Host "Error: Failed to install CustomTkinter" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Check if in the correct directory
if (-not (Test-Path "autoglm_desktop_enhanced.py")) {
    Write-Host "Error: autoglm_desktop_enhanced.py file not found" -ForegroundColor Red
    Write-Host "Please ensure you are running this script in the AutoGLM project directory" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Start the desktop application
Write-Host "Starting AutoGLM Desktop Application..." -ForegroundColor Green
try {
    python autoglm_desktop_enhanced.py
    $exitCode = $LASTEXITCODE
    if ($exitCode -ne 0) {
        Write-Host ""
        Write-Host "Application exited with error code: $exitCode" -ForegroundColor Red
        Read-Host "Press Enter to exit"
    }
} catch {
    Write-Host "Application exited abnormally: $_" -ForegroundColor Red
    Read-Host "Press Enter to exit"
}