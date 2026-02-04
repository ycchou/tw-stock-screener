"""
股票數據服務 - 使用 yfinance 抓取台股資料
"""
import yfinance as yf
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


# 常用台股列表（精選約 200 支流動性較高的股票）
# 完整列表可從證交所網站抓取，這裡先用精選列表
POPULAR_STOCKS = {
    # 上市 (TW)
    "TW": [
        ("2330", "台積電"), ("2317", "鴻海"), ("2454", "聯發科"),
        ("2308", "台達電"), ("2881", "富邦金"), ("2882", "國泰金"),
        ("2891", "中信金"), ("2886", "兆豐金"), ("2884", "玉山金"),
        ("2885", "元大金"), ("2303", "聯電"), ("2412", "中華電"),
        ("3711", "日月光投控"), ("2002", "中鋼"), ("1301", "台塑"),
        ("1303", "南亞"), ("1326", "台化"), ("2207", "和泰車"),
        ("2912", "統一超"), ("2382", "廣達"), ("2357", "華碩"),
        ("2395", "研華"), ("3008", "大立光"), ("2379", "瑞昱"),
        ("2327", "國巨"), ("3034", "聯詠"), ("2345", "智邦"),
        ("6415", "矽力-KY"), ("3037", "欣興"), ("2492", "華新科"),
        ("2603", "長榮"), ("2609", "陽明"), ("2615", "萬海"),
        ("2618", "長榮航"), ("2610", "華航"), ("9921", "巨大"),
        ("2105", "正新"), ("1102", "亞泥"), ("1101", "台泥"),
        ("2408", "南亞科"), ("3231", "緯創"), ("2356", "英業達"),
        ("2301", "光寶科"), ("2353", "宏碁"), ("2324", "仁寶"),
        ("4904", "遠傳"), ("3045", "台灣大"), ("2880", "華南金"),
        ("2890", "永豐金"), ("2883", "開發金"), ("2887", "台新金"),
        ("2892", "第一金"), ("5880", "合庫金"), ("5871", "中租-KY"),
        ("2801", "彰銀"), ("2834", "臺企銀"), ("2823", "中壽"),
        ("2347", "聯強"), ("2474", "可成"), ("3481", "群創"),
        ("2409", "友達"), ("2377", "微星"), ("2392", "正崴"),
        ("2344", "華邦電"), ("6669", "緯穎"), ("3443", "創意"),
        ("2049", "上銀"), ("1476", "儒鴻"), ("9904", "寶成"),
        ("2201", "裕隆"), ("2227", "裕日車"), ("9910", "豐泰"),
        ("1216", "統一"), ("1210", "大成"), ("2915", "潤泰全"),
        ("9914", "美利達"), ("8046", "南電"), ("6239", "力成"),
        ("3706", "神達"), ("2360", "致茂"), ("2404", "漢唐"),
        ("6505", "台塑化"), ("6176", "瑞儀"), ("2059", "川湖"),
        ("2354", "鴻準"), ("3653", "健策"), ("2376", "技嘉"),
        ("2385", "群光"), ("5269", "祥碩"), ("3044", "健鼎"),
        ("6278", "台表科"), ("2458", "義隆"), ("3533", "嘉澤"),
    ],
    # 上櫃 (TWO)
    "TWO": [
        ("6488", "環球晶"), ("5274", "信驊"), ("3105", "穩懋"),
        ("6409", "旭隼"), ("8454", "富邦媒"), ("6533", "晶心科"),
        ("3587", "閎康"), ("6510", "精測"), ("6770", "力積電"),
        ("5289", "宜鼎"), ("6472", "保瑞"), ("4966", "譜瑞-KY"),
        ("6547", "高端疫苗"), ("6223", "旺矽"), ("5388", "中磊"),
        ("3163", "波若威"), ("6411", "晶焜"), ("8016", "矽創"),
        ("6414", "樺漢"), ("3552", "同致"), ("4919", "新唐"),
        ("6285", "啟碁"), ("3227", "原相"), ("6452", "康友-KY"),
        ("4943", "康控-KY"), ("5309", "系統電"), ("8210", "勤誠"),
        ("6477", "安集"), ("3530", "晶相光"), ("4977", "眾達-KY"),
    ]
}


class StockDataService:
    """股票數據服務"""
    
    def __init__(self):
        self.cache = {}
        self.cache_time = {}
        self.cache_duration = timedelta(minutes=30)
    
    def get_stock_list(
        self, 
        market: str = "all", 
        limit: int = 100
    ) -> List[Dict]:
        """
        取得股票列表
        
        Args:
            market: all, TW, TWO
            limit: 回傳筆數限制
        
        Returns:
            股票列表
        """
        stocks = []
        
        if market in ("all", "TW"):
            for code, name in POPULAR_STOCKS["TW"]:
                stocks.append({
                    "code": code,
                    "name": name,
                    "market": "TW"
                })
        
        if market in ("all", "TWO"):
            for code, name in POPULAR_STOCKS["TWO"]:
                stocks.append({
                    "code": code,
                    "name": name,
                    "market": "TWO"
                })
        
        return stocks[:limit]
    
    def get_yfinance_symbol(self, code: str, market: str = None) -> str:
        """
        轉換為 yfinance 格式的股票代碼
        
        Args:
            code: 股票代碼
            market: TW 或 TWO
        
        Returns:
            yfinance 格式代碼
        """
        if market:
            suffix = ".TW" if market == "TW" else ".TWO"
            return f"{code}{suffix}"
        
        # 自動判斷市場
        for c, _ in POPULAR_STOCKS["TW"]:
            if c == code:
                return f"{code}.TW"
        
        for c, _ in POPULAR_STOCKS["TWO"]:
            if c == code:
                return f"{code}.TWO"
        
        # 預設上市
        return f"{code}.TW"
    
    def get_stock_name(self, code: str) -> str:
        """取得股票名稱"""
        for c, name in POPULAR_STOCKS["TW"]:
            if c == code:
                return name
        for c, name in POPULAR_STOCKS["TWO"]:
            if c == code:
                return name
        return code
    
    def get_stock_market(self, code: str) -> str:
        """取得股票市場"""
        for c, _ in POPULAR_STOCKS["TW"]:
            if c == code:
                return "TW"
        for c, _ in POPULAR_STOCKS["TWO"]:
            if c == code:
                return "TWO"
        return "TW"
    
    async def get_stock_history(
        self, 
        code: str, 
        days: int = 250
    ) -> Optional[pd.DataFrame]:
        """
        取得股票歷史數據
        
        Args:
            code: 股票代碼
            days: 取幾天的數據
        
        Returns:
            DataFrame with OHLCV data
        """
        cache_key = f"{code}_{days}"
        
        # 檢查快取
        if cache_key in self.cache:
            cache_time = self.cache_time.get(cache_key)
            if cache_time and datetime.now() - cache_time < self.cache_duration:
                return self.cache[cache_key]
        
        try:
            symbol = self.get_yfinance_symbol(code)
            
            # 多抓一些天數來確保有足夠的數據計算長週期均線
            fetch_days = days + 300
            
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=f"{fetch_days}d")
            
            if df.empty:
                logger.warning(f"No data for {symbol}")
                return None
            
            # 快取
            self.cache[cache_key] = df
            self.cache_time[cache_key] = datetime.now()
            
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {code}: {e}")
            return None
    
    async def get_stock_kline(
        self, 
        code: str, 
        days: int = 120,
        ma_periods: List[int] = None
    ) -> Optional[Dict]:
        """
        取得個股 K 線數據與均線
        
        Args:
            code: 股票代碼
            days: 取幾天的數據
            ma_periods: 要計算的均線週期
        
        Returns:
            K 線數據與均線
        """
        df = await self.get_stock_history(code, days)
        
        if df is None or df.empty:
            return None
        
        # 計算均線
        ma_lines = {}
        if ma_periods:
            for period in ma_periods:
                ma_col = f"MA{period}"
                df[ma_col] = df['Close'].rolling(window=period).mean()
                
                # 只取最近 days 天的均線數據
                ma_data = df[[ma_col]].tail(days).dropna()
                ma_lines[ma_col] = [
                    {
                        "time": idx.strftime("%Y-%m-%d"),
                        "value": round(row[ma_col], 2) if pd.notna(row[ma_col]) else None
                    }
                    for idx, row in ma_data.iterrows()
                    if pd.notna(row[ma_col])
                ]
        
        # 只取最近 days 天
        df = df.tail(days)
        
        # 轉換為 K 線格式
        ohlc = []
        for idx, row in df.iterrows():
            ohlc.append({
                "time": idx.strftime("%Y-%m-%d"),
                "open": round(row['Open'], 2),
                "high": round(row['High'], 2),
                "low": round(row['Low'], 2),
                "close": round(row['Close'], 2),
                "volume": int(row['Volume']) if pd.notna(row['Volume']) else 0
            })
        
        return {
            "code": code,
            "name": self.get_stock_name(code),
            "ohlc": ohlc,
            "ma_lines": ma_lines
        }
