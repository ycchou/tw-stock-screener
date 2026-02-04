"""
台股均線糾結篩選器 - 後端 API 測試

測試案例來源: doc/test/backend-api-tests.md
"""
import pytest
import re


class TestHealthAPI:
    """健康檢查 API"""
    
    @pytest.mark.anyio
    async def test_health_should_return_ok(self, client):
        """【API 回應】呼叫 `/api/health` 應回傳 `{"status": "ok"}`"""
        response = await client.get("/api/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestStocksAPI:
    """股票列表 API"""
    
    @pytest.mark.anyio
    async def test_stocks_should_return_list(self, client):
        """【API 回應】呼叫 `/api/stocks` 應回傳股票列表陣列"""
        response = await client.get("/api/stocks?limit=3")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # 檢查欄位
        for stock in data:
            assert "code" in stock
            assert "name" in stock
            assert "market" in stock
    
    @pytest.mark.anyio
    async def test_stocks_filter_market_tw(self, client):
        """【參數篩選】使用 `market=TW` 應只回傳上市股票"""
        response = await client.get("/api/stocks?market=TW&limit=3")
        assert response.status_code == 200
        data = response.json()
        for stock in data:
            assert stock["market"] == "TW"
    
    @pytest.mark.anyio
    async def test_stocks_filter_market_two(self, client):
        """【參數篩選】使用 `market=TWO` 應只回傳上櫃股票"""
        response = await client.get("/api/stocks?market=TWO&limit=3")
        assert response.status_code == 200
        data = response.json()
        for stock in data:
            assert stock["market"] == "TWO"
    
    @pytest.mark.anyio
    async def test_stocks_limit_parameter(self, client):
        """【參數限制】使用 `limit=5` 應回傳最多 5 筆資料"""
        response = await client.get("/api/stocks?limit=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 5


class TestKlineAPI:
    """K 線數據 API"""
    
    @pytest.mark.anyio
    async def test_kline_should_return_data(self, client):
        """【API 回應】呼叫 `/api/stock/2330/kline` 應回傳 K 線數據"""
        response = await client.get("/api/stock/2330/kline?days=30")
        assert response.status_code == 200
        data = response.json()
        assert "code" in data
        assert "name" in data
        assert "ohlc" in data
        assert "ma_lines" in data
    
    @pytest.mark.anyio
    async def test_kline_ohlc_format(self, client):
        """【資料格式】ohlc 陣列應包含正確的 OHLC 欄位"""
        response = await client.get("/api/stock/2330/kline?days=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["ohlc"]) > 0
        for ohlc in data["ohlc"]:
            assert "time" in ohlc
            assert "open" in ohlc
            assert "high" in ohlc
            assert "low" in ohlc
            assert "close" in ohlc
    
    @pytest.mark.anyio
    async def test_kline_ma_periods(self, client):
        """【均線計算】指定 ma_periods 應回傳對應均線"""
        response = await client.get("/api/stock/2330/kline?ma_periods=5,10,20")
        assert response.status_code == 200
        data = response.json()
        assert "MA5" in data["ma_lines"]
        assert "MA10" in data["ma_lines"]
        assert "MA20" in data["ma_lines"]
    
    @pytest.mark.anyio
    async def test_kline_time_format(self, client):
        """【日期格式】time 欄位格式應為 YYYY-MM-DD"""
        response = await client.get("/api/stock/2330/kline?days=10")
        assert response.status_code == 200
        data = response.json()
        date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
        for ohlc in data["ohlc"]:
            assert date_pattern.match(ohlc["time"])


class TestScreenAPI:
    """篩選 API"""
    
    @pytest.mark.anyio
    async def test_screen_should_return_list(self, client):
        """【API 回應】POST `/api/screen` 應回傳符合條件的股票列表"""
        response = await client.post("/api/screen", json={
            "ma_periods": [5, 10, 20],
            "convergence_pct": 5.0,
            "convergence_days": 3
        })
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # 檢查欄位 (如果有結果)
        if len(data) > 0:
            for stock in data:
                assert "code" in stock
                assert "name" in stock
                assert "market" in stock
                assert "convergence_pct" in stock
    
    @pytest.mark.anyio
    async def test_screen_sorted_by_convergence(self, client):
        """【排序規則】回傳結果應按 convergence_pct 排序（小到大）"""
        response = await client.post("/api/screen", json={
            "ma_periods": [5, 10, 20],
            "convergence_pct": 10.0,
            "convergence_days": 1
        })
        assert response.status_code == 200
        data = response.json()
        if len(data) > 1:
            for i in range(len(data) - 1):
                assert data[i]["convergence_pct"] <= data[i + 1]["convergence_pct"]
