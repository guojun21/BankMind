"""
客户分群模型
使用 K-Means 对客户进行聚类分析
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, calinski_harabasz_score

from .base import BaseModel
from ..config import settings
from ..data import FeatureEngineer


class CustomerClustering(BaseModel):
    """客户分群模型"""
    
    DEFAULT_FEATURES = [
        "age", "total_assets", "monthly_income",
        "product_count", "app_login_count"
    ]
    
    CLUSTER_LABELS = {
        0: "高价值活跃客户",
        1: "中产稳健客户", 
        2: "年轻成长客户",
    }
    
    def __init__(
        self,
        name: str = "customer_clustering",
        n_clusters: int = None,
        features: Optional[List[str]] = None
    ):
        super().__init__(name)
        self.n_clusters = n_clusters or settings.DEFAULT_N_CLUSTERS
        self.features = features or self.DEFAULT_FEATURES
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=2)
        self.feature_engineer = FeatureEngineer()
    
    def prepare_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        准备聚类数据
        
        Args:
            df: 原始数据
        
        Returns:
            处理后的特征矩阵
        """
        # 创建特征
        df = self.feature_engineer.create_clustering_features(df)
        
        # 选择可用特征
        available_features = [f for f in self.features if f in df.columns]
        self.features = available_features
        
        X = df[available_features].fillna(0)
        
        return X
    
    def fit(
        self,
        X: pd.DataFrame,
        y=None,
        **kwargs
    ) -> Dict[str, float]:
        """
        训练聚类模型
        
        Args:
            X: 特征矩阵
        
        Returns:
            评估指标字典
        """
        # 标准化
        X_scaled = self.scaler.fit_transform(X)
        
        # 训练 K-Means
        self.model = KMeans(
            n_clusters=self.n_clusters,
            random_state=42,
            n_init=10
        )
        self.model.fit(X_scaled)
        
        self.is_fitted = True
        
        # 评估
        metrics = self.evaluate(X_scaled)
        self.metadata["metrics"] = metrics
        self.metadata["features"] = self.features
        
        return metrics
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        预测客户所属群组
        
        Args:
            X: 特征矩阵
        
        Returns:
            群组标签数组
        """
        if not self.is_fitted:
            raise ValueError("模型尚未训练，请先调用 fit() 方法")
        
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)
    
    def fit_predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        训练并预测
        """
        self.fit(X)
        return self.predict(X)
    
    def evaluate(self, X_scaled: np.ndarray) -> Dict[str, float]:
        """
        评估聚类效果
        
        Args:
            X_scaled: 标准化后的特征矩阵
        
        Returns:
            评估指标字典
        """
        labels = self.model.labels_
        
        return {
            "silhouette_score": silhouette_score(X_scaled, labels),
            "calinski_harabasz_score": calinski_harabasz_score(X_scaled, labels),
            "inertia": self.model.inertia_,
        }
    
    def get_cluster_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        获取各群组的统计摘要
        
        Args:
            df: 包含 cluster 列的数据
        
        Returns:
            各群组统计摘要
        """
        if "cluster" not in df.columns:
            raise ValueError("数据中没有 cluster 列，请先进行聚类")
        
        # 数值列统计
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if "cluster" in numeric_cols:
            numeric_cols.remove("cluster")
        
        summary = df.groupby("cluster")[numeric_cols].agg(["mean", "std", "count"])
        
        return summary
    
    def get_cluster_profiles(self, df: pd.DataFrame) -> Dict[int, Dict]:
        """
        获取各群组的画像
        
        Args:
            df: 包含 cluster 列的数据
        
        Returns:
            各群组画像字典
        """
        if "cluster" not in df.columns:
            raise ValueError("数据中没有 cluster 列")
        
        profiles = {}
        
        for cluster_id in range(self.n_clusters):
            cluster_data = df[df["cluster"] == cluster_id]
            
            profile = {
                "count": len(cluster_data),
                "percentage": len(cluster_data) / len(df) * 100,
                "label": self.CLUSTER_LABELS.get(cluster_id, f"群组{cluster_id}"),
            }
            
            # 添加各特征的均值
            for feature in self.features:
                if feature in cluster_data.columns:
                    profile[f"avg_{feature}"] = cluster_data[feature].mean()
            
            profiles[cluster_id] = profile
        
        return profiles
    
    def get_pca_coordinates(self, X: pd.DataFrame) -> np.ndarray:
        """
        获取 PCA 降维后的坐标（用于可视化）
        
        Args:
            X: 特征矩阵
        
        Returns:
            2D 坐标数组
        """
        X_scaled = self.scaler.transform(X)
        return self.pca.fit_transform(X_scaled)
    
    def find_optimal_clusters(
        self,
        X: pd.DataFrame,
        max_clusters: int = 10
    ) -> Dict[int, float]:
        """
        寻找最优聚类数（肘部法则 + 轮廓系数）
        
        Args:
            X: 特征矩阵
            max_clusters: 最大聚类数
        
        Returns:
            各聚类数对应的轮廓系数
        """
        X_scaled = self.scaler.fit_transform(X)
        
        scores = {}
        for k in range(2, max_clusters + 1):
            kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
            labels = kmeans.fit_predict(X_scaled)
            scores[k] = silhouette_score(X_scaled, labels)
        
        return scores

