#!/bin/bash

set -e

echo "Installing MindSafe backend and frontend dependencies"
echo "===================================================="

if [ ! -d backend/venv ]; then
    python3 -m venv backend/venv
fi
source backend/venv/bin/activate
pip install -r backend/requirements.txt

cd frontend
npm install
cd ..

echo ""
echo "Setup complete."
echo "1. Copy backend/.env.example to backend/.env and add GEMINI_API_KEY if desired."
echo "2. Copy frontend/.env.example to frontend/.env if it does not already exist."
echo "3. Run ./start.sh"
