"""
日志配置模块
"""

import logging
import sys
from pathlib import Path
from typing import Optional

from ..config import settings


def get_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    获取配置好的 Logger
    
    Args:
        name: Logger 名称
        level: 日志级别
        log_file: 日志文件路径
    
    Returns:
        Logger 实例
    """
    logger = logging.getLogger(name)
    
    # 避免重复添加 handler
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # 格式化器
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # 控制台 Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件 Handler（可选）
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# 预配置的 Logger
def get_app_logger() -> logging.Logger:
    """获取应用主 Logger"""
    return get_logger("bankmind")


def get_model_logger() -> logging.Logger:
    """获取模型训练 Logger"""
    log_file = settings.OUTPUT_DIR / "logs" / "model.log"
    return get_logger("bankmind.model", log_file=str(log_file))


def get_api_logger() -> logging.Logger:
    """获取 API Logger"""
    return get_logger("bankmind.api")

