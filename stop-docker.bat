@echo off
echo ========================================
echo Stopping Docker Services
echo ========================================
echo.

docker-compose down

echo.
echo All services stopped.
echo.
pause
