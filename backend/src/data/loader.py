"""
数据加载模块
统一管理数据的读取，支持 CSV 和数据库
"""

import pandas as pd
from pathlib import Path
from typing import Optional, Union
from sqlalchemy import text

from ..config import settings, db_config


class DataLoader:
    """数据加载器"""
    
    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or settings.DATA_DIR
        self._engine = None
    
    @property
    def engine(self):
        """懒加载数据库引擎"""
        if self._engine is None:
            self._engine = db_config.create_engine()
        return self._engine
    
    def load_csv(
        self,
        filename: str,
        encoding: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        加载 CSV 文件，自动处理编码问题
        
        Args:
            filename: 文件名或完整路径
            encoding: 指定编码，默认自动尝试 utf-8 和 gbk
            **kwargs: 传递给 pd.read_csv 的其他参数
        
        Returns:
            DataFrame
        """
        filepath = Path(filename)
        if not filepath.is_absolute():
            filepath = self.data_dir / filename
        
        if encoding:
            return pd.read_csv(filepath, encoding=encoding, **kwargs)
        
        # 自动尝试不同编码
        for enc in ["utf-8", "gbk", "utf-8-sig", "latin1"]:
            try:
                return pd.read_csv(filepath, encoding=enc, **kwargs)
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        raise ValueError(f"无法读取文件 {filepath}，请检查文件编码")
    
    def load_customer_base(self) -> pd.DataFrame:
        """加载客户基础信息表"""
        return self.load_csv("customer_base.csv")
    
    def load_customer_behavior(self) -> pd.DataFrame:
        """加载客户行为资产表"""
        return self.load_csv("customer_behavior_assets.csv")
    
    def load_merged_data(self) -> pd.DataFrame:
        """加载并合并客户数据"""
        base = self.load_customer_base()
        behavior = self.load_customer_behavior()
        return pd.merge(base, behavior, on="customer_id", how="inner")
    
    def query_sql(self, sql: str, database: Optional[str] = None) -> pd.DataFrame:
        """
        执行 SQL 查询
        
        Args:
            sql: SQL 查询语句
            database: 数据库名，默认使用配置中的数据库
        
        Returns:
            DataFrame
        """
        engine = self.engine
        if database and database != db_config.database:
            # 切换数据库
            config = db_config.__class__(database=database)
            engine = config.create_engine()
        
        return pd.read_sql(sql, engine)
    
    def execute_sql(self, sql: str) -> None:
        """执行非查询 SQL（INSERT, UPDATE, DELETE）"""
        with self.engine.connect() as conn:
            conn.execute(text(sql))
            conn.commit()


# 便捷的全局加载器实例
data_loader = DataLoader()

