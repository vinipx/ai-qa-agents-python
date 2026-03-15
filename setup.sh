#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "============================================================"
echo " Setting up AI-Powered Multi-Agent QE Framework"
echo "============================================================"

# 1. Check Python version (requires 3.10+)
echo "[1/4] Checking Python version..."
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python is not installed. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$($PYTHON_CMD -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if awk "BEGIN {exit !($PYTHON_VERSION >= 3.10)}"; then
    echo "✅ Python $PYTHON_VERSION detected."
else
    echo "❌ Error: Python version must be 3.10 or higher. Detected version is $PYTHON_VERSION."
    exit 1
fi

# 2. Setup Virtual Environment
VENV_DIR=".venv"
echo "[2/4] Setting up Python virtual environment in '$VENV_DIR'..."
if [ ! -d "$VENV_DIR" ]; then
    $PYTHON_CMD -m venv $VENV_DIR
    echo "✅ Virtual environment created."
else
    echo "✅ Virtual environment already exists."
fi

# Activate the virtual environment based on OS
if [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* || "$OSTYPE" == "win32"* ]]; then
    source $VENV_DIR/Scripts/activate
else
    source $VENV_DIR/bin/activate
fi

# 3. Upgrade Pip
echo "[3/4] Upgrading pip..."
pip install --upgrade pip --quiet
echo "✅ pip upgraded."

# 4. Install Dependencies
echo "[4/4] Installing required packages from pyproject.toml..."
if [ -f "pyproject.toml" ]; then
    pip install .
    echo "✅ Packages installed successfully."
else
    echo "❌ Error: pyproject.toml not found!"
    exit 1
fi

# Copy .env.example to .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Copying .env.example to .env..."
    cp .env.example .env
    echo "⚠️  Please update the .env file with your API keys!"
fi

echo "============================================================"
echo " Setup Complete! 🎉"
echo "============================================================"
echo "To get started, activate your virtual environment and run the main script:"
echo ""
if [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "cygwin"* || "$OSTYPE" == "win32"* ]]; then
    echo "  source $VENV_DIR/Scripts/activate"
else
    echo "  source $VENV_DIR/bin/activate"
fi
echo "  python main.py"
echo "============================================================"
