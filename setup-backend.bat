@echo off
echo ========================================
echo Setting up Backend
echo ========================================
echo.

cd backend

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env file created. Please edit it with your database password.
    notepad .env
)

echo.
echo Creating directories...
if not exist uploads mkdir uploads
if not exist processed mkdir processed
if not exist models mkdir models

echo.
echo ========================================
echo Backend setup complete!
echo ========================================
echo.
echo To start the backend:
echo 1. cd backend
echo 2. venv\Scripts\activate
echo 3. python main.py
echo.
pause
