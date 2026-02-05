# Startup Script for TW Stock Screener (Separated Mode)

# Get Local IP for Mobile Access
$ipv4 = Get-NetIPAddress | Where-Object {$_.AddressFamily -eq "IPv4" -and $_.InterfaceAlias -notlike "*Loopback*"} | Select-Object -ExpandProperty IPAddress -First 1

$root = Get-Location

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "TW Stock Screener - Startup Script" -ForegroundColor White
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "Computer URL: http://localhost:3000" -ForegroundColor Green
Write-Host "Mobile URL:   http://$($ipv4):3000" -ForegroundColor Yellow
Write-Host "Backend API:  http://$($ipv4):8000" -ForegroundColor Gray
Write-Host "========================================================" -ForegroundColor Cyan

# 1. Start Backend (Port 8000)
Write-Host "Starting Backend Service (Port 8000)..." -ForegroundColor Magenta
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "Set-Location '$root\backend'; .\venv\Scripts\activate; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

# 2. Start Frontend (Port 3000)
Write-Host "Starting Frontend Service (Port 3000)..." -ForegroundColor Magenta
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "Set-Location '$root\frontend'; python -m http.server 3000"

Write-Host "Services are starting..."
