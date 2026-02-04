# 台股均線糾結篩選器 PWA

篩選台股中均線糾結的股票，並以 K 線圖展示分析結果。

## 功能特色

- 📊 **均線糾結篩選**：根據用戶設定的參數篩選符合條件的股票
- 📈 **K 線圖展示**：使用 TradingView Lightweight Charts 顯示股票 K 線
- ⚙️ **參數自訂**：可選擇均線（5/10/20/60/120/240）、糾結幅度、糾結天數
- 📱 **PWA 支援**：可安裝到桌面，離線查看已快取的數據

## 技術架構

### 後端 (Python FastAPI)
- FastAPI 提供 REST API
- yfinance 抓取台股歷史數據
- 均線計算與糾結篩選邏輯

### 前端 (PWA)
- 純 HTML/CSS/JavaScript
- TradingView Lightweight Charts
- Service Worker 離線快取

## 快速啟動 (Windows 推薦)

專案根目錄附帶了一個 PowerShell 啟動腳本，可同時開啟前後端並設定好網路連線。

1. 在專案根目錄右鍵點擊 `start_server.ps1`，選擇「使用 PowerShell 執行」。
2. 或者在終端機輸入：
   ```powershell
   .\start_server.ps1
   ```
3. 腳本會自動開啟兩個視窗，並顯示：
   - 電腦端網址：http://localhost:3000
   - 手機端網址：http://192.168.xx.xx:3000 (請確保手機連線到同一 Wi-Fi)

---

## 手動啟動

若您想詳細控制或在其他平台執行，請依序啟動前後端：

### 1. 啟動後端服務

```bash
cd backend

# 啟用虛擬環境 (如果未啟用)
.\venv\Scripts\activate

# 啟動服務 (加上 --host 0.0.0.0 以允許手機連線)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 啟動前端服務

開啟新的終端機視窗：

```bash
cd frontend

# 使用 Python 簡易伺服器
python -m http.server 3000
```

### 3. 開啟瀏覽器

- **電腦**：前往 http://localhost:3000
- **手機**：前往您的電腦 IP (例如 http://192.168.50.79:3000)

## API 文件

啟動後端後，可前往 http://localhost:8000/docs 查看 Swagger API 文件。

## 專案結構

```
tw-stock-screener/
├── backend/
│   ├── main.py              # FastAPI 主程式
│   ├── requirements.txt     # Python 依賴
│   └── services/
│       ├── stock_data.py    # 股票數據抓取
│       ├── ma_calculator.py # 均線計算
│       └── screener.py      # 篩選邏輯
│
├── frontend/
│   ├── index.html           # 主頁面
│   ├── manifest.json        # PWA 設定
│   ├── sw.js                # Service Worker
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── app.js           # 主邏輯
│       ├── chart.js         # K線圖模組
│       └── api.js           # API 呼叫
│
└── README.md
```

## 使用說明

1. 選擇要分析的均線週期（至少選擇兩條）
2. 調整糾結幅度（數值越小，篩選越嚴格）
3. 調整糾結天數（連續幾天維持糾結狀態）
4. 選擇市場（上市/上櫃/全部）
5. 點擊「開始篩選」按鈕
6. 從結果列表點選股票查看 K 線圖
