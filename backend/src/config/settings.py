"""
全局配置管理
统一管理项目的所有配置项，支持环境变量覆盖
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional


@dataclass
class Settings:
    """全局配置类"""
    
    # ===== 项目路径 =====
    PROJECT_ROOT: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent)
    DATA_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "data")
    OUTPUT_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "output")
    MODEL_DIR: Path = field(default_factory=lambda: Path(__file__).parent.parent.parent / "models" / "saved")
    
    # ===== API 配置 =====
    DASHSCOPE_API_KEY: str = field(
        default_factory=lambda: os.getenv("DASHSCOPE_API_KEY", "")
    )
    DASHSCOPE_TIMEOUT: int = 30
    
    # ===== 模型配置 =====
    LLM_MODEL: str = "qwen-turbo-2025-04-28"
    LLM_RETRY_COUNT: int = 3
    
    # ===== 可视化配置 =====
    CHINESE_FONTS: List[str] = field(
        default_factory=lambda: ["SimHei", "Microsoft YaHei", "SimSun", "Arial Unicode MS", "PingFang SC"]
    )
    FIGURE_DPI: int = 150
    FIGURE_SIZE: tuple = (10, 6)
    
    # ===== 业务配置 =====
    HIGH_VALUE_THRESHOLD: float = 1000000  # 高净值客户资产阈值 (100万)
    PREDICTION_MONTHS: int = 3  # 预测周期（月）
    
    # ===== 聚类配置 =====
    DEFAULT_N_CLUSTERS: int = 3
    
    # ===== 关联分析配置 =====
    APRIORI_MIN_SUPPORT: float = 0.05
    APRIORI_MIN_LIFT: float = 1.0
    
    def __post_init__(self):
        """初始化后创建必要的目录"""
        self.DATA_DIR.mkdir(parents=True, exist_ok=True)
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.MODEL_DIR.mkdir(parents=True, exist_ok=True)
        (self.OUTPUT_DIR / "charts").mkdir(exist_ok=True)
        (self.OUTPUT_DIR / "reports").mkdir(exist_ok=True)


# 全局配置实例
settings = Settings()

