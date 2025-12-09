"""
模型基类
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Optional
import pickle
import json

from ..config import settings


class BaseModel(ABC):
    """模型基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.model = None
        self.is_fitted = False
        self.metadata: Dict[str, Any] = {}
    
    @abstractmethod
    def fit(self, X, y=None, **kwargs):
        """训练模型"""
        pass
    
    @abstractmethod
    def predict(self, X, **kwargs):
        """预测"""
        pass
    
    def save(self, filepath: Optional[Path] = None) -> Path:
        """
        保存模型
        
        Args:
            filepath: 保存路径，默认保存到 models/saved 目录
        
        Returns:
            保存的文件路径
        """
        if filepath is None:
            filepath = settings.MODEL_DIR / f"{self.name}.pkl"
        
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, "wb") as f:
            pickle.dump({
                "model": self.model,
                "metadata": self.metadata,
                "is_fitted": self.is_fitted,
            }, f)
        
        return filepath
    
    def load(self, filepath: Optional[Path] = None) -> "BaseModel":
        """
        加载模型
        
        Args:
            filepath: 模型文件路径
        
        Returns:
            self
        """
        if filepath is None:
            filepath = settings.MODEL_DIR / f"{self.name}.pkl"
        
        with open(filepath, "rb") as f:
            data = pickle.load(f)
            self.model = data["model"]
            self.metadata = data["metadata"]
            self.is_fitted = data["is_fitted"]
        
        return self
    
    def get_params(self) -> Dict[str, Any]:
        """获取模型参数"""
        if self.model is not None and hasattr(self.model, "get_params"):
            return self.model.get_params()
        return {}

