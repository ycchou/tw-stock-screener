"""
台股均線糾結篩選器 - FastAPI 主程式
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import os

from services.stock_data import StockDataService
from services.ma_calculator import MACalculator
from services.screener import MAConvergenceScreener

app = FastAPI(
    title="台股均線糾結篩選器",
    description="篩選均線糾結的台股，顯示 K 線圖",
    version="1.0.0"
)

# CORS 設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服務
stock_service = StockDataService()
ma_calculator = MACalculator()
screener = MAConvergenceScreener(stock_service, ma_calculator)


# ==================== 請求/回應模型 ====================

class ScreenRequest(BaseModel):
    """篩選請求"""
    ma_periods: List[int] = [5, 10, 20, 60]
    convergence_pct: float = 3.0
    convergence_days: int = 5
    market: Optional[str] = "all"  # all, TW, TWO


class StockInfo(BaseModel):
    """股票資訊"""
    code: str
    name: str
    market: str
    close: Optional[float] = None
    convergence_pct: Optional[float] = None


class KlineData(BaseModel):
    """K 線數據"""
    time: str
    open: float
    high: float
    low: float
    close: float
    volume: Optional[int] = None


class StockKlineResponse(BaseModel):
    """個股 K 線回應"""
    code: str
    name: str
    ohlc: List[KlineData]
    ma_lines: dict


# ==================== API 端點 ====================



@app.get("/api/stocks", response_model=List[StockInfo])
async def get_stocks(market: str = "all", limit: int = 100):
    """
    取得股票列表
    
    - market: all, TW (上市), TWO (上櫃)
    - limit: 回傳筆數限制
    """
    try:
        stocks = stock_service.get_stock_list(market=market, limit=limit)
        return stocks
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/screen", response_model=List[StockInfo])
async def screen_stocks(request: ScreenRequest):
    """
    篩選均線糾結股票
    
    - ma_periods: 要檢查的均線週期, 如 [5, 10, 20, 60]
    - convergence_pct: 糾結幅度百分比, 如 3.0 表示 3%
    - convergence_days: 連續糾結天數
    - market: all, TW, TWO
    """
    try:
        results = await screener.screen(
            ma_periods=request.ma_periods,
            convergence_pct=request.convergence_pct,
            convergence_days=request.convergence_days,
            market=request.market
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stock/{code}/kline")
async def get_stock_kline(
    code: str,
    days: int = 120,
    ma_periods: str = "5,10,20,60"
):
    """
    取得個股 K 線數據與均線
    
    - code: 股票代碼 (如 2330)
    - days: 取幾天的數據
    - ma_periods: 要計算的均線週期，逗號分隔
    """
    try:
        # 解析均線週期
        periods = [int(p.strip()) for p in ma_periods.split(",")]
        
        # 取得 K 線數據
        result = await stock_service.get_stock_kline(code, days, periods)
        
        if not result:
            raise HTTPException(status_code=404, detail=f"找不到股票 {code}")
        
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    """健康檢查"""
    return {"status": "ok"}



# ==================== 靜態檔案服務 (Frontend Integration) ====================

# 取得 frontend 資料夾絕對路徑
# 假設此檔案在 backend/main.py，則 frontend 在 ../frontend
frontend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

if os.path.exists(frontend_dir):
    print(f"Mounting frontend from: {frontend_dir}")
    # Mount 靜態資源目錄
    # 注意: 這裡將根路徑改為 StaticFiles 可能會蓋掉 API，所以我們用特定路徑 + root route
    
    app.mount("/css", StaticFiles(directory=os.path.join(frontend_dir, "css")), name="css")
    app.mount("/js", StaticFiles(directory=os.path.join(frontend_dir, "js")), name="js")
    app.mount("/icons", StaticFiles(directory=os.path.join(frontend_dir, "icons")), name="icons")

    # 根路徑與單頁應用支援
    from fastapi.responses import FileResponse

    @app.get("/", include_in_schema=False)
    async def serve_index():
        return FileResponse(os.path.join(frontend_dir, "index.html"))

    @app.get("/index.html", include_in_schema=False)
    async def serve_index_file():
        return FileResponse(os.path.join(frontend_dir, "index.html"))
        
    @app.get("/manifest.json", include_in_schema=False)
    async def serve_manifest():
        return FileResponse(os.path.join(frontend_dir, "manifest.json"))
        
    @app.get("/sw.js", include_in_schema=False)
    async def serve_sw():
        return FileResponse(os.path.join(frontend_dir, "sw.js"), media_type="application/javascript")


if __name__ == "__main__":
    import uvicorn
    # 整合模式下，我們統一使用 Port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
