"""
高价值客户预测模型
使用 LightGBM 预测客户未来是否会成为高净值客户
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, classification_report
)

from .base import BaseModel
from ..config import settings
from ..data import FeatureEngineer


class HighValuePredictor(BaseModel):
    """高价值客户预测器"""
    
    DEFAULT_PARAMS = {
        "objective": "binary",
        "metric": "auc",
        "verbosity": -1,
        "boosting_type": "gbdt",
        "seed": 42,
        "num_leaves": 31,
        "learning_rate": 0.05,
        "feature_fraction": 0.9,
    }
    
    def __init__(
        self,
        name: str = "high_value_predictor",
        params: Optional[Dict] = None,
        num_boost_round: int = 100
    ):
        super().__init__(name)
        self.params = {**self.DEFAULT_PARAMS, **(params or {})}
        self.num_boost_round = num_boost_round
        self.feature_names: List[str] = []
        self.feature_engineer = FeatureEngineer()
    
    def prepare_data(
        self,
        df: pd.DataFrame,
        threshold: float = None
    ) -> Tuple[pd.DataFrame, pd.Series]:
        """
        准备训练数据
        
        Args:
            df: 原始数据
            threshold: 高价值阈值
        
        Returns:
            (特征矩阵, 标签)
        """
        threshold = threshold or settings.HIGH_VALUE_THRESHOLD
        
        # 创建特征
        df = self.feature_engineer.create_high_value_features(df)
        df = self.feature_engineer.create_high_value_label(df, threshold=threshold)
        
        # 获取特征矩阵
        X, self.feature_names = self.feature_engineer.get_feature_matrix(df)
        y = df["label"]
        
        return X, y
    
    def fit(
        self,
        X: pd.DataFrame,
        y: pd.Series,
        test_size: float = 0.2,
        early_stopping_rounds: int = 10,
        **kwargs
    ) -> Dict[str, float]:
        """
        训练模型
        
        Args:
            X: 特征矩阵
            y: 标签
            test_size: 测试集比例
            early_stopping_rounds: 早停轮数
        
        Returns:
            评估指标字典
        """
        # 划分数据集
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        # 创建 LightGBM 数据集
        train_data = lgb.Dataset(X_train, label=y_train)
        val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)
        
        # 训练模型
        self.model = lgb.train(
            self.params,
            train_data,
            num_boost_round=self.num_boost_round,
            valid_sets=[train_data, val_data],
            valid_names=["train", "valid"],
            callbacks=[
                lgb.early_stopping(stopping_rounds=early_stopping_rounds),
                lgb.log_evaluation(period=20),
            ],
        )
        
        self.is_fitted = True
        
        # 存储特征名
        if isinstance(X, pd.DataFrame):
            self.feature_names = X.columns.tolist()
        
        # 评估模型
        metrics = self.evaluate(X_val, y_val)
        self.metadata["metrics"] = metrics
        self.metadata["feature_names"] = self.feature_names
        
        return metrics
    
    def predict(self, X: pd.DataFrame, threshold: float = 0.5) -> np.ndarray:
        """
        预测类别
        
        Args:
            X: 特征矩阵
            threshold: 分类阈值
        
        Returns:
            预测类别数组
        """
        proba = self.predict_proba(X)
        return (proba >= threshold).astype(int)
    
    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        """
        预测概率
        
        Args:
            X: 特征矩阵
        
        Returns:
            预测概率数组
        """
        if not self.is_fitted:
            raise ValueError("模型尚未训练，请先调用 fit() 方法")
        
        return self.model.predict(X)
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """
        评估模型
        
        Args:
            X: 特征矩阵
            y: 真实标签
        
        Returns:
            评估指标字典
        """
        y_pred = self.predict(X)
        y_proba = self.predict_proba(X)
        
        return {
            "accuracy": accuracy_score(y, y_pred),
            "precision": precision_score(y, y_pred, zero_division=0),
            "recall": recall_score(y, y_pred, zero_division=0),
            "f1": f1_score(y, y_pred, zero_division=0),
            "auc": roc_auc_score(y, y_proba) if len(np.unique(y)) > 1 else 0,
        }
    
    def get_feature_importance(self, importance_type: str = "split") -> pd.DataFrame:
        """
        获取特征重要性
        
        Args:
            importance_type: 重要性类型 ('split' 或 'gain')
        
        Returns:
            特征重要性 DataFrame
        """
        if not self.is_fitted:
            raise ValueError("模型尚未训练")
        
        importance = self.model.feature_importance(importance_type=importance_type)
        
        df = pd.DataFrame({
            "feature": self.feature_names,
            "importance": importance
        })
        
        return df.sort_values("importance", ascending=False).reset_index(drop=True)
    
    def save_model(self, filepath: Optional[Path] = None) -> Path:
        """
        保存 LightGBM 模型（文本格式）
        """
        if filepath is None:
            filepath = settings.MODEL_DIR / f"{self.name}.txt"
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        self.model.save_model(str(filepath))
        return filepath
    
    def load_model(self, filepath: Optional[Path] = None) -> "HighValuePredictor":
        """
        加载 LightGBM 模型
        """
        if filepath is None:
            filepath = settings.MODEL_DIR / f"{self.name}.txt"
        
        self.model = lgb.Booster(model_file=str(filepath))
        self.is_fitted = True
        
        return self

