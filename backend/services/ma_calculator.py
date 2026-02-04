"""
均線計算模組
"""
import pandas as pd
from typing import List, Dict, Optional


class MACalculator:
    """均線計算器"""
    
    @staticmethod
    def calculate_ma(df: pd.DataFrame, periods: List[int]) -> pd.DataFrame:
        """
        計算多條均線
        
        Args:
            df: 股票歷史數據 (需要有 Close 欄位)
            periods: 均線週期列表
        
        Returns:
            包含均線欄位的 DataFrame
        """
        result = df.copy()
        
        for period in periods:
            col_name = f"MA{period}"
            result[col_name] = result['Close'].rolling(window=period).mean()
        
        return result
    
    @staticmethod
    def calculate_convergence(
        df: pd.DataFrame, 
        ma_periods: List[int]
    ) -> pd.DataFrame:
        """
        計算均線糾結程度
        
        Args:
            df: 已計算均線的 DataFrame
            ma_periods: 用於計算糾結的均線週期
        
        Returns:
            包含糾結程度欄位的 DataFrame
        """
        result = df.copy()
        
        # 取得均線欄位
        ma_columns = [f"MA{p}" for p in ma_periods if f"MA{p}" in result.columns]
        
        if len(ma_columns) < 2:
            raise ValueError("需要至少兩條均線才能計算糾結程度")
        
        # 計算每日均線最大值和最小值
        result['MA_max'] = result[ma_columns].max(axis=1)
        result['MA_min'] = result[ma_columns].min(axis=1)
        
        # 計算糾結幅度百分比 (最大值與最小值的差距佔最小值的百分比)
        result['convergence_pct'] = (
            (result['MA_max'] - result['MA_min']) / result['MA_min'] * 100
        )
        
        return result
    
    @staticmethod
    def check_convergence(
        df: pd.DataFrame,
        ma_periods: List[int],
        convergence_pct: float,
        convergence_days: int
    ) -> tuple[bool, float]:
        """
        檢查是否符合均線糾結條件
        
        Args:
            df: 股票歷史數據
            ma_periods: 要檢查的均線週期列表
            convergence_pct: 糾結幅度百分比閾值
            convergence_days: 連續糾結天數
        
        Returns:
            (是否符合條件, 當前糾結幅度百分比)
        """
        if df is None or df.empty:
            return False, 0.0
        
        # 確保有足夠的數據
        max_period = max(ma_periods)
        if len(df) < max_period + convergence_days:
            return False, 0.0
        
        # 計算均線
        for period in ma_periods:
            col_name = f"MA{period}"
            if col_name not in df.columns:
                df[col_name] = df['Close'].rolling(window=period).mean()
        
        # 取得均線欄位
        ma_columns = [f"MA{p}" for p in ma_periods]
        
        # 過濾掉包含 NaN 的行
        valid_df = df.dropna(subset=ma_columns)
        
        if len(valid_df) < convergence_days:
            return False, 0.0
        
        # 計算最近 N 天的糾結幅度
        recent = valid_df.tail(convergence_days)
        
        ma_max = recent[ma_columns].max(axis=1)
        ma_min = recent[ma_columns].min(axis=1)
        range_pct = (ma_max - ma_min) / ma_min * 100
        
        # 取得當前糾結幅度（最近一天）
        current_pct = range_pct.iloc[-1] if len(range_pct) > 0 else 0.0
        
        # 檢查是否所有天數都符合條件
        is_converged = (range_pct <= convergence_pct).all()
        
        return is_converged, round(current_pct, 2)
