"""
数据库配置管理
"""

import os
from dataclasses import dataclass
from typing import Optional
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


@dataclass
class DatabaseConfig:
    """数据库配置类"""
    
    host: str = "rm-uf6z891lon6dxuqblqo.mysql.rds.aliyuncs.com"
    port: int = 3306
    database: str = "bank2"
    username: str = "bank123"
    password: str = "bank321"
    charset: str = "utf8mb4"
    connect_timeout: int = 10
    pool_size: int = 10
    max_overflow: int = 20
    
    def __post_init__(self):
        """支持从环境变量覆盖配置"""
        self.host = os.getenv("DB_HOST", self.host)
        self.port = int(os.getenv("DB_PORT", self.port))
        self.database = os.getenv("DB_NAME", self.database)
        self.username = os.getenv("DB_USER", self.username)
        self.password = os.getenv("DB_PASSWORD", self.password)
    
    @property
    def connection_string(self) -> str:
        """生成数据库连接字符串"""
        return (
            f"mysql+mysqlconnector://{self.username}:{self.password}"
            f"@{self.host}:{self.port}/{self.database}?charset={self.charset}"
        )
    
    def create_engine(self) -> Engine:
        """创建 SQLAlchemy 引擎"""
        return create_engine(
            self.connection_string,
            connect_args={"connect_timeout": self.connect_timeout},
            pool_size=self.pool_size,
            max_overflow=self.max_overflow,
        )


# 全局数据库配置实例
db_config = DatabaseConfig()

