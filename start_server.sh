#!/bin/bash

# 台股篩選器 Linux 啟動腳本

# 取得腳本所在目錄
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$DIR/backend"

echo "========================================================"
echo "TW Stock Screener - Linux Launcher"
echo "========================================================"

# 檢查 Python 是否安裝
if ! command -v python3 &> /dev/null; then
    echo "❌ 錯誤: 未安裝 Python3"
    exit 1
fi

# 進入 backend 目錄
cd "$BACKEND_DIR"

# 檢查 venv 是否存在，不存在則建立
if [ ! -d "venv" ]; then
    echo "🔧 正在建立虛擬環境..."
    python3 -m venv venv
fi

# 啟用虛擬環境
source venv/bin/activate

# 安裝/更新依賴
echo "📦 檢查並安裝依賴套件..."
pip install -q -r requirements.txt

# 啟動服務
echo "🚀 正在啟動服務 (Port 8000)..."
echo "👉 http://localhost:8000"
echo "👉 http://$(hostname -I | awk '{print $1}'):8000 (區網 IP)"
echo "========================================================"

# 執行 uvicorn
exec uvicorn main:app --host 0.0.0.0 --port 8000
