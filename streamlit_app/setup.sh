#!/bin/bash
# Setup script for Anxiety Detection Streamlit Dashboard (Linux/macOS)
# Run this file to set up the environment automatically

echo "========================================"
echo "Anxiety Detection Dashboard Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 is not installed or not in PATH"
    echo "Please install Python 3.9+ first"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✓ Python found: $PYTHON_VERSION"

echo "[1/4] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/4] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to activate virtual environment"
    exit 1
fi

echo "[3/4] Upgrading pip, setuptools, and wheel..."
python -m pip install --upgrade pip setuptools wheel
if [ $? -ne 0 ]; then
    echo "WARNING: Failed to upgrade pip"
fi

echo "[4/4] Installing dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install requirements"
    exit 1
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo "  2. Run the app:"
echo "     streamlit run streamlit_app.py"
echo ""
echo "Virtual environment location: $(pwd)/venv"
echo ""
