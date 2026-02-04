# 台股均線糾結篩選器 - 後端 API 測試案例

狀態：初始為 [ ]、完成為 [x]
注意：狀態只能在測試通過後由流程更新。

---

## 健康檢查 API

[x] 【API 回應】呼叫 `/api/health` 應回傳 `{"status": "ok"}`
範例輸入：GET http://localhost:8000/api/health
期待輸出：{ "status": "ok" }

---

## 股票列表 API

[x] 【API 回應】呼叫 `/api/stocks` 應回傳股票列表陣列
範例輸入：GET http://localhost:8000/api/stocks?limit=3
期待輸出：包含 code、name、market 欄位的陣列

[x] 【參數篩選】使用 `market=TW` 應只回傳上市股票
範例輸入：GET http://localhost:8000/api/stocks?market=TW&limit=3
期待輸出：所有股票的 market 欄位值為 "TW"

[x] 【參數篩選】使用 `market=TWO` 應只回傳上櫃股票
範例輸入：GET http://localhost:8000/api/stocks?market=TWO&limit=3
期待輸出：所有股票的 market 欄位值為 "TWO"

[x] 【參數限制】使用 `limit=5` 應回傳最多 5 筆資料
範例輸入：GET http://localhost:8000/api/stocks?limit=5
期待輸出：回傳陣列長度 <= 5

---

## K 線數據 API

[x] 【API 回應】呼叫 `/api/stock/2330/kline` 應回傳 K 線數據
範例輸入：GET http://localhost:8000/api/stock/2330/kline?days=30
期待輸出：包含 code、name、ohlc、ma_lines 欄位

[x] 【資料格式】ohlc 陣列應包含正確的 OHLC 欄位
範例輸入：GET http://localhost:8000/api/stock/2330/kline?days=10
期待輸出：每個 ohlc 物件包含 time、open、high、low、close

[x] 【均線計算】指定 ma_periods 應回傳對應均線
範例輸入：GET http://localhost:8000/api/stock/2330/kline?ma_periods=5,10,20
期待輸出：ma_lines 包含 MA5、MA10、MA20 鍵值

[x] 【日期格式】time 欄位格式應為 YYYY-MM-DD
範例輸入：GET http://localhost:8000/api/stock/2330/kline
期待輸出：time 格式符合 /^\d{4}-\d{2}-\d{2}$/

---

## 篩選 API

[x] 【API 回應】POST `/api/screen` 應回傳符合條件的股票列表
範例輸入：POST http://localhost:8000/api/screen
         Body: {"ma_periods": [5,10,20], "convergence_pct": 5.0, "convergence_days": 3}
期待輸出：包含 code、name、market、close、convergence_pct 的陣列

[x] 【排序規則】回傳結果應按 convergence_pct 排序（小到大）
範例輸入：POST http://localhost:8000/api/screen
期待輸出：陣列按 convergence_pct 升序排列
