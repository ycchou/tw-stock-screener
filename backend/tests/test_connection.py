"""
測試類型：環境與連線診斷
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Ensure backend/ is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

class TestEnvironment:
    """describe: 環境檢測"""
    
    def test_check_dependencies(self):
        """it: 【環境檢測】檢查 Python 環境與依賴套件是否正確安裝"""
        import yfinance
        import fastapi
        import uvicorn
        import pandas
        assert yfinance.__version__ is not None
        assert fastapi.__version__ is not None

    def test_check_yfinance_connection(self):
        """it: 【資料抓取】測試 yfinance 連線與資料獲取能力"""
        import yfinance as yf
        # 測試抓取台積電 (2330.TW)
        ticker = yf.Ticker("2330.TW")
        # 只抓一天，快速測試連線
        df = ticker.history(period="1d")
        assert not df.empty, "yfinance should return data for 2330.TW"
        assert "Close" in df.columns

class TestServer:
    """describe: 後端啟動與 API 連線"""
    
    @pytest.fixture(scope="class")
    def client(self):
        return TestClient(app)

    def test_check_server_startup(self, client):
        """it: 【後端啟動】啟動 FastAPI 伺服器並檢測回應 (Smoke Test)"""
        # 測試 Docs 頁面 (FastAPI 預設)
        response = client.get("/docs")
        assert response.status_code == 200

    def test_check_static_files(self, client):
        """it: 【前端資源】測試靜態檔案服務"""
        # 測試 index.html
        # 注意：如果靜態檔案未掛載或路徑錯誤，這裡會 404
        # 假設 index.html 路徑是正確的
        try:
            response = client.get("/")
            # 如果 main.py 有 redirect "/" to "/index.html" 或者直接 serve
            assert response.status_code in [200, 307], f"Root endpoint returned {response.status_code}"
            
            # 直接請求 static file
            response = client.get("/index.html")
            assert response.status_code == 200
            assert "台股均線糾結篩選器" in response.text
        except Exception as e:
            pytest.fail(f"Static file test failed: {e}")
