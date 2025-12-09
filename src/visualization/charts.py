"""
图表生成模块
提供各种常用图表的生成方法
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union
import time

from ..config import settings
from .style import setup_chinese_font, get_color_palette


class ChartGenerator:
    """图表生成器"""
    
    def __init__(
        self,
        output_dir: Optional[Path] = None,
        palette: str = "bank"
    ):
        self.output_dir = output_dir or settings.OUTPUT_DIR / "charts"
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.colors = get_color_palette(palette)
        setup_chinese_font()
    
    def _save_figure(
        self,
        fig: plt.Figure,
        filename: str = None,
        prefix: str = ""
    ) -> str:
        """保存图表"""
        if filename is None:
            timestamp = int(time.time() * 1000)
            filename = f"{prefix}chart_{timestamp}.png"
        
        filepath = self.output_dir / filename
        fig.savefig(filepath, dpi=settings.FIGURE_DPI, bbox_inches="tight")
        plt.close(fig)
        
        return str(filepath)
    
    def bar_chart(
        self,
        data: Union[pd.DataFrame, Dict],
        x: str = None,
        y: Union[str, List[str]] = None,
        title: str = "柱状图",
        xlabel: str = None,
        ylabel: str = "数值",
        stacked: bool = False,
        horizontal: bool = False,
        save: bool = True,
        filename: str = None
    ) -> Tuple[plt.Figure, str]:
        """
        生成柱状图
        
        Args:
            data: 数据（DataFrame 或字典）
            x: X 轴列名
            y: Y 轴列名（可多个）
            title: 图表标题
            xlabel: X 轴标签
            ylabel: Y 轴标签
            stacked: 是否堆叠
            horizontal: 是否水平
            save: 是否保存
            filename: 保存文件名
        
        Returns:
            (Figure, 文件路径)
        """
        fig, ax = plt.subplots(figsize=settings.FIGURE_SIZE)
        
        # 处理字典数据
        if isinstance(data, dict):
            df = pd.DataFrame(list(data.items()), columns=["category", "value"])
            x, y = "category", "value"
        else:
            df = data.copy()
        
        # 确定 X 轴
        if x is None:
            x = df.columns[0]
        
        # 确定 Y 轴（可能多列）
        if y is None:
            y = [col for col in df.columns if col != x and df[col].dtype in ["int64", "float64"]]
        elif isinstance(y, str):
            y = [y]
        
        # 绑定数据
        x_data = np.arange(len(df))
        width = 0.8 / len(y) if not stacked else 0.8
        
        if stacked:
            bottom = np.zeros(len(df))
            for i, col in enumerate(y):
                if horizontal:
                    ax.barh(x_data, df[col], left=bottom, label=col, color=self.colors[i % len(self.colors)])
                else:
                    ax.bar(x_data, df[col], bottom=bottom, label=col, color=self.colors[i % len(self.colors)])
                bottom += df[col].fillna(0).values
        else:
            for i, col in enumerate(y):
                offset = (i - len(y) / 2 + 0.5) * width
                if horizontal:
                    ax.barh(x_data + offset, df[col], height=width, label=col, color=self.colors[i % len(self.colors)])
                else:
                    ax.bar(x_data + offset, df[col], width=width, label=col, color=self.colors[i % len(self.colors)])
        
        # 设置标签
        if horizontal:
            ax.set_yticks(x_data)
            ax.set_yticklabels(df[x])
            ax.set_xlabel(ylabel)
            ax.set_ylabel(xlabel or x)
        else:
            ax.set_xticks(x_data)
            ax.set_xticklabels(df[x], rotation=45, ha="right")
            ax.set_xlabel(xlabel or x)
            ax.set_ylabel(ylabel)
        
        ax.set_title(title)
        if len(y) > 1:
            ax.legend()
        
        plt.tight_layout()
        
        filepath = ""
        if save:
            filepath = self._save_figure(fig, filename, prefix="bar_")
        
        return fig, filepath
    
    def pie_chart(
        self,
        data: Union[pd.DataFrame, Dict],
        values: str = None,
        labels: str = None,
        title: str = "饼图",
        show_percentage: bool = True,
        save: bool = True,
        filename: str = None
    ) -> Tuple[plt.Figure, str]:
        """
        生成饼图
        
        Args:
            data: 数据
            values: 值列名
            labels: 标签列名
            title: 标题
            show_percentage: 是否显示百分比
            save: 是否保存
            filename: 文件名
        
        Returns:
            (Figure, 文件路径)
        """
        fig, ax = plt.subplots(figsize=(8, 8))
        
        if isinstance(data, dict):
            labels_data = list(data.keys())
            values_data = list(data.values())
        else:
            if labels is None:
                labels = data.columns[0]
            if values is None:
                values = data.columns[1]
            labels_data = data[labels].tolist()
            values_data = data[values].tolist()
        
        autopct = "%1.1f%%" if show_percentage else None
        
        ax.pie(
            values_data,
            labels=labels_data,
            autopct=autopct,
            colors=self.colors[:len(values_data)],
            startangle=90,
        )
        ax.set_title(title)
        
        filepath = ""
        if save:
            filepath = self._save_figure(fig, filename, prefix="pie_")
        
        return fig, filepath
    
    def line_chart(
        self,
        data: pd.DataFrame,
        x: str = None,
        y: Union[str, List[str]] = None,
        title: str = "折线图",
        xlabel: str = None,
        ylabel: str = "数值",
        markers: bool = True,
        save: bool = True,
        filename: str = None
    ) -> Tuple[plt.Figure, str]:
        """
        生成折线图
        
        Args:
            data: 数据
            x: X 轴列名
            y: Y 轴列名
            title: 标题
            xlabel: X 轴标签
            ylabel: Y 轴标签
            markers: 是否显示数据点
            save: 是否保存
            filename: 文件名
        
        Returns:
            (Figure, 文件路径)
        """
        fig, ax = plt.subplots(figsize=settings.FIGURE_SIZE)
        
        if x is None:
            x = data.columns[0]
        if y is None:
            y = [col for col in data.columns if col != x and data[col].dtype in ["int64", "float64"]]
        elif isinstance(y, str):
            y = [y]
        
        marker = "o" if markers else None
        
        for i, col in enumerate(y):
            ax.plot(
                data[x], data[col],
                marker=marker,
                label=col,
                color=self.colors[i % len(self.colors)],
                linewidth=2
            )
        
        ax.set_xlabel(xlabel or x)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        
        if len(y) > 1:
            ax.legend()
        
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        
        filepath = ""
        if save:
            filepath = self._save_figure(fig, filename, prefix="line_")
        
        return fig, filepath
    
    def scatter_chart(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        hue: str = None,
        title: str = "散点图",
        xlabel: str = None,
        ylabel: str = None,
        save: bool = True,
        filename: str = None
    ) -> Tuple[plt.Figure, str]:
        """
        生成散点图
        
        Args:
            data: 数据
            x: X 轴列名
            y: Y 轴列名
            hue: 分组列名
            title: 标题
            xlabel: X 轴标签
            ylabel: Y 轴标签
            save: 是否保存
            filename: 文件名
        
        Returns:
            (Figure, 文件路径)
        """
        fig, ax = plt.subplots(figsize=settings.FIGURE_SIZE)
        
        if hue is None:
            ax.scatter(data[x], data[y], c=self.colors[0], alpha=0.6)
        else:
            groups = data[hue].unique()
            for i, group in enumerate(groups):
                mask = data[hue] == group
                ax.scatter(
                    data.loc[mask, x],
                    data.loc[mask, y],
                    c=self.colors[i % len(self.colors)],
                    label=str(group),
                    alpha=0.6
                )
            ax.legend()
        
        ax.set_xlabel(xlabel or x)
        ax.set_ylabel(ylabel or y)
        ax.set_title(title)
        
        plt.tight_layout()
        
        filepath = ""
        if save:
            filepath = self._save_figure(fig, filename, prefix="scatter_")
        
        return fig, filepath
    
    def histogram(
        self,
        data: pd.DataFrame,
        column: str,
        bins: int = 20,
        title: str = "直方图",
        xlabel: str = None,
        ylabel: str = "频数",
        save: bool = True,
        filename: str = None
    ) -> Tuple[plt.Figure, str]:
        """
        生成直方图
        
        Args:
            data: 数据
            column: 列名
            bins: 分箱数
            title: 标题
            xlabel: X 轴标签
            ylabel: Y 轴标签
            save: 是否保存
            filename: 文件名
        
        Returns:
            (Figure, 文件路径)
        """
        fig, ax = plt.subplots(figsize=settings.FIGURE_SIZE)
        
        ax.hist(data[column].dropna(), bins=bins, color=self.colors[0], edgecolor="white")
        
        ax.set_xlabel(xlabel or column)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        
        plt.tight_layout()
        
        filepath = ""
        if save:
            filepath = self._save_figure(fig, filename, prefix="hist_")
        
        return fig, filepath
    
    def feature_importance_chart(
        self,
        importance_df: pd.DataFrame,
        feature_col: str = "feature",
        importance_col: str = "importance",
        title: str = "特征重要性",
        top_n: int = 10,
        save: bool = True,
        filename: str = None
    ) -> Tuple[plt.Figure, str]:
        """
        生成特征重要性图
        
        Args:
            importance_df: 特征重要性数据
            feature_col: 特征列名
            importance_col: 重要性列名
            title: 标题
            top_n: 显示前 N 个特征
            save: 是否保存
            filename: 文件名
        
        Returns:
            (Figure, 文件路径)
        """
        df = importance_df.nlargest(top_n, importance_col)
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        y_pos = np.arange(len(df))
        ax.barh(y_pos, df[importance_col], color=self.colors[0])
        ax.set_yticks(y_pos)
        ax.set_yticklabels(df[feature_col])
        ax.invert_yaxis()  # 最重要的在上面
        ax.set_xlabel("重要性")
        ax.set_title(title)
        
        plt.tight_layout()
        
        filepath = ""
        if save:
            filepath = self._save_figure(fig, filename, prefix="importance_")
        
        return fig, filepath
    
    def cluster_scatter(
        self,
        data: pd.DataFrame,
        x: str,
        y: str,
        cluster_col: str = "cluster",
        title: str = "客户聚类分布",
        save: bool = True,
        filename: str = None
    ) -> Tuple[plt.Figure, str]:
        """
        生成聚类散点图
        
        Args:
            data: 数据
            x: X 轴列名
            y: Y 轴列名
            cluster_col: 聚类标签列名
            title: 标题
            save: 是否保存
            filename: 文件名
        
        Returns:
            (Figure, 文件路径)
        """
        return self.scatter_chart(
            data, x, y,
            hue=cluster_col,
            title=title,
            save=save,
            filename=filename
        )
    
    def time_series_forecast(
        self,
        history: pd.Series,
        forecast: pd.Series,
        title: str = "资产趋势预测",
        xlabel: str = "时间",
        ylabel: str = "资产",
        save: bool = True,
        filename: str = None
    ) -> Tuple[plt.Figure, str]:
        """
        生成时间序列预测图
        
        Args:
            history: 历史数据
            forecast: 预测数据
            title: 标题
            xlabel: X 轴标签
            ylabel: Y 轴标签
            save: 是否保存
            filename: 文件名
        
        Returns:
            (Figure, 文件路径)
        """
        fig, ax = plt.subplots(figsize=settings.FIGURE_SIZE)
        
        ax.plot(history.index, history.values, marker="o", label="历史数据", color=self.colors[0], linewidth=2)
        ax.plot(forecast.index, forecast.values, marker="*", label="预测数据", color=self.colors[1], linewidth=2, linestyle="--")
        
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend()
        
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        
        filepath = ""
        if save:
            filepath = self._save_figure(fig, filename, prefix="forecast_")
        
        return fig, filepath

