"""
数据预处理模块
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Tuple
from sklearn.preprocessing import StandardScaler, LabelEncoder


class DataPreprocessor:
    """数据预处理器"""
    
    def __init__(self):
        self.scalers = {}
        self.encoders = {}
    
    def fill_missing(
        self,
        df: pd.DataFrame,
        strategy: str = "mean",
        columns: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        填充缺失值
        
        Args:
            df: 输入数据
            strategy: 填充策略 ('mean', 'median', 'mode', 'zero', 'ffill')
            columns: 指定列，默认处理所有列
        
        Returns:
            处理后的 DataFrame
        """
        df = df.copy()
        cols = columns or df.columns.tolist()
        
        for col in cols:
            if col not in df.columns:
                continue
            
            if strategy == "mean" and df[col].dtype in ["int64", "float64"]:
                df[col] = df[col].fillna(df[col].mean())
            elif strategy == "median" and df[col].dtype in ["int64", "float64"]:
                df[col] = df[col].fillna(df[col].median())
            elif strategy == "mode":
                df[col] = df[col].fillna(df[col].mode().iloc[0] if not df[col].mode().empty else 0)
            elif strategy == "zero":
                df[col] = df[col].fillna(0)
            elif strategy == "ffill":
                df[col] = df[col].fillna(method="ffill")
        
        return df
    
    def scale_features(
        self,
        df: pd.DataFrame,
        columns: List[str],
        method: str = "standard",
        fit: bool = True
    ) -> pd.DataFrame:
        """
        特征标准化
        
        Args:
            df: 输入数据
            columns: 需要标准化的列
            method: 标准化方法 ('standard', 'minmax')
            fit: 是否拟合 scaler
        
        Returns:
            标准化后的 DataFrame
        """
        df = df.copy()
        
        for col in columns:
            if col not in df.columns:
                continue
            
            if fit or col not in self.scalers:
                self.scalers[col] = StandardScaler()
                df[col] = self.scalers[col].fit_transform(df[[col]])
            else:
                df[col] = self.scalers[col].transform(df[[col]])
        
        return df
    
    def encode_categorical(
        self,
        df: pd.DataFrame,
        columns: List[str],
        method: str = "label",
        fit: bool = True
    ) -> pd.DataFrame:
        """
        类别特征编码
        
        Args:
            df: 输入数据
            columns: 需要编码的列
            method: 编码方法 ('label', 'onehot')
            fit: 是否拟合 encoder
        
        Returns:
            编码后的 DataFrame
        """
        df = df.copy()
        
        if method == "label":
            for col in columns:
                if col not in df.columns:
                    continue
                
                if fit or col not in self.encoders:
                    self.encoders[col] = LabelEncoder()
                    df[col] = self.encoders[col].fit_transform(df[col].astype(str))
                else:
                    df[col] = self.encoders[col].transform(df[col].astype(str))
        
        elif method == "onehot":
            df = pd.get_dummies(df, columns=columns)
        
        return df
    
    def remove_outliers(
        self,
        df: pd.DataFrame,
        columns: List[str],
        method: str = "iqr",
        threshold: float = 1.5
    ) -> pd.DataFrame:
        """
        移除异常值
        
        Args:
            df: 输入数据
            columns: 检测异常值的列
            method: 检测方法 ('iqr', 'zscore')
            threshold: 阈值
        
        Returns:
            移除异常值后的 DataFrame
        """
        df = df.copy()
        mask = pd.Series(True, index=df.index)
        
        for col in columns:
            if col not in df.columns or df[col].dtype not in ["int64", "float64"]:
                continue
            
            if method == "iqr":
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                mask &= (df[col] >= Q1 - threshold * IQR) & (df[col] <= Q3 + threshold * IQR)
            
            elif method == "zscore":
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                mask &= z_scores <= threshold
        
        return df[mask]
    
    def create_age_groups(
        self,
        df: pd.DataFrame,
        age_col: str = "age",
        bins: List[int] = None,
        labels: List[str] = None
    ) -> pd.DataFrame:
        """
        创建年龄分组
        """
        df = df.copy()
        bins = bins or [0, 30, 45, 60, 100]
        labels = labels or ["30岁以下", "30-45岁", "46-60岁", "60岁以上"]
        
        if age_col in df.columns:
            df["age_group"] = pd.cut(df[age_col], bins=bins, labels=labels)
        
        return df
    
    def create_asset_level(
        self,
        df: pd.DataFrame,
        asset_col: str = "total_assets",
        bins: List[float] = None,
        labels: List[str] = None
    ) -> pd.DataFrame:
        """
        创建资产等级分组
        """
        df = df.copy()
        bins = bins or [0, 100000, 500000, 1000000, float("inf")]
        labels = labels or ["低资产", "中等资产", "高资产", "超高资产"]
        
        if asset_col in df.columns:
            df["asset_level"] = pd.cut(df[asset_col], bins=bins, labels=labels)
        
        return df

