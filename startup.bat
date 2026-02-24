@echo off
echo =====================================
echo Launching AI Cybersecurity System...
echo =====================================

REM 1️⃣ Open VS Code
start "" code .

REM 2️⃣ Start MongoDB (will require admin if service-based)
start "" cmd /k "net start MongoDB"

REM 3️⃣ Start Backend
start "" cmd /k "cd backend && venv\Scripts\activate && python -m uvicorn main:app --reload"

REM 4️⃣ Start Frontend
start "" cmd /k "cd frontend && npm run dev"

REM Wait a few seconds before opening browser
timeout /t 10 >nul

REM Open main first
start http://localhost:5173

REM Small delay so browser fully loads
timeout /t 2 >nul

REM Now open secondary tabs
start http://localhost:5173/dashboard
start http://localhost:8000/docs