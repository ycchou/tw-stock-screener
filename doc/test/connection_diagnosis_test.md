狀態：初始為 [ ]、完成為 [x]
注意：狀態只能在測試通過後由流程更新。
測試類型：環境與連線診斷

[x] 【環境檢測】檢查 Python 環境與依賴套件是否正確安裝
範例輸入：執行 `pip list`, `python --version`
期待輸出：列出 requirements.txt 中的套件 (yfinance, fastapi, uvicorn 等) 且無錯誤

[x] 【資料抓取】測試 yfinance 連線與資料獲取能力
範例輸入：執行 Python script 抓取 2330.TW 歷史資料
期待輸出：成功回傳 DataFrame，無連線錯誤或權限錯誤

[x] 【後端啟動】啟動 FastAPI 伺服器並檢測回應 (Smoke Test)
範例輸入：啟動伺服器後，請求 `http://localhost:8000/docs`
期待輸出：HTTP 200 OK，且能看到 OpenAPI 文件

[x] 【前端資源】測試靜態檔案服務
範例輸入：請求 `http://localhost:8000/index.html`
期待輸出：HTTP 200 OK，內容包含 `<title>台股均線糾結篩選器</title>`
