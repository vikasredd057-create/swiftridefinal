@echo off
echo ========================================
echo Starting SwiftRide Broadcast System
echo ========================================
echo.

echo Starting Backend Service (Port 8001)...
start "Backend Service" cmd /k "python -m uvicorn backend_service.main:app --host 0.0.0.0 --port 8001"
timeout /t 3 /nobreak >nul

echo Starting User Service (Port 8000)...
start "User Service" cmd /k "python -m uvicorn user_service.main:app --host 0.0.0.0 --port 8000"
timeout /t 2 /nobreak >nul

echo Starting Driver: Rajesh Kumar (Port 9001)...
start "Driver - Rajesh Kumar" cmd /k "set DRIVER_ID=1 && set DRIVER_NAME=Rajesh Kumar && set DRIVER_PORT=9001 && python -m uvicorn driver_instance.main:app --host 0.0.0.0 --port 9001"
timeout /t 1 /nobreak >nul

echo Starting Driver: Amit Singh (Port 9002)...
start "Driver - Amit Singh" cmd /k "set DRIVER_ID=2 && set DRIVER_NAME=Amit Singh && set DRIVER_PORT=9002 && python -m uvicorn driver_instance.main:app --host 0.0.0.0 --port 9002"
timeout /t 1 /nobreak >nul

echo Starting Driver: Priya Sharma (Port 9003)...
start "Driver - Priya Sharma" cmd /k "set DRIVER_ID=3 && set DRIVER_NAME=Priya Sharma && set DRIVER_PORT=9003 && python -m uvicorn driver_instance.main:app --host 0.0.0.0 --port 9003"
timeout /t 1 /nobreak >nul

echo Starting Driver: Vikram Patel (Port 9004)...
start "Driver - Vikram Patel" cmd /k "set DRIVER_ID=4 && set DRIVER_NAME=Vikram Patel && set DRIVER_PORT=9004 && python -m uvicorn driver_instance.main:app --host 0.0.0.0 --port 9004"
timeout /t 1 /nobreak >nul

echo Starting Driver: Sunita Reddy (Port 9005)...
start "Driver - Sunita Reddy" cmd /k "set DRIVER_ID=5 && set DRIVER_NAME=Sunita Reddy && set DRIVER_PORT=9005 && python -m uvicorn driver_instance.main:app --host 0.0.0.0 --port 9005"

echo.
echo ========================================
echo All Services Started!
echo ========================================
echo.
echo User Interface:     http://localhost:8000
echo Backend API:        http://localhost:8001
echo.
echo Driver Dashboards:
echo   Rajesh Kumar:     http://localhost:9001
echo   Amit Singh:       http://localhost:9002
echo   Priya Sharma:     http://localhost:9003
echo   Vikram Patel:     http://localhost:9004
echo   Sunita Reddy:     http://localhost:9005
echo.
echo Press any key to close this window...
pause >nul
