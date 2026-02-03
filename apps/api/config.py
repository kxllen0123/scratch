"""
环境配置管理模块

支持 Dev、Stage、Prd 三个环境的配置管理
使用环境变量进行配置
"""

import os
from enum import Enum
from typing import List


class Environment(str, Enum):
    """环境枚举"""

    DEV = "dev"
    STAGE = "stage"
    PRD = "prd"


class Config:
    """应用配置类"""

    def __init__(self):
        # 从环境变量读取当前环境，默认为 dev
        self.environment = Environment(os.getenv("ENVIRONMENT", "dev"))

        # API 配置
        self.api_title = "Code-Sentinel API"
        self.api_version = "1.0.0"
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("API_PORT", "8000"))

        # CORS 配置
        self.cors_origins = self._get_cors_origins()
        self.cors_credentials = True
        self.cors_methods = ["*"]
        self.cors_headers = ["*"]

        # 日志配置
        self.log_level = self._get_log_level()
        self.log_format = "json"  # 结构化日志格式

        # 性能配置
        self.max_code_length = 100000
        self.request_timeout = 30  # 秒

    def _get_cors_origins(self) -> List[str]:
        """根据环境获取 CORS 允许的来源"""
        if self.environment == Environment.DEV:
            # 开发环境允许所有来源
            return ["*"]
        elif self.environment == Environment.STAGE:
            # 预发布环境允许特定域名
            return [
                "https://stage.code-sentinel.com",
                "http://localhost:3000",
                "http://localhost:3001",
            ]
        else:  # PRD
            # 生产环境只允许生产域名
            return [
                "https://code-sentinel.com",
                "https://www.code-sentinel.com",
            ]

    def _get_log_level(self) -> str:
        """根据环境获取日志级别"""
        if self.environment == Environment.DEV:
            return "DEBUG"
        elif self.environment == Environment.STAGE:
            return "INFO"
        else:  # PRD
            return "WARNING"

    @property
    def is_dev(self) -> bool:
        """是否为开发环境"""
        return self.environment == Environment.DEV

    @property
    def is_stage(self) -> bool:
        """是否为预发布环境"""
        return self.environment == Environment.STAGE

    @property
    def is_prd(self) -> bool:
        """是否为生产环境"""
        return self.environment == Environment.PRD

    def __repr__(self) -> str:
        return f"Config(environment={self.environment.value})"


# 创建全局配置实例
config = Config()
