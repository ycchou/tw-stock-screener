# Startup Script for TW Stock Screener (Integrated Mode)
# This script launches a single backend process that serves both API and Frontend.

# Get Local IP
$ipv4 = Get-NetIPAddress | Where-Object {$_.AddressFamily -eq "IPv4" -and $_.InterfaceAlias -notlike "*Loopback*"} | Select-Object -ExpandProperty IPAddress -First 1

$root = Get-Location

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "TW Stock Screener - Integrated Server" -ForegroundColor White
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "URL:          http://localhost:8000" -ForegroundColor Green
Write-Host "Mobile URL:   http://$($ipv4):8000" -ForegroundColor Yellow
Write-Host "========================================================" -ForegroundColor Cyan

# Start Backend (which now serves frontend files too)
Write-Host "Starting Integrated Service (Port 8000)..." -ForegroundColor Magenta
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "Set-Location '$root\backend'; .\venv\Scripts\activate; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

Write-Host "Service started in a new window."
