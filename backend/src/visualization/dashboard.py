"""
Dashboard 数据生成器
为 Web 可视化大屏提供数据接口
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any

from ..data import DataLoader


class DashboardGenerator:
    """Dashboard 数据生成器"""
    
    def __init__(self, data_loader: DataLoader = None):
        self.loader = data_loader or DataLoader()
        self._df: Optional[pd.DataFrame] = None
    
    @property
    def df(self) -> pd.DataFrame:
        """懒加载数据"""
        if self._df is None:
            self._df = self.loader.load_merged_data()
        return self._df
    
    def reload_data(self) -> None:
        """重新加载数据"""
        self._df = None
    
    def get_key_indicators(self) -> Dict[str, Any]:
        """
        获取核心指标卡片数据
        
        Returns:
            核心指标字典
        """
        df = self.df
        
        # 总客户数
        total_customers = df["customer_id"].nunique()
        
        # 总资产
        asset_col = "total_assets" if "total_assets" in df.columns else "total_aum"
        total_assets = df[asset_col].sum() if asset_col in df.columns else 0
        avg_assets = df[asset_col].mean() if asset_col in df.columns else 0
        
        # 活跃客户数
        active_count = None
        if "last_app_login_time" in df.columns:
            active_count = df["last_app_login_time"].notnull().sum()
        elif "last_mobile_login" in df.columns:
            active_count = df["last_mobile_login"].notnull().sum()
        
        # 产品复购率
        repurchase_rate = None
        tx_col = "financial_repurchase_count" if "financial_repurchase_count" in df.columns else "monthly_transaction_count"
        if tx_col in df.columns:
            avg_count = df[tx_col].mean()
            repurchase_rate = (df[tx_col] > avg_count).mean()
        
        return {
            "total_customers": int(total_customers),
            "total_assets": float(total_assets),
            "avg_assets": float(avg_assets),
            "active_customers": int(active_count) if active_count else None,
            "repurchase_rate": float(repurchase_rate) if repurchase_rate else None,
        }
    
    def get_customer_lifecycle(self) -> Dict[str, int]:
        """
        获取客户生命周期分布
        
        Returns:
            各生命周期阶段的客户数
        """
        df = self.df
        
        if "lifecycle_stage" in df.columns:
            return df["lifecycle_stage"].value_counts().to_dict()
        
        if "customer_tier" in df.columns:
            return df["customer_tier"].value_counts().to_dict()
        
        # 从年龄推断
        if "age" in df.columns:
            df = df.copy()
            df["lifecycle"] = pd.cut(
                df["age"],
                bins=[0, 30, 45, 60, 100],
                labels=["青年", "中年", "中老年", "老年"]
            )
            return df["lifecycle"].value_counts().to_dict()
        
        return {}
    
    def get_asset_level_distribution(self) -> Dict[str, int]:
        """
        获取资产等级分布
        
        Returns:
            各资产等级的客户数
        """
        df = self.df
        
        if "asset_level" in df.columns:
            return df["asset_level"].value_counts().to_dict()
        
        asset_col = "total_assets" if "total_assets" in df.columns else "total_aum"
        if asset_col in df.columns:
            df = df.copy()
            df["asset_level"] = pd.cut(
                df[asset_col],
                bins=[0, 100000, 500000, 1000000, float("inf")],
                labels=["低资产", "中等资产", "高资产", "超高资产"]
            )
            return df["asset_level"].value_counts().to_dict()
        
        return {}
    
    def get_product_holdings(self) -> Dict[str, int]:
        """
        获取产品持有情况
        
        Returns:
            各产品的持有客户数
        """
        df = self.df
        
        # 产品标志列
        product_flags = {
            "deposit_flag": "存款",
            "financial_flag": "理财",
            "fund_flag": "基金",
            "insurance_flag": "保险",
        }
        
        # 余额列（用于推断产品持有）
        balance_cols = {
            "deposit_balance": "存款",
            "financial_balance": "理财",
            "wealth_management_balance": "理财",
            "fund_balance": "基金",
            "insurance_balance": "保险",
        }
        
        result = {}
        
        # 优先使用标志列
        for flag, name in product_flags.items():
            if flag in df.columns:
                result[name] = int((df[flag] == 1).sum())
        
        # 如果没有标志列，从余额推断
        if not result:
            for col, name in balance_cols.items():
                if col in df.columns:
                    result[name] = int((df[col] > 0).sum())
        
        return result
    
    def get_app_activity_trend(self) -> Dict[str, int]:
        """
        获取 APP 活跃度分布
        
        Returns:
            各登录次数区间的客户数
        """
        df = self.df
        
        login_col = "app_login_count" if "app_login_count" in df.columns else "mobile_bank_login_count"
        
        if login_col not in df.columns:
            return {}
        
        df = df.copy()
        df["login_group"] = pd.cut(
            df[login_col],
            bins=[0, 5, 10, 15, 20, float("inf")],
            labels=["0-5次", "6-10次", "11-15次", "16-20次", "20次以上"]
        )
        
        return df["login_group"].value_counts().sort_index().to_dict()
    
    def get_risk_distribution(self) -> Dict[str, int]:
        """
        获取风险等级分布
        
        Returns:
            各风险等级的客户数
        """
        df = self.df
        
        # 使用交易频率作为风险指标
        tx_col = "monthly_transaction_count" if "monthly_transaction_count" in df.columns else None
        
        if tx_col is None:
            return {}
        
        avg_count = df[tx_col].mean()
        std_count = df[tx_col].std()
        
        def risk_level(val):
            if pd.isnull(val) or val == 0:
                return "高风险"
            elif val < avg_count - 0.5 * std_count:
                return "中风险"
            else:
                return "低风险"
        
        df = df.copy()
        df["risk_level"] = df[tx_col].apply(risk_level)
        
        return df["risk_level"].value_counts().to_dict()
    
    def get_age_distribution(self) -> Dict[str, int]:
        """
        获取年龄分布
        
        Returns:
            各年龄段的客户数
        """
        df = self.df
        
        if "age" not in df.columns:
            return {}
        
        df = df.copy()
        df["age_group"] = pd.cut(
            df["age"],
            bins=[0, 25, 35, 45, 55, 65, 100],
            labels=["25岁以下", "25-35岁", "35-45岁", "45-55岁", "55-65岁", "65岁以上"]
        )
        
        return df["age_group"].value_counts().sort_index().to_dict()
    
    def get_occupation_distribution(self) -> Dict[str, int]:
        """
        获取职业分布
        
        Returns:
            各职业的客户数
        """
        df = self.df
        
        occ_col = "occupation_type" if "occupation_type" in df.columns else "occupation"
        
        if occ_col not in df.columns:
            return {}
        
        return df[occ_col].value_counts().head(10).to_dict()
    
    def get_all_dashboard_data(self) -> Dict[str, Any]:
        """
        获取所有 Dashboard 数据
        
        Returns:
            完整的 Dashboard 数据
        """
        return {
            "indicators": self.get_key_indicators(),
            "lifecycle": self.get_customer_lifecycle(),
            "asset_level": self.get_asset_level_distribution(),
            "product_holdings": self.get_product_holdings(),
            "app_activity": self.get_app_activity_trend(),
            "risk": self.get_risk_distribution(),
            "age": self.get_age_distribution(),
            "occupation": self.get_occupation_distribution(),
        }

