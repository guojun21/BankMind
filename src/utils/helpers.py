"""
通用工具函数
"""

from typing import Union, Optional
import numpy as np


def format_number(value: Union[int, float], precision: int = 2) -> str:
    """
    格式化数字，自动转换为万/亿
    
    Args:
        value: 数值
        precision: 小数位数
    
    Returns:
        格式化后的字符串
    """
    if value is None or np.isnan(value):
        return "--"
    
    if abs(value) >= 100000000:  # 亿
        return f"{value / 100000000:.{precision}f}亿"
    elif abs(value) >= 10000:  # 万
        return f"{value / 10000:.{precision}f}万"
    else:
        return f"{value:,.{precision}f}"


def format_currency(value: Union[int, float], currency: str = "¥") -> str:
    """
    格式化货币
    
    Args:
        value: 金额
        currency: 货币符号
    
    Returns:
        格式化后的字符串
    """
    if value is None or np.isnan(value):
        return "--"
    
    formatted = format_number(value)
    return f"{currency}{formatted}"


def format_percentage(value: Union[int, float], precision: int = 1) -> str:
    """
    格式化百分比
    
    Args:
        value: 比例值（0-1）
        precision: 小数位数
    
    Returns:
        格式化后的字符串
    """
    if value is None or np.isnan(value):
        return "--"
    
    return f"{value * 100:.{precision}f}%"


def safe_divide(
    numerator: Union[int, float],
    denominator: Union[int, float],
    default: float = 0.0
) -> float:
    """
    安全除法，避免除零错误
    
    Args:
        numerator: 分子
        denominator: 分母
        default: 除零时的默认值
    
    Returns:
        除法结果
    """
    if denominator == 0 or denominator is None:
        return default
    return numerator / denominator


def truncate_string(s: str, max_length: int = 50, suffix: str = "...") -> str:
    """
    截断字符串
    
    Args:
        s: 原始字符串
        max_length: 最大长度
        suffix: 截断后缀
    
    Returns:
        截断后的字符串
    """
    if len(s) <= max_length:
        return s
    return s[:max_length - len(suffix)] + suffix


def clean_column_name(name: str) -> str:
    """
    清理列名，转换为 Python 友好的格式
    
    Args:
        name: 原始列名
    
    Returns:
        清理后的列名
    """
    import re
    # 转小写
    name = name.lower()
    # 替换空格和特殊字符
    name = re.sub(r"[^a-z0-9_]", "_", name)
    # 移除连续下划线
    name = re.sub(r"_+", "_", name)
    # 移除首尾下划线
    name = name.strip("_")
    return name


def get_time_greeting() -> str:
    """
    根据当前时间返回问候语
    
    Returns:
        问候语
    """
    from datetime import datetime
    
    hour = datetime.now().hour
    
    if 5 <= hour < 12:
        return "早上好"
    elif 12 <= hour < 14:
        return "中午好"
    elif 14 <= hour < 18:
        return "下午好"
    else:
        return "晚上好"

