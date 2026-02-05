# 台股均線糾結篩選器 PWA

篩選台股中均線糾結的股票，並以 K 線圖展示分析結果。本專案採用 **前後端整合架構**，單一服務即可同時提供 API 與網頁介面。

## 功能特色

- 📊 **均線糾結篩選**：根據用戶設定的參數篩選符合條件的股票
- 📈 **K 線圖展示**：使用 TradingView Lightweight Charts 顯示股票 K 線
- ⚙️ **參數自訂**：可選擇均線（5/10/20/60/120/240）、糾結幅度、糾結天數
- 📱 **PWA 支援**：可安裝到桌面/手機主畫面，體驗如原生 App
- 🚀 **單一端口部署**：整合前後端於 Port 8000，簡化網路設定與部署流程

## 技術架構

### 後端 (Python FastAPI)
- **FastAPI**: 提供 REST API 與 靜態檔案服務 (Static Server)
- **yfinance**: 抓取台股歷史數據
- **Pandas**: 均線計算與數據分析

### 前端 (Vanilla JS PWA)
- **HTML/CSS/JS**: 純原生實作，無須編譯 (No Build Step)
- **Service Worker**: 離線快取與 PWA 功能
- **Lightweight Charts**: 互動式 K 線圖

---

## 快速啟動 (Windows)

### 👍 方法一：一鍵啟動 (推薦)

專案根目錄附帶了一個 PowerShell 啟動腳本，可自動設定環境並啟動服務。

1. 在專案根目錄右鍵點擊 `start_server.ps1`，選擇「使用 PowerShell 執行」。
2. 或者在終端機輸入：
   ```powershell
   .\start_server.ps1
   ```
3. 腳本會開啟一個視窗，並顯示：
   - 電腦端網址：http://localhost:8000
   - 手機端網址：http://192.168.xx.xx:8000 (需連至同一 Wi-Fi)

### 🔧 方法二：手動啟動

若您想在其他平台 (如 Linux/Mac) 執行，只需啟動 Python 後端即可：

```bash
cd backend

# 1. 建立虛擬環境 (初次執行)
python -m venv venv

# 2. 啟用虛擬環境
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
# source venv/bin/activate

# 3. 安裝依賴
pip install -r requirements.txt

# 4. 啟動服務 (同時包含前端與 API)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

啟動後，直接瀏覽器訪問 `http://localhost:8000` 即可。

---

## 雲端部署 (Docker / GCP)

本專案已包含 `Dockerfile`，支援容器化部署。

### Google Cloud Run (推薦，Serverless)

1. **安裝 gcloud CLI** 並登入。
2. **部署指令**：
   ```bash
   gcloud run deploy tw-stock-screener --source . --region asia-east1 --allow-unauthenticated
   ```
3. 部署完成後，GCP 會提供一個 HTTPS 網址，即可直接使用。

### Docker 自行構建

```bash
# 建立映像檔
docker build -t stock-screener .

# 執行容器
docker run -p 8080:8080 stock-screener
```
訪問 `http://localhost:8080`。

---

## 專案結構

```
tw-stock-screener/
├── backend/
│   ├── main.py              # FastAPI 主程式 (整合靜態檔案服務)
│   ├── requirements.txt     # Python 依賴
│   └── services/            # 核心邏輯
│
├── frontend/
│   ├── index.html           # 主頁面
│   ├── sw.js                # Service Worker
│   ├── js/                  # 前端邏輯 (api.js, chart.js, app.js)
│   ├── css/                 # 樣式表
│   └── icons/               # 應用圖示
│
├── Dockerfile               # 部署設定檔
├── start_server.ps1         # Windows 啟動腳本
└── README.md
```

## 使用說明

1. 選擇要分析的均線週期（至少選擇兩條）
2. 調整糾結幅度（數值越小，篩選越嚴格）
3. 調整糾結天數（連續幾天維持糾結狀態）
4. 選擇市場（上市/上櫃/全部）
5. 點擊「開始篩選」按鈕
6. 從結果列表點選股票查看 K 線圖
