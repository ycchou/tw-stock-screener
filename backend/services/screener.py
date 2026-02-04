"""
均線糾結篩選器
"""
import asyncio
from typing import List, Dict
import logging

from .stock_data import StockDataService
from .ma_calculator import MACalculator

logger = logging.getLogger(__name__)


class MAConvergenceScreener:
    """均線糾結篩選器"""
    
    def __init__(
        self, 
        stock_service: StockDataService,
        ma_calculator: MACalculator
    ):
        self.stock_service = stock_service
        self.ma_calculator = ma_calculator
    
    async def screen_single(
        self,
        code: str,
        name: str,
        market: str,
        ma_periods: List[int],
        convergence_pct: float,
        convergence_days: int
    ) -> Dict:
        """
        篩選單支股票
        
        Returns:
            符合條件時回傳股票資訊，否則回傳 None
        """
        try:
            # 取得歷史數據
            df = await self.stock_service.get_stock_history(code)
            
            if df is None or df.empty:
                return None
            
            # 檢查糾結條件
            is_converged, current_pct = self.ma_calculator.check_convergence(
                df, ma_periods, convergence_pct, convergence_days
            )
            
            if is_converged:
                # 取得最新收盤價
                close = round(df['Close'].iloc[-1], 2) if len(df) > 0 else None
                
                return {
                    "code": code,
                    "name": name,
                    "market": market,
                    "close": close,
                    "convergence_pct": current_pct
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error screening {code}: {e}")
            return None
    
    async def screen(
        self,
        ma_periods: List[int] = [5, 10, 20, 60],
        convergence_pct: float = 3.0,
        convergence_days: int = 5,
        market: str = "all"
    ) -> List[Dict]:
        """
        批量篩選均線糾結股票
        
        Args:
            ma_periods: 要檢查的均線週期列表
            convergence_pct: 糾結幅度百分比閾值
            convergence_days: 連續糾結天數
            market: all, TW, TWO
        
        Returns:
            符合條件的股票列表
        """
        # 取得股票列表
        stocks = self.stock_service.get_stock_list(market=market, limit=500)
        
        logger.info(f"開始篩選 {len(stocks)} 支股票...")
        logger.info(f"條件: 均線={ma_periods}, 幅度<={convergence_pct}%, 天數={convergence_days}")
        
        # 並行處理（控制併發數量避免過載）
        semaphore = asyncio.Semaphore(10)
        
        async def screen_with_limit(stock):
            async with semaphore:
                return await self.screen_single(
                    code=stock["code"],
                    name=stock["name"],
                    market=stock["market"],
                    ma_periods=ma_periods,
                    convergence_pct=convergence_pct,
                    convergence_days=convergence_days
                )
        
        # 執行並行篩選
        tasks = [screen_with_limit(stock) for stock in stocks]
        results = await asyncio.gather(*tasks)
        
        # 過濾出符合條件的股票
        matched = [r for r in results if r is not None]
        
        # 按糾結幅度排序（幅度小的排前面）
        matched.sort(key=lambda x: x.get("convergence_pct", 100))
        
        logger.info(f"篩選完成，共 {len(matched)} 支股票符合條件")
        
        return matched
