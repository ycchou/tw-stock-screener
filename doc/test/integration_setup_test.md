---
description: 架構整合測試案例 (Port 8000)
---

狀態：初始為 [ ]、完成為 [x]
注意：狀態只能在測試通過後由流程更新。
測試類型：後端靜態資源掛載驗證、單一端口整合驗證

# 架構整合 (Integration Architecture)

[x] 【單一端口驗證】根路徑訪問測試
範例輸入：GET http://localhost:8000/
期待輸出：HTTP 200 OK，內容包含 HTML 標籤與 `<title>台股均線糾結篩選器</title>`

[x] 【單一端口驗證】index.html 訪問測試
範例輸入：GET http://localhost:8000/index.html
期待輸出：HTTP 200 OK，內容與根路徑回應一致

[x] 【靜態資源驗證】JavaScript 檔案載入測試
範例輸入：GET http://localhost:8000/js/app.js
期待輸出：HTTP 200 OK，Content-Type 為 application/javascript

[x] 【靜態資源驗證】CSS 檔案載入測試
範例輸入：GET http://localhost:8000/css/style.css
期待輸出：HTTP 200 OK，Content-Type 為 text/css

[x] 【Service Worker驗證】Service Worker 載入與 Content-Type 測試
範例輸入：GET http://localhost:8000/sw.js
期待輸出：HTTP 200 OK，Content-Type 為 application/javascript (必須正確以便瀏覽器註冊)

[x] 【API整合驗證】API 文件頁面測試
範例輸入：GET http://localhost:8000/docs
期待輸出：HTTP 200 OK，顯示 Swagger UI
