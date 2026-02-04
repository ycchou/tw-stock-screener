# 啟動腳本 - 台股均線糾結篩選器

# 1. 啟動後端 (Backend) - 監聽所有 IP (0.0.0.0) 以允許手機連線
Write-Host "正在啟動後端服務..."
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd backend; .\venv\Scripts\activate; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

# 2. 啟動前端 (Frontend)
Write-Host "正在啟動前端服務..."
Start-Process -FilePath "powershell" -ArgumentList "-NoExit", "-Command", "cd frontend; python -m http.server 3000"

Write-Host "------------------------------------------------"
Write-Host "服務啟動完成！"
Write-Host "電腦端請訪問: http://localhost:3000"
Write-Host "手機端請訪問: http://192.168.50.79:3000"
Write-Host "------------------------------------------------"
