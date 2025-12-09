"""
AI 助手工具模块
定义可供 AI 助手调用的工具
"""

import os
import json
import time
import pandas as pd
from pathlib import Path
from typing import Any, Dict

from qwen_agent.tools.base import BaseTool, register_tool

from ..config import settings, db_config
from ..visualization import ChartGenerator


@register_tool("exc_sql")
class SQLQueryTool(BaseTool):
    """
    SQL 查询工具
    执行传入的 SQL 语句并返回结果，自动生成可视化图表
    """
    
    description = "对于生成的SQL，进行SQL查询，并自动可视化"
    parameters = [
        {
            "name": "sql_input",
            "type": "string",
            "description": "生成的SQL语句",
            "required": True,
        }
    ]
    
    def __init__(self, cfg: Dict = None):
        super().__init__(cfg)
        self._engine = None
        self.chart_generator = ChartGenerator()
    
    @property
    def engine(self):
        """懒加载数据库引擎"""
        if self._engine is None:
            self._engine = db_config.create_engine()
        return self._engine
    
    def call(self, params: str, **kwargs) -> str:
        """
        执行 SQL 查询
        
        Args:
            params: JSON 格式的参数字符串
        
        Returns:
            查询结果（Markdown 表格 + 图表）
        """
        try:
            args = json.loads(params)
            sql_input = args["sql_input"]
            database = args.get("database", db_config.database)
            
            # 执行查询
            engine = self.engine
            if database != db_config.database:
                config = db_config.__class__(database=database)
                engine = config.create_engine()
            
            df = pd.read_sql(sql_input, engine)
            
            # 生成 Markdown 表格
            md_table = df.head(10).to_markdown(index=False)
            
            # 生成图表
            chart_path = self._generate_chart(df)
            
            # 构建返回结果
            result = md_table
            if chart_path:
                img_md = f"\n\n![数据分析图表]({chart_path})"
                result += img_md
            
            return result
            
        except Exception as e:
            return f"SQL执行或可视化出错: {str(e)}"
    
    def _generate_chart(self, df: pd.DataFrame) -> str:
        """
        根据数据自动生成合适的图表
        
        Args:
            df: 查询结果数据
        
        Returns:
            图表文件路径
        """
        if df.empty:
            return ""
        
        try:
            # 获取列信息
            columns = df.columns.tolist()
            object_cols = df.select_dtypes(include="object").columns.tolist()
            numeric_cols = df.select_dtypes(exclude="object").columns.tolist()
            
            # 如果第一列是分类列，其他是数值列，生成柱状图
            if columns[0] in object_cols and numeric_cols:
                _, filepath = self.chart_generator.bar_chart(
                    df,
                    x=columns[0],
                    y=numeric_cols,
                    title="银行客户数据分析",
                    stacked=len(numeric_cols) > 1,
                )
                return filepath
            
            # 如果只有数值列，生成折线图
            if numeric_cols and len(df) > 1:
                _, filepath = self.chart_generator.line_chart(
                    df,
                    y=numeric_cols[:3],  # 最多显示3条线
                    title="银行客户数据分析",
                )
                return filepath
            
        except Exception as e:
            print(f"图表生成失败: {e}")
        
        return ""


# 注册其他工具（可扩展）
# @register_tool("predict_high_value")
# class HighValuePredictTool(BaseTool):
#     """高价值客户预测工具"""
#     pass

