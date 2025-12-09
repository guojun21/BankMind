"""
可视化样式配置
统一管理图表样式、颜色、字体等
"""

import matplotlib.pyplot as plt
import matplotlib
from typing import List

from ..config import settings


def setup_chinese_font() -> None:
    """
    设置 matplotlib 中文字体
    解决中文显示乱码问题
    """
    # 尝试设置中文字体
    for font in settings.CHINESE_FONTS:
        try:
            matplotlib.rcParams["font.sans-serif"] = [font] + matplotlib.rcParams["font.sans-serif"]
            break
        except Exception:
            continue
    
    # 解决负号显示问题
    matplotlib.rcParams["axes.unicode_minus"] = False
    
    # 设置默认图片质量
    matplotlib.rcParams["figure.dpi"] = settings.FIGURE_DPI
    matplotlib.rcParams["savefig.dpi"] = settings.FIGURE_DPI


def get_color_palette(name: str = "default") -> List[str]:
    """
    获取颜色调色板
    
    Args:
        name: 调色板名称
    
    Returns:
        颜色列表
    """
    palettes = {
        "default": [
            "#4E79A7",  # 蓝色
            "#F28E2B",  # 橙色
            "#E15759",  # 红色
            "#76B7B2",  # 青色
            "#59A14F",  # 绿色
            "#EDC948",  # 黄色
            "#B07AA1",  # 紫色
            "#FF9DA7",  # 粉色
            "#9C755F",  # 棕色
            "#BAB0AC",  # 灰色
        ],
        "bank": [
            "#1E3A5F",  # 深蓝（银行主色）
            "#3498DB",  # 亮蓝
            "#27AE60",  # 绿色（增长）
            "#E74C3C",  # 红色（警告）
            "#F39C12",  # 橙色
            "#9B59B6",  # 紫色
            "#1ABC9C",  # 青色
            "#34495E",  # 深灰
        ],
        "warm": [
            "#FF6B6B",
            "#FFA07A",
            "#FFD93D",
            "#6BCB77",
            "#4D96FF",
        ],
        "cool": [
            "#00B4D8",
            "#0077B6",
            "#90E0EF",
            "#CAF0F8",
            "#023E8A",
        ],
    }
    
    return palettes.get(name, palettes["default"])


def get_chart_style() -> dict:
    """
    获取图表样式配置
    
    Returns:
        样式配置字典
    """
    return {
        "figure.figsize": settings.FIGURE_SIZE,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }


def apply_chart_style() -> None:
    """应用图表样式"""
    setup_chinese_font()
    plt.rcParams.update(get_chart_style())


# 模块导入时自动设置中文字体
setup_chinese_font()

