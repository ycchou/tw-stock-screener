
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add backend directory to sys.path to import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

describe_integration = "架構整合測試 (Integration Architecture)"

def test_root_access():
    """【單一端口驗證】根路徑訪問測試"""
    response = client.get("/")
    assert response.status_code == 200
    assert "<html" in response.text.lower()
    assert "<title>台股均線糾結篩選器</title>" in response.text

def test_index_html_access():
    """【單一端口驗證】index.html 訪問測試"""
    response = client.get("/index.html")
    assert response.status_code == 200
    assert response.text == client.get("/").text

def test_js_resource_access():
    """【靜態資源驗證】JavaScript 檔案載入測試"""
    # 測試一個實際存在的 JS 檔案，例如 app.js 或 chart.js
    # 我們先假設 js/app.js 存在 (根據專案結構)
    response = client.get("/js/app.js")
    assert response.status_code == 200, f"Status: {response.status_code}, Body: {response.text[:100]}"
    content_type = response.headers["content-type"].lower()
    assert "application/javascript" in content_type or "text/javascript" in content_type

def test_css_resource_access():
    """【靜態資源驗證】CSS 檔案載入測試"""
    response = client.get("/css/style.css")
    assert response.status_code == 200, f"Status: {response.status_code}, Body: {response.text[:100]}"
    assert "text/css" in response.headers["content-type"].lower()

def test_sw_resource_access():
    """【Service Worker驗證】Service Worker 載入與 Content-Type 測試"""
    response = client.get("/sw.js")
    assert response.status_code == 200, f"Status: {response.status_code}, Body: {response.text[:100]}"
    # Service Worker 必須是 javascript 且通常在根目錄 (或被正確 serve)
    assert "application/javascript" in response.headers["content-type"].lower()

def test_api_docs_access():
    """【API整合驗證】API 文件頁面測試"""
    response = client.get("/docs")
    assert response.status_code == 200
    assert "Swagger UI" in response.text
