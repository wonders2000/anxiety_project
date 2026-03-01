#!/usr/bin/env pwsh
# Setup script for Anxiety Detection Streamlit Dashboard (PowerShell)
# Run this file to set up the environment automatically

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Anxiety Detection Dashboard Setup" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.9+ from https://www.python.org" -ForegroundColor Yellow
    exit 1
}

Write-Host "[1/4] Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host "[2/4] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to activate virtual environment" -ForegroundColor Red
    exit 1
}

Write-Host "[3/4] Upgrading pip, setuptools, and wheel..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠ Warning: Failed to upgrade pip" -ForegroundColor Yellow
}

Write-Host "[4/4] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Failed to install requirements" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Cyan
Write-Host "  1. Ensure the virtual environment is activated" -ForegroundColor White
Write-Host "  2. Run: streamlit run streamlit_app.py" -ForegroundColor White
Write-Host ""
Write-Host "Virtual environment location: $(Get-Location)\venv" -ForegroundColor Gray
Write-Host ""
