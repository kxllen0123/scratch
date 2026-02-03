import logging
import json
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from config import config


# 配置结构化日志
class JSONFormatter(logging.Formatter):
    """自定义 JSON 格式化器"""

    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "environment": config.environment.value,
        }

        # 添加额外的字段
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id
        if hasattr(record, "method"):
            log_data["method"] = record.method
        if hasattr(record, "path"):
            log_data["path"] = record.path
        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms

        return json.dumps(log_data, ensure_ascii=False)


# 配置日志记录器
logger = logging.getLogger("code-sentinel")
logger.setLevel(getattr(logging, config.log_level))

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, config.log_level))
console_handler.setFormatter(JSONFormatter())

# 添加处理器到日志记录器
logger.addHandler(console_handler)

app = FastAPI(
    title=config.api_title,
    version=config.api_version,
    description="""
    ## Code-Sentinel API
    
    模拟 AI Agent 代码审查 API，用于接收代码提交并返回模拟的代码质量问题检测结果。
    
    ### 功能特性
    
    - ✅ RESTful API 设计
    - ✅ 自动数据验证
    - ✅ 结构化日志记录
    - ✅ 多环境支持（Dev/Stage/Prd）
    - ✅ CORS 跨域支持
    
    ### 使用说明
    
    1. 使用 `POST /api/review` 端点提交代码
    2. API 返回检测到的代码坏味道列表
    3. 每个坏味道包含类型、严重程度、位置和修复建议
    
    ### 注意事项
    
    这是一个模拟 API，返回固定的模拟数据用于开发和测试。
    在实际生产环境中，应集成真实的 AI 模型进行代码分析。
    """,
    contact={
        "name": "Code-Sentinel Team",
        "url": "https://github.com/your-org/code-sentinel",
    },
    license_info={
        "name": "MIT",
    },
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=config.cors_credentials,
    allow_methods=config.cors_methods,
    allow_headers=config.cors_headers,
)


# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """记录所有 HTTP 请求和响应"""
    request_id = str(time.time())
    start_time = time.time()

    # 记录请求
    logger.info(
        f"Request started: {request.method} {request.url.path}",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
        },
    )

    # 处理请求
    response = await call_next(request)

    # 计算处理时间
    duration_ms = (time.time() - start_time) * 1000

    # 记录响应
    logger.info(
        f"Request completed: {request.method} {request.url.path}",
        extra={
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "status_code": response.status_code,
            "duration_ms": round(duration_ms, 2),
        },
    )

    return response


class CodeReviewRequest(BaseModel):
    """
    代码审查请求模型

    用于提交待审查的代码。
    """

    code: str = Field(
        ...,
        min_length=1,
        max_length=config.max_code_length,
        description="待审查的代码文本，不能为空，最大长度 100,000 字符",
        examples=["def hello():\n    print('Hello, World!')"],
    )
    language: str = Field(
        default="python",
        description="编程语言标识",
        examples=["python", "javascript", "java", "go"],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"code": "def calculate(x, y):\n    return x + y", "language": "python"}
            ]
        }
    }


class CodeSmell(BaseModel):
    """
    代码坏味道模型

    表示检测到的单个代码质量问题。
    """

    type: str = Field(
        ...,
        min_length=3,
        description="坏味道类型，最小长度 3 字符",
        examples=["Long Method", "Magic Number", "Duplicate Code"],
    )
    severity: str = Field(
        ...,
        pattern="^(low|medium|high)$",
        description="严重程度，允许值: low, medium, high",
        examples=["low", "medium", "high"],
    )
    line: int = Field(
        ..., gt=0, description="问题所在行号，必须大于 0", examples=[10, 15, 25]
    )
    message: str = Field(
        ...,
        min_length=5,
        description="问题描述，最小长度 5 字符",
        examples=["方法过长，建议拆分"],
    )
    suggestion: str = Field(
        ...,
        min_length=10,
        description="修复建议，最小长度 10 字符",
        examples=["将此方法拆分为多个小方法，每个方法只负责一个功能"],
    )


class CodeReviewResponse(BaseModel):
    """
    代码审查响应模型

    包含代码审查的完整结果。
    """

    status: str = Field(description="处理状态", examples=["success"])
    smells: list[CodeSmell] = Field(
        ..., min_length=1, description="检测到的代码坏味道列表，最小长度 1"
    )
    summary: str = Field(
        ...,
        min_length=10,
        description="分析摘要，最小长度 10 字符",
        examples=["分析了 150 个字符的 python 代码，发现 3 个潜在问题"],
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "success",
                    "smells": [
                        {
                            "type": "Long Method",
                            "severity": "medium",
                            "line": 10,
                            "message": "方法过长，建议拆分",
                            "suggestion": "将此方法拆分为多个小方法，每个方法只负责一个功能",
                        }
                    ],
                    "summary": "分析了 150 个字符的 python 代码，发现 3 个潜在问题",
                }
            ]
        }
    }


@app.get("/")
async def root():
    """
    根端点 - API 可用性检查

    返回简单的消息以确认 API 正在运行。
    用于快速检查 API 是否可访问。

    Returns:
        dict: 包含消息的 JSON 对象

    Example:
        ```json
        {
            "message": "Code-Sentinel API is running"
        }
        ```
    """
    return {"message": "Code-Sentinel API is running"}


@app.get("/health")
async def health():
    """
    健康检查端点

    用于容器健康检查、负载均衡器探测和监控系统检查。
    返回 API 的健康状态。

    Returns:
        dict: 包含健康状态的 JSON 对象

    Example:
        ```json
        {
            "status": "healthy"
        }
        ```
    """
    return {"status": "healthy"}


@app.post("/api/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    """
    代码审查端点

    接收代码提交并返回模拟的代码坏味道检测结果。
    这是一个模拟实现，返回固定的三个代码坏味道示例。

    Args:
        request (CodeReviewRequest): 代码审查请求
            - code (str): 待审查的代码文本（1-100,000 字符）
            - language (str, optional): 编程语言标识，默认为 "python"

    Returns:
        CodeReviewResponse: 代码审查结果
            - status (str): 处理状态，固定为 "success"
            - smells (list[CodeSmell]): 检测到的代码坏味道列表（固定返回 3 个）
            - summary (str): 分析摘要，包含代码字符数、语言和问题数量

    Raises:
        HTTPException: 422 - 请求数据验证失败

    Example Request:
        ```json
        {
            "code": "def hello():\\n    print('Hello, World!')",
            "language": "python"
        }
        ```

    Example Response:
        ```json
        {
            "status": "success",
            "smells": [
                {
                    "type": "Long Method",
                    "severity": "medium",
                    "line": 10,
                    "message": "方法过长，建议拆分",
                    "suggestion": "将此方法拆分为多个小方法，每个方法只负责一个功能"
                },
                {
                    "type": "Magic Number",
                    "severity": "low",
                    "line": 15,
                    "message": "发现魔法数字",
                    "suggestion": "将硬编码的数字提取为常量"
                },
                {
                    "type": "Duplicate Code",
                    "severity": "high",
                    "line": 25,
                    "message": "发现重复代码",
                    "suggestion": "提取重复代码到公共方法中"
                }
            ],
            "summary": "分析了 42 个字符的 python 代码，发现 3 个潜在问题"
        }
        ```

    Note:
        这是一个模拟 API，返回固定的模拟数据。
        在实际生产环境中，应集成真实的 AI 模型进行代码分析。
    """

    # 记录代码审查请求
    logger.info(
        f"Code review requested for {request.language} code",
        extra={
            "language": request.language,
            "code_length": len(request.code),
        },
    )

    # 模拟返回一些常见的 code smells
    mock_smells = [
        CodeSmell(
            type="Long Method",
            severity="medium",
            line=10,
            message="方法过长，建议拆分",
            suggestion="将此方法拆分为多个小方法，每个方法只负责一个功能",
        ),
        CodeSmell(
            type="Magic Number",
            severity="low",
            line=15,
            message="发现魔法数字",
            suggestion="将硬编码的数字提取为常量",
        ),
        CodeSmell(
            type="Duplicate Code",
            severity="high",
            line=25,
            message="发现重复代码",
            suggestion="提取重复代码到公共方法中",
        ),
    ]

    response = CodeReviewResponse(
        status="success",
        smells=mock_smells,
        summary=f"分析了 {len(request.code)} 个字符的 {request.language} 代码，发现 {len(mock_smells)} 个潜在问题",
    )

    # 记录代码审查结果
    logger.info(
        f"Code review completed: found {len(mock_smells)} issues",
        extra={
            "language": request.language,
            "smells_count": len(mock_smells),
        },
    )

    return response


if __name__ == "__main__":
    import uvicorn

    # 记录启动信息
    logger.info(
        f"Starting Code-Sentinel API in {config.environment.value} environment",
        extra={
            "environment": config.environment.value,
            "host": config.api_host,
            "port": config.api_port,
        },
    )

    uvicorn.run(app, host=config.api_host, port=config.api_port)
