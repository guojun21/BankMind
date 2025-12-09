"""
模型可解释性分析模块
使用 SHAP 解释模型预测
"""

import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Optional, Any
import shap

from ..config import settings


class ModelExplainer:
    """模型解释器"""
    
    def __init__(self, model: Any, feature_names: List[str] = None):
        """
        初始化解释器
        
        Args:
            model: 训练好的模型（支持 LightGBM, XGBoost, sklearn 等）
            feature_names: 特征名称列表
        """
        self.model = model
        self.feature_names = feature_names
        self.explainer = None
        self.shap_values = None
    
    def create_explainer(self, X_background: pd.DataFrame = None) -> "ModelExplainer":
        """
        创建 SHAP 解释器
        
        Args:
            X_background: 背景数据集（用于计算基准值）
        
        Returns:
            self
        """
        # 尝试创建 TreeExplainer（适用于树模型）
        try:
            self.explainer = shap.TreeExplainer(self.model)
        except Exception:
            # 回退到 KernelExplainer
            if X_background is None:
                raise ValueError("非树模型需要提供背景数据集 X_background")
            self.explainer = shap.KernelExplainer(
                self.model.predict,
                X_background.sample(min(100, len(X_background)))
            )
        
        return self
    
    def explain(self, X: pd.DataFrame) -> np.ndarray:
        """
        计算 SHAP 值
        
        Args:
            X: 需要解释的数据
        
        Returns:
            SHAP 值数组
        """
        if self.explainer is None:
            self.create_explainer()
        
        self.shap_values = self.explainer.shap_values(X)
        
        # 更新特征名
        if self.feature_names is None and isinstance(X, pd.DataFrame):
            self.feature_names = X.columns.tolist()
        
        return self.shap_values
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        获取基于 SHAP 的特征重要性
        
        Returns:
            特征重要性 DataFrame
        """
        if self.shap_values is None:
            raise ValueError("请先调用 explain()")
        
        # 处理二分类情况（shap_values 可能是列表）
        values = self.shap_values
        if isinstance(values, list):
            values = values[1]  # 取正类的 SHAP 值
        
        importance = np.abs(values).mean(axis=0)
        
        df = pd.DataFrame({
            "feature": self.feature_names,
            "importance": importance
        })
        
        return df.sort_values("importance", ascending=False).reset_index(drop=True)
    
    def explain_single(
        self,
        X: pd.DataFrame,
        index: int = 0
    ) -> Dict[str, float]:
        """
        解释单个样本的预测
        
        Args:
            X: 数据
            index: 样本索引
        
        Returns:
            各特征对预测的贡献
        """
        if self.shap_values is None:
            self.explain(X)
        
        values = self.shap_values
        if isinstance(values, list):
            values = values[1]
        
        contributions = {}
        for i, feature in enumerate(self.feature_names):
            contributions[feature] = float(values[index, i])
        
        # 按贡献绝对值排序
        return dict(sorted(
            contributions.items(),
            key=lambda x: abs(x[1]),
            reverse=True
        ))
    
    def generate_explanation_text(
        self,
        X: pd.DataFrame,
        index: int = 0,
        top_n: int = 5
    ) -> str:
        """
        生成可读的解释文本
        
        Args:
            X: 数据
            index: 样本索引
            top_n: 显示前 N 个重要特征
        
        Returns:
            解释文本
        """
        contributions = self.explain_single(X, index)
        
        # 获取预测结果
        if hasattr(self.model, "predict_proba"):
            prob = self.model.predict_proba(X.iloc[[index]])[0, 1]
            prediction_text = f"预测概率: {prob:.2%}"
        else:
            pred = self.model.predict(X.iloc[[index]])[0]
            prediction_text = f"预测值: {pred:.4f}"
        
        # 构建解释文本
        lines = [prediction_text, "", "主要影响因素:"]
        
        for i, (feature, value) in enumerate(list(contributions.items())[:top_n]):
            direction = "↑ 正向" if value > 0 else "↓ 负向"
            lines.append(f"  {i+1}. {feature}: {direction} ({value:+.4f})")
        
        return "\n".join(lines)
    
    def batch_explain(
        self,
        X: pd.DataFrame,
        top_n: int = 3
    ) -> pd.DataFrame:
        """
        批量解释多个样本
        
        Args:
            X: 数据
            top_n: 每个样本显示前 N 个特征
        
        Returns:
            解释结果 DataFrame
        """
        if self.shap_values is None:
            self.explain(X)
        
        values = self.shap_values
        if isinstance(values, list):
            values = values[1]
        
        results = []
        for i in range(len(X)):
            # 获取该样本的 SHAP 值
            sample_shap = dict(zip(self.feature_names, values[i]))
            
            # 排序并取 top N
            sorted_features = sorted(
                sample_shap.items(),
                key=lambda x: abs(x[1]),
                reverse=True
            )[:top_n]
            
            result = {"index": i}
            for j, (feature, shap_val) in enumerate(sorted_features):
                result[f"feature_{j+1}"] = feature
                result[f"shap_{j+1}"] = shap_val
            
            results.append(result)
        
        return pd.DataFrame(results)
    
    def save_explanation(
        self,
        X: pd.DataFrame,
        output_dir: str = None,
        prefix: str = ""
    ) -> str:
        """
        保存解释结果
        
        Args:
            X: 数据
            output_dir: 输出目录
            prefix: 文件名前缀
        
        Returns:
            结果文件路径
        """
        output_dir = Path(output_dir) if output_dir else settings.OUTPUT_DIR / "reports"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存特征重要性
        importance_path = output_dir / f"{prefix}shap_importance.csv"
        self.get_feature_importance().to_csv(importance_path, index=False, encoding="utf-8-sig")
        
        # 保存详细解释
        explanation_path = output_dir / f"{prefix}shap_explanations.csv"
        self.batch_explain(X).to_csv(explanation_path, index=False, encoding="utf-8-sig")
        
        return str(importance_path)

