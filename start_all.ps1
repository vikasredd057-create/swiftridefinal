# SwiftRide Broadcast System Launcher
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Starting SwiftRide Broadcast System" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Start Backend Service
Write-Host "Starting Backend Service (Port 8001)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn backend_service.main:app --host 0.0.0.0 --port 8001"
Start-Sleep -Seconds 3

# Start User Service
Write-Host "Starting User Service (Port 8000)..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python -m uvicorn user_service.main:app --host 0.0.0.0 --port 8000"
Start-Sleep -Seconds 2

# Start Driver Instances
Write-Host "Starting Driver: Rajesh Kumar (Port 9001)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:DRIVER_ID='1'; `$env:DRIVER_NAME='Rajesh Kumar'; `$env:DRIVER_PORT='9001'; python -m uvicorn driver_instance.main:app --host 0.0.0.0 --port 9001"
Start-Sleep -Seconds 1

Write-Host "Starting Driver: Amit Singh (Port 9002)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:DRIVER_ID='2'; `$env:DRIVER_NAME='Amit Singh'; `$env:DRIVER_PORT='9002'; python -m uvicorn driver_instance.main:app --host 0.0.0.0 --port 9002"
Start-Sleep -Seconds 1

Write-Host "Starting Driver: Priya Sharma (Port 9003)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:DRIVER_ID='3'; `$env:DRIVER_NAME='Priya Sharma'; `$env:DRIVER_PORT='9003'; python -m uvicorn driver_instance.main:app --host 0.0.0.0 --port 9003"
Start-Sleep -Seconds 1

Write-Host "Starting Driver: Vikram Patel (Port 9004)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:DRIVER_ID='4'; `$env:DRIVER_NAME='Vikram Patel'; `$env:DRIVER_PORT='9004'; python -m uvicorn driver_instance.main:app --host 0.0.0.0 --port 9004"
Start-Sleep -Seconds 1

Write-Host "Starting Driver: Sunita Reddy (Port 9005)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "`$env:DRIVER_ID='5'; `$env:DRIVER_NAME='Sunita Reddy'; `$env:DRIVER_PORT='9005'; python -m uvicorn driver_instance.main:app --host 0.0.0.0 --port 9005"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "All Services Started!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "User Interface:     http://localhost:8000" -ForegroundColor White
Write-Host "Backend API:        http://localhost:8001" -ForegroundColor White
Write-Host ""
Write-Host "Driver Dashboards:" -ForegroundColor Yellow
Write-Host "  Rajesh Kumar:     http://localhost:9001" -ForegroundColor White
Write-Host "  Amit Singh:       http://localhost:9002" -ForegroundColor White
Write-Host "  Priya Sharma:     http://localhost:9003" -ForegroundColor White
Write-Host "  Vikram Patel:     http://localhost:9004" -ForegroundColor White
Write-Host "  Sunita Reddy:     http://localhost:9005" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
