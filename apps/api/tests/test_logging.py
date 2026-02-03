"""
测试结构化日志记录功能

验证日志记录器正确配置并记录关键操作
"""

import json
import logging
from fastapi.testclient import TestClient
from main import app, logger, JSONFormatter


client = TestClient(app)


def test_json_formatter():
    """测试 JSON 格式化器正确格式化日志记录"""
    formatter = JSONFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Test message",
        args=(),
        exc_info=None,
    )

    # 添加额外字段
    record.request_id = "test-123"
    record.method = "GET"
    record.path = "/test"
    record.status_code = 200
    record.duration_ms = 15.5

    formatted = formatter.format(record)
    log_data = json.loads(formatted)

    # 验证基本字段
    assert log_data["level"] == "INFO"
    assert log_data["logger"] == "test"
    assert log_data["message"] == "Test message"

    # 验证额外字段
    assert log_data["request_id"] == "test-123"
    assert log_data["method"] == "GET"
    assert log_data["path"] == "/test"
    assert log_data["status_code"] == 200
    assert log_data["duration_ms"] == 15.5


def test_logger_configuration():
    """测试日志记录器正确配置"""
    assert logger.name == "code-sentinel"
    # 日志级别根据环境配置，在 dev 环境下是 DEBUG
    assert logger.level in [logging.DEBUG, logging.INFO, logging.WARNING]
    assert len(logger.handlers) > 0

    # 验证处理器配置
    handler = logger.handlers[0]
    assert isinstance(handler, logging.StreamHandler)
    assert isinstance(handler.formatter, JSONFormatter)


def test_request_logging(caplog):
    """测试请求日志记录"""
    with caplog.at_level(logging.INFO, logger="code-sentinel"):
        response = client.get("/")
        assert response.status_code == 200

    # 验证日志记录
    assert len(caplog.records) >= 2  # 至少有请求开始和完成日志

    # 检查日志消息
    messages = [record.message for record in caplog.records]
    assert any("Request started" in msg for msg in messages)
    assert any("Request completed" in msg for msg in messages)


def test_health_endpoint_logging(caplog):
    """测试健康检查端点日志记录"""
    with caplog.at_level(logging.INFO, logger="code-sentinel"):
        response = client.get("/health")
        assert response.status_code == 200

    # 验证日志包含路径信息
    assert any("/health" in record.message for record in caplog.records)


def test_review_endpoint_logging(caplog):
    """测试代码审查端点日志记录"""
    with caplog.at_level(logging.INFO, logger="code-sentinel"):
        response = client.post(
            "/api/review", json={"code": "def hello(): pass", "language": "python"}
        )
        assert response.status_code == 200

    # 验证日志记录
    messages = [record.message for record in caplog.records]

    # 应该包含请求、审查请求和审查完成的日志
    assert any("Request started" in msg for msg in messages)
    assert any("Code review requested" in msg for msg in messages)
    assert any("Code review completed" in msg for msg in messages)
    assert any("Request completed" in msg for msg in messages)


def test_logging_includes_duration(caplog):
    """测试日志包含请求处理时间"""
    with caplog.at_level(logging.INFO, logger="code-sentinel"):
        response = client.get("/")
        assert response.status_code == 200

    # 查找包含 duration_ms 的日志记录
    duration_logs = [
        record for record in caplog.records if hasattr(record, "duration_ms")
    ]

    assert len(duration_logs) > 0
    # 验证 duration_ms 是数字
    for record in duration_logs:
        assert isinstance(record.duration_ms, (int, float))
        assert record.duration_ms >= 0


def test_logging_includes_status_code(caplog):
    """测试日志包含 HTTP 状态码"""
    with caplog.at_level(logging.INFO, logger="code-sentinel"):
        response = client.get("/")
        assert response.status_code == 200

    # 查找包含 status_code 的日志记录
    status_logs = [
        record for record in caplog.records if hasattr(record, "status_code")
    ]

    assert len(status_logs) > 0
    # 验证 status_code 正确
    for record in status_logs:
        assert record.status_code == 200
