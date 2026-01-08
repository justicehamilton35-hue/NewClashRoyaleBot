@echo off
echo ========================================
echo Starting Backend Server
echo ========================================
echo.

cd backend
call venv\Scripts\activate.bat

echo Starting FastAPI server...
echo Backend will be available at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py
