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

## 快速開始

### 1. 啟動後端服務

```bash
cd backend

# 建立虛擬環境
python -m venv venv

# 啟用虛擬環境 (Windows)
.\venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 啟動服務
uvicorn main:app --reload --port 8000
```

### 2. 啟動前端服務

```bash
cd frontend

# 使用 npx serve 啟動
npx serve .

# 或使用 Python 簡易伺服器
python -m http.server 3000
```

### 3. 開啟瀏覽器

前往 http://localhost:3000 (或 serve 顯示的網址)

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
