#!/bin/bash

set -e

echo "Starting MindSafe"
echo "=================="

if [ ! -f backend/.env ]; then
    cp backend/.env.example backend/.env
    echo "Created backend/.env from template. Add your GEMINI_API_KEY if you want Gemini responses."
fi

if [ ! -f frontend/.env ]; then
    cp frontend/.env.example frontend/.env
    echo "Created frontend/.env from template."
fi

echo ""
echo "Installing backend dependencies if needed..."
cd backend
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
source venv/bin/activate
pip install -q -r requirements.txt
python main.py &
BACKEND_PID=$!
cd ..

echo ""
echo "Installing frontend dependencies if needed..."
cd frontend
if [ ! -d "node_modules" ]; then
    npm install
fi
npm run dev -- --host 0.0.0.0 &
FRONTEND_PID=$!
cd ..

echo ""
echo "MindSafe is starting."
echo "Frontend: http://localhost:5173"
echo "Backend:  http://localhost:8000"
echo ""
echo "If the Git LFS model files are missing, the backend will start in support-only mode."
echo "Press Ctrl+C to stop both services."

trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT TERM
wait
