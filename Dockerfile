# 使用 Python 3.11 輕量版作為基底
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴 (如果需要的話，目前看似不需要額外 apt-get)

# 1. 複製需求檔案並安裝 Python 套件
# 先複製 requirements.txt 比較能利用 Docker 快取層
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2. 複製專案程式碼
# 我們將整個 backend 和 frontend 目錄複製進去，保持相對路徑結構
COPY backend/ ./backend/
COPY frontend/ ./frontend/

# 3. 切換到 backend 目錄準備執行
WORKDIR /app/backend

# Cloud Run 預設會提供 PORT 環境變數 (通常是 8080)
ENV PORT=8080

# 4. 啟動指令
# 使用 Shell 模式執行，以便讀取 $PORT 變數
CMD exec uvicorn main:app --host 0.0.0.0 --port $PORT
