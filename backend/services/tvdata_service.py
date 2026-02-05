"""
TradingView / 多週期 K 線資料服務
支援：1d (日K), 1wk (週K), 1mo (月K)

注意：分鐘 K 線需要額外的資料源 (如 TradingView WebSocket)
目前先使用 yfinance 支援日/週/月 K
"""
import yfinance as yf
import pandas as pd
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

# Interval 對應 yfinance 格式
    # "1m": "1m",   # 移除 1m (不穩定)
    # "5m": "5m",   # 移除 5m (不穩定)
    "15m": "15m",
    "30m": "30m",
    "1h": "1h",
    "4h": "4h",
    "1d": "1d",
    "1wk": "1wk",
    "1mo": "1mo",
}

# 台股代碼對應 yfinance 格式
def get_yf_symbol(code: str, market: str = "TW") -> str:
    """轉換為 yfinance 格式"""
    suffix = ".TW" if market == "TW" else ".TWO"
    return f"{code}{suffix}"


class MultiTimeframeService:
    """多週期 K 線服務"""
    
    def __init__(self):
        self.cache: Dict[str, pd.DataFrame] = {}
        self.cache_time: Dict[str, datetime] = {}
        self.cache_duration = timedelta(minutes=5)
    
    def get_supported_intervals(self) -> List[str]:
        """取得支援的週期列表"""
        return list(INTERVAL_MAP.keys())
    
    async def get_kline_data(
        self,
        code: str,
        market: str = "TW",
        interval: str = "1d",
        n_bars: int = 200
    ) -> Optional[pd.DataFrame]:
        """
        取得 K 線資料
        
        Args:
            code: 股票代碼 (如 2330)
            market: TW (上市) 或 TWO (上櫃)
            interval: 週期 (1m, 5m, 15m, 30m, 1h, 4h, 1d, 1wk, 1mo)
            n_bars: 取幾根 K 棒
        
        Returns:
            DataFrame with OHLCV data
        """
        cache_key = f"{code}_{market}_{interval}_{n_bars}"
        
        # 檢查快取
        if cache_key in self.cache:
            cache_time = self.cache_time.get(cache_key)
            if cache_time and datetime.now() - cache_time < self.cache_duration:
                logger.info(f"Cache hit for {cache_key}")
                return self.cache[cache_key]
        
        try:
            symbol = get_yf_symbol(code, market)
            yf_interval = INTERVAL_MAP.get(interval, "1d")
            
            logger.info(f"Fetching {symbol} with interval {yf_interval}")
            
            ticker = yf.Ticker(symbol)
            
            # 根據 interval 決定 period (使用 yfinance 最大支援天數)
            if interval in ["15m", "30m"]:
                period = "59d"  # yfinance limit ~60d
            elif interval in ["1h", "4h"]:
                period = "720d" # yfinance limit 730d
            elif interval == "1d":
                period = f"{n_bars + 60}d" # 取多一點確保 MA
            elif interval == "1wk":
                period = f"{n_bars * 7}d"
            elif interval == "1mo":
                period = f"{n_bars * 31}d"
            else:
                period = "1y"
            
            # yfinance 對於某些 interval 有特殊處理
            if interval == "4h":
                # yfinance 不直接支援 4h，需要用 1h 然後 resample
                df = ticker.history(period=period, interval="1h")
                if not df.empty:
                    df = self._resample_to_4h(df)
            else:
                df = ticker.history(period=period, interval=yf_interval)
            
            if df is None or df.empty:
                logger.warning(f"No data returned for {symbol} with interval {interval}")
                # 對於不支援的分鐘 K，返回 None 並讓前端顯示提示
                return None
            
            # 只取最後 n_bars 筆
            df = df.tail(n_bars)
            
            # 快取
            self.cache[cache_key] = df
            self.cache_time[cache_key] = datetime.now()
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {code}: {e}")
            return None
    
    def _resample_to_4h(self, df: pd.DataFrame) -> pd.DataFrame:
        """將 1h K 線合併為 4h"""
        try:
            resampled = df.resample('4h').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }).dropna()
            return resampled
        except Exception as e:
            logger.error(f"Resample error: {e}")
            return df


# 單例模式
_service = None

def get_tv_service() -> MultiTimeframeService:
    """取得 MultiTimeframeService 單例"""
    global _service
    if _service is None:
        _service = MultiTimeframeService()
    return _service
