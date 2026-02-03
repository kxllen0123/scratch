"""
测试环境配置模块

验证配置模块正确支持 Dev、Stage、Prd 三个环境
"""

import os
import pytest
from config import Config, Environment


def test_default_environment_is_dev():
    """测试默认环境是 dev"""
    # 清除环境变量
    if "ENVIRONMENT" in os.environ:
        del os.environ["ENVIRONMENT"]

    config = Config()
    assert config.environment == Environment.DEV
    assert config.is_dev is True
    assert config.is_stage is False
    assert config.is_prd is False


def test_dev_environment_configuration():
    """测试 dev 环境配置"""
    os.environ["ENVIRONMENT"] = "dev"
    config = Config()

    assert config.environment == Environment.DEV
    assert config.is_dev is True
    assert config.cors_origins == ["*"]
    assert config.log_level == "DEBUG"


def test_stage_environment_configuration():
    """测试 stage 环境配置"""
    os.environ["ENVIRONMENT"] = "stage"
    config = Config()

    assert config.environment == Environment.STAGE
    assert config.is_stage is True
    assert "https://stage.code-sentinel.com" in config.cors_origins
    assert "http://localhost:3000" in config.cors_origins
    assert config.log_level == "INFO"


def test_prd_environment_configuration():
    """测试 prd 环境配置"""
    os.environ["ENVIRONMENT"] = "prd"
    config = Config()

    assert config.environment == Environment.PRD
    assert config.is_prd is True
    assert "https://code-sentinel.com" in config.cors_origins
    assert "https://www.code-sentinel.com" in config.cors_origins
    assert "*" not in config.cors_origins
    assert config.log_level == "WARNING"


def test_api_configuration():
    """测试 API 基本配置"""
    config = Config()

    assert config.api_title == "Code-Sentinel API"
    assert config.api_version == "1.0.0"
    assert config.api_host == "0.0.0.0"
    assert config.api_port == 8000


def test_custom_api_host_and_port():
    """测试自定义 API 主机和端口"""
    os.environ["API_HOST"] = "127.0.0.1"
    os.environ["API_PORT"] = "9000"

    config = Config()

    assert config.api_host == "127.0.0.1"
    assert config.api_port == 9000

    # 清理环境变量
    del os.environ["API_HOST"]
    del os.environ["API_PORT"]


def test_cors_configuration():
    """测试 CORS 配置"""
    config = Config()

    assert config.cors_credentials is True
    assert config.cors_methods == ["*"]
    assert config.cors_headers == ["*"]


def test_performance_configuration():
    """测试性能配置"""
    config = Config()

    assert config.max_code_length == 100000
    assert config.request_timeout == 30


def test_log_format():
    """测试日志格式配置"""
    config = Config()

    assert config.log_format == "json"


def test_config_repr():
    """测试配置对象的字符串表示"""
    os.environ["ENVIRONMENT"] = "dev"
    config = Config()

    repr_str = repr(config)
    assert "Config" in repr_str
    assert "environment=dev" in repr_str


def test_environment_enum_values():
    """测试环境枚举值"""
    assert Environment.DEV.value == "dev"
    assert Environment.STAGE.value == "stage"
    assert Environment.PRD.value == "prd"


# 清理：在所有测试后重置环境变量
@pytest.fixture(autouse=True)
def reset_environment():
    """在每个测试后重置环境变量"""
    yield
    # 重置为默认 dev 环境
    os.environ["ENVIRONMENT"] = "dev"
