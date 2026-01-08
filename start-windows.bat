@echo off
echo ========================================
echo Clash Royale Analyzer - Windows Starter
echo ========================================
echo.

REM Check if Docker is available
docker --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Docker detected! Starting with Docker...
    echo.
    docker-compose up -d
    echo.
    echo ========================================
    echo Application started successfully!
    echo ========================================
    echo.
    echo Frontend: http://localhost:3000
    echo Backend:  http://localhost:8000
    echo API Docs: http://localhost:8000/docs
    echo.
    echo Press any key to view logs, or close this window.
    pause >nul
    docker-compose logs -f
) else (
    echo Docker not found. Please use manual setup.
    echo.
    echo See WINDOWS_SETUP.md for detailed instructions.
    echo.
    echo Quick summary:
    echo 1. Install Python, Node.js, PostgreSQL, Redis
    echo 2. Run setup-backend.bat
    echo 3. Run setup-frontend.bat
    echo.
    pause
)
