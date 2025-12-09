"""
特征工程模块
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Tuple


class FeatureEngineer:
    """特征工程器"""
    
    # 高价值客户预测的特征列表
    HIGH_VALUE_FEATURES = [
        "total_assets", "monthly_income", "product_count",
        "app_login_count", "financial_repurchase_count",
        "investment_monthly_count"
    ]
    
    # 客户分群的特征列表
    CLUSTERING_FEATURES = [
        "age", "total_assets", "monthly_income",
        "product_count", "app_login_count"
    ]
    
    # 产品标志列
    PRODUCT_FLAGS = [
        "deposit_flag", "financial_flag",
        "fund_flag", "insurance_flag"
    ]
    
    def create_product_flags(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        创建产品持有标志
        
        根据余额字段创建 0/1 标志
        """
        df = df.copy()
        
        # 余额字段到标志字段的映射
        balance_to_flag = {
            "deposit_balance": "deposit_flag",
            "financial_balance": "financial_flag",
            "fund_balance": "fund_flag",
            "insurance_balance": "insurance_flag",
            # 兼容另一种字段命名
            "wealth_management_balance": "financial_flag",
        }
        
        for balance_col, flag_col in balance_to_flag.items():
            if balance_col in df.columns:
                df[flag_col] = (df[balance_col] > 0).astype(int)
        
        return df
    
    def create_product_count(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        计算持有产品数量
        """
        df = df.copy()
        
        # 先确保产品标志存在
        df = self.create_product_flags(df)
        
        # 计算产品数量
        flag_cols = [col for col in self.PRODUCT_FLAGS if col in df.columns]
        if flag_cols:
            df["product_count"] = df[flag_cols].sum(axis=1)
        
        return df
    
    def create_high_value_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        创建高价值客户预测所需的特征
        """
        df = df.copy()
        
        # 1. 总资产
        if "total_aum" in df.columns and "total_assets" not in df.columns:
            df["total_assets"] = df["total_aum"]
        
        # 2. 月收入（从交易金额估算）
        if "monthly_transaction_amount" in df.columns and "monthly_income" not in df.columns:
            df["monthly_income"] = df["monthly_transaction_amount"] * 0.3
        
        # 3. 产品数量
        df = self.create_product_count(df)
        
        # 4. APP 登录次数
        if "mobile_bank_login_count" in df.columns and "app_login_count" not in df.columns:
            df["app_login_count"] = df["mobile_bank_login_count"]
        
        # 5. 理财复购次数
        if "monthly_transaction_count" in df.columns:
            financial_flag = df.get("financial_flag", 0)
            if "financial_repurchase_count" not in df.columns:
                df["financial_repurchase_count"] = df["monthly_transaction_count"] * financial_flag
        
        # 6. 月均投资次数
        if "monthly_transaction_count" in df.columns:
            has_investment = (
                df.get("fund_flag", 0) | df.get("financial_flag", 0)
            ).astype(int)
            if "investment_monthly_count" not in df.columns:
                df["investment_monthly_count"] = df["monthly_transaction_count"] * has_investment
        
        return df
    
    def create_high_value_label(
        self,
        df: pd.DataFrame,
        threshold: float = 1000000,
        simulate: bool = True
    ) -> pd.DataFrame:
        """
        创建高价值客户标签
        
        Args:
            df: 输入数据
            threshold: 高价值阈值（默认100万）
            simulate: 是否模拟未来资产（用于训练）
        
        Returns:
            添加了标签的 DataFrame
        """
        df = df.copy()
        
        asset_col = "total_assets" if "total_assets" in df.columns else "total_aum"
        
        if simulate:
            # 模拟未来资产变化
            np.random.seed(42)
            df["future_total_assets"] = df[asset_col] * np.random.uniform(0.95, 1.2, size=len(df))
            df["label"] = (df["future_total_assets"] >= threshold).astype(int)
        else:
            df["label"] = (df[asset_col] >= threshold).astype(int)
        
        return df
    
    def get_feature_matrix(
        self,
        df: pd.DataFrame,
        feature_list: Optional[List[str]] = None
    ) -> Tuple[pd.DataFrame, List[str]]:
        """
        获取特征矩阵
        
        Args:
            df: 输入数据
            feature_list: 特征列表，默认使用高价值预测特征
        
        Returns:
            (特征矩阵, 实际使用的特征列表)
        """
        features = feature_list or self.HIGH_VALUE_FEATURES
        
        # 只保留存在的特征
        available_features = [f for f in features if f in df.columns]
        
        X = df[available_features].fillna(0)
        
        return X, available_features
    
    def create_clustering_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        创建聚类分析所需的特征
        """
        df = df.copy()
        
        # 创建基础特征
        df = self.create_high_value_features(df)
        
        return df
    
    def create_rfm_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        创建 RFM 特征（Recency, Frequency, Monetary）
        """
        df = df.copy()
        
        # Recency: 最近一次登录/交易的时间间隔
        if "last_app_login_time" in df.columns:
            df["last_app_login_time"] = pd.to_datetime(df["last_app_login_time"], errors="coerce")
            df["recency_days"] = (pd.Timestamp.now() - df["last_app_login_time"]).dt.days
        
        # Frequency: 交易/登录频率
        if "app_login_count" in df.columns:
            df["frequency"] = df["app_login_count"]
        elif "mobile_bank_login_count" in df.columns:
            df["frequency"] = df["mobile_bank_login_count"]
        
        # Monetary: 资产/交易金额
        if "total_assets" in df.columns:
            df["monetary"] = df["total_assets"]
        elif "total_aum" in df.columns:
            df["monetary"] = df["total_aum"]
        
        return df

