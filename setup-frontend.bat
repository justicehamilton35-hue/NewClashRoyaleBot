@echo off
echo ========================================
echo Setting up Frontend
echo ========================================
echo.

cd frontend

echo Installing dependencies (this may take a few minutes)...
call npm install

echo.
echo ========================================
echo Frontend setup complete!
echo ========================================
echo.
echo To start the frontend:
echo 1. cd frontend
echo 2. npm run dev
echo.
pause
