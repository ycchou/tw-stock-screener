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
from services.tvdata_service import get_tv_service

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
    interval: str = "1d"  # K線週期: 1m, 5m, 15m, 30m, 1h, 4h, 1d, 1wk, 1mo


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
            market=request.market,
            interval=request.interval
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stock/{code}/kline")
async def get_stock_kline(
    code: str,
    days: int = 120,
    ma_periods: str = "5,10,20,60",
    interval: str = "1d"
):
    """
    取得個股 K 線數據與均線
    
    - code: 股票代碼 (如 2330)
    - days: 取幾天的數據 (用於日K以上週期)
    - ma_periods: 要計算的均線週期，逗號分隔
    - interval: K 線週期 (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1wk, 1mo)
    """
    try:
        # 解析均線週期
        periods = [int(p.strip()) for p in ma_periods.split(",")]
        
        # 根據 interval 決定資料來源
        if interval == "1d":
            # 日K 使用原本的 yfinance (較穩定)
            result = await stock_service.get_stock_kline(code, days, periods)
        else:
            # 其他週期使用 TradingView
            tv_service = get_tv_service()
            market = stock_service.get_stock_market(code)
            
            # 計算需要的 K 棒數量
            n_bars = days if interval in ["1d", "1wk", "1mo"] else days * 8  # 分鐘K需要更多bars
            
            df = await tv_service.get_kline_data(code, market, interval, n_bars)
            
            if df is None or df.empty:
                raise HTTPException(status_code=404, detail=f"找不到股票 {code} 的 {interval} 資料")
            
            # 計算均線
            ma_lines = {}
            for period in periods:
                if len(df) >= period:
                    ma_lines[f"ma{period}"] = df["Close"].rolling(window=period).mean().dropna().tolist()
            
            # 格式化 OHLC
            ohlc = []
            for idx, row in df.iterrows():
                ohlc.append({
                    "time": idx.strftime("%Y-%m-%d %H:%M") if interval not in ["1d", "1wk", "1mo"] else idx.strftime("%Y-%m-%d"),
                    "open": float(row["Open"]),
                    "high": float(row["High"]),
                    "low": float(row["Low"]),
                    "close": float(row["Close"]),
                    "volume": int(row["Volume"]) if "Volume" in row else 0
                })
            
            result = {
                "code": code,
                "name": stock_service.get_stock_name(code),
                "ohlc": ohlc,
                "ma_lines": ma_lines,
                "interval": interval
            }
        
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
