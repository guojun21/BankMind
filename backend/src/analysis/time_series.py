"""
时间序列分析模块
使用 ARIMA 预测资产趋势
"""

import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple
from statsmodels.tsa.arima.model import ARIMA

from ..config import settings


class AssetTrendAnalyzer:
    """资产趋势分析器"""
    
    def __init__(
        self,
        order: Tuple[int, int, int] = (1, 1, 1),
        forecast_periods: int = 4
    ):
        self.order = order
        self.forecast_periods = forecast_periods
        self.model = None
        self.model_fit = None
        self.series: Optional[pd.Series] = None
        self.forecast: Optional[pd.Series] = None
    
    def prepare_data(
        self,
        df: pd.DataFrame,
        date_col: str = "account_open_date",
        value_col: str = "total_aum",
        min_periods: int = 12
    ) -> pd.Series:
        """
        准备时间序列数据
        
        Args:
            df: 原始数据
            date_col: 日期列名
            value_col: 值列名
            min_periods: 最小时间周期数
        
        Returns:
            时间序列 Series
        """
        df = df.copy()
        
        # 转换日期
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        
        # 按月汇总
        monthly_data = df.groupby(
            df[date_col].dt.to_period("M")
        )[value_col].mean().reset_index()
        
        monthly_data[date_col] = monthly_data[date_col].dt.to_timestamp()
        monthly_data = monthly_data.sort_values(date_col)
        
        # 如果数据不足，生成模拟数据补充
        if len(monthly_data) < min_periods:
            series = self._generate_simulated_series(
                monthly_data, value_col, min_periods
            )
        else:
            monthly_data = monthly_data.tail(min_periods)
            series = pd.Series(
                monthly_data[value_col].values,
                index=monthly_data[date_col]
            )
        
        self.series = series
        return series
    
    def _generate_simulated_series(
        self,
        monthly_data: pd.DataFrame,
        value_col: str,
        num_periods: int
    ) -> pd.Series:
        """生成模拟时间序列数据"""
        np.random.seed(42)
        
        if len(monthly_data) > 0:
            mean_val = monthly_data[value_col].mean()
            std_val = monthly_data[value_col].std() if len(monthly_data) > 1 else mean_val * 0.1
        else:
            mean_val = 100000
            std_val = 20000
        
        # 生成最近 N 个月的时间序列
        dates = pd.date_range(end=datetime.now(), periods=num_periods, freq="M")
        values = np.cumsum(np.random.normal(mean_val * 0.02, std_val * 0.1, size=num_periods)) + mean_val
        
        return pd.Series(values, index=dates)
    
    def fit(self, series: pd.Series = None) -> "AssetTrendAnalyzer":
        """
        拟合 ARIMA 模型
        
        Args:
            series: 时间序列，默认使用 prepare_data 生成的
        
        Returns:
            self
        """
        if series is not None:
            self.series = series
        
        if self.series is None:
            raise ValueError("请先调用 prepare_data() 或传入 series")
        
        self.model = ARIMA(self.series, order=self.order)
        self.model_fit = self.model.fit()
        
        return self
    
    def predict(self, periods: int = None) -> pd.Series:
        """
        预测未来趋势
        
        Args:
            periods: 预测周期数
        
        Returns:
            预测结果 Series
        """
        if self.model_fit is None:
            raise ValueError("请先调用 fit()")
        
        periods = periods or self.forecast_periods
        
        self.forecast = self.model_fit.forecast(steps=periods)
        
        # 设置预测时间索引
        last_date = self.series.index[-1]
        self.forecast.index = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=periods,
            freq="M"
        )
        
        return self.forecast
    
    def analyze(
        self,
        df: pd.DataFrame,
        date_col: str = "account_open_date",
        value_col: str = "total_aum"
    ) -> Dict:
        """
        执行完整的时间序列分析
        
        Args:
            df: 原始数据
            date_col: 日期列名
            value_col: 值列名
        
        Returns:
            分析结果字典
        """
        # 准备数据
        series = self.prepare_data(df, date_col, value_col)
        
        # 拟合模型
        self.fit(series)
        
        # 预测
        forecast = self.predict()
        
        # 计算趋势指标
        trend_analysis = self._analyze_trend()
        
        return {
            "history": series,
            "forecast": forecast,
            "trend": trend_analysis,
            "model_summary": str(self.model_fit.summary()) if self.model_fit else None
        }
    
    def _analyze_trend(self) -> Dict:
        """分析趋势特征"""
        if self.series is None or self.forecast is None:
            return {}
        
        # 历史趋势
        history_change = (self.series.iloc[-1] - self.series.iloc[0]) / self.series.iloc[0] * 100
        
        # 预测趋势
        forecast_change = (self.forecast.iloc[-1] - self.series.iloc[-1]) / self.series.iloc[-1] * 100
        
        # 趋势方向
        if forecast_change > 5:
            trend_direction = "上升"
        elif forecast_change < -5:
            trend_direction = "下降"
        else:
            trend_direction = "平稳"
        
        return {
            "history_change_pct": round(history_change, 2),
            "forecast_change_pct": round(forecast_change, 2),
            "trend_direction": trend_direction,
            "current_value": round(self.series.iloc[-1], 2),
            "forecast_end_value": round(self.forecast.iloc[-1], 2),
        }
    
    def get_combined_series(self) -> pd.Series:
        """获取历史+预测的完整序列"""
        if self.series is None or self.forecast is None:
            raise ValueError("请先调用 analyze()")
        
        return pd.concat([self.series, self.forecast])
    
    def save_results(
        self,
        output_dir: str = None,
        prefix: str = ""
    ) -> str:
        """
        保存分析结果
        
        Args:
            output_dir: 输出目录
            prefix: 文件名前缀
        
        Returns:
            结果文件路径
        """
        output_dir = Path(output_dir) if output_dir else settings.OUTPUT_DIR / "reports"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = output_dir / f"{prefix}asset_trend_forecast.csv"
        
        combined = self.get_combined_series()
        result_df = pd.DataFrame({
            "date": combined.index,
            "value": combined.values,
            "type": ["历史"] * len(self.series) + ["预测"] * len(self.forecast)
        })
        
        result_df.to_csv(filepath, index=False, encoding="utf-8-sig")
        
        return str(filepath)

