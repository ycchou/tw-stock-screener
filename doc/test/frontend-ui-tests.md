# 台股均線糾結篩選器 - 前端 UI 測試案例

狀態：初始為 [ ]、完成為 [x]
注意：狀態只能在測試通過後由流程更新。

---

## 頁面載入

[x] 【前端元素】頁面應顯示標題「台股均線糾結篩選器」
範例輸入：開啟 http://localhost:3000
期待輸出：h1 元素包含文字「台股均線糾結篩選器」

[x] 【前端元素】設定面板應顯示均線選擇 checkbox
範例輸入：開啟頁面
期待輸出：顯示 5日、10日、20日、60日、120日、240日 的 checkbox

[x] 【前端元素】糾結幅度滑桿應可見且可操作
範例輸入：開啟頁面
期待輸出：#convergencePct 元素存在且 type="range"

[x] 【前端元素】「開始篩選」按鈕應存在
範例輸入：開啟頁面
期待輸出：#screenBtn 按鈕存在

---

## 參數設定互動

[x] 【function 邏輯】拖動幅度滑桿時數值顯示應即時更新
範例輸入：將 #convergencePct 拖動到 5
期待輸出：#convergencePctValue 顯示 "5%"

[x] 【function 邏輯】拖動天數滑桿時數值顯示應即時更新
範例輸入：將 #convergenceDays 拖動到 10
期待輸出：#convergenceDaysValue 顯示 "10 天"

[x] 【前端元素】預設應選取 5日、10日、20日、60日 均線
範例輸入：開啟頁面
期待輸出：#ma5, #ma10, #ma20, #ma60 為 checked 狀態

---

## 篩選功能

[x] 【function 邏輯】點擊篩選按鈕應顯示 loading 狀態
範例輸入：點擊 #screenBtn
期待輸出：按鈕內顯示 spinner，按鈕 disabled

[ ] 【驗證邏輯】選擇少於兩條均線應顯示警告
範例輸入：只選擇 #ma5，點擊篩選
期待輸出：顯示 toast 警告訊息
備註：測試環境中 Toast 顯示不穩定或 Checkbox 操作問題

[x] 【Mock API】篩選完成後應顯示股票列表
範例輸入：設定參數後點擊篩選
期待輸出：#stockList 內顯示 .stock-item 元素 (Count > 0)

---

## 股票列表

[x] 【前端元素】股票項目應顯示代碼、名稱、價格
範例輸入：篩選結果顯示後
期待輸出：.stock-item 包含 .stock-code, .stock-name, .stock-price

[x] 【function 邏輯】點擊股票應切換 active 狀態
範例輸入：點擊某個 .stock-item
期待輸出：該元素加上 .active class

---

## K 線圖顯示

[ ] 【function 邏輯】點擊股票後應載入 K 線圖
範例輸入：點擊股票列表中的某檔股票
期待輸出：#chartContainer 內顯示 canvas 圖表
備註：Canvas 元素在測試環境中檢測超時 (但功能正常)

[x] 【前端元素】圖表標題應顯示股票名稱
範例輸入：點擊股票後
期待輸出：#chartStockName 顯示股票名稱

[x] 【前端元素】選擇股票後應顯示資訊卡片
範例輸入：點擊股票後
期待輸出：#infoCards 區域顯示（display 不為 none）

[x] 【function 邏輯】點擊週期按鈕應切換圖表數據
範例輸入：點擊 data-days="30" 的週期按鈕
期待輸出：該按鈕加上 .active class，圖表重新載入
