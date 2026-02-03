# Code-Sentinel API

模拟 AI Agent 代码审查 API - 基于 FastAPI 构建的 RESTful API，用于接收代码提交并返回模拟的代码质量问题检测结果。

## 📋 目录

- [功能特性](#功能特性)
- [技术栈](#技术栈)
- [快速开始](#快速开始)
- [API 端点](#api-端点)
- [环境配置](#环境配置)
- [开发指南](#开发指南)
- [测试](#测试)
- [部署](#部署)

## ✨ 功能特性

- ✅ RESTful API 设计
- ✅ 自动数据验证（Pydantic）
- ✅ 结构化日志记录（JSON 格式）
- ✅ 多环境支持（Dev/Stage/Prd）
- ✅ CORS 跨域支持
- ✅ 自动 API 文档（OpenAPI/Swagger）
- ✅ 完整的单元测试和属性测试
- ✅ 高测试覆盖率（98%+）

## 🛠 技术栈

- **语言**: Python 3.11+
- **框架**: FastAPI 0.115.0
- **ASGI 服务器**: Uvicorn
- **数据验证**: Pydantic v2
- **包管理器**: uv（根据项目约束）
- **测试框架**: pytest + Hypothesis（属性测试）

## 🚀 快速开始

### 前置要求

- Python 3.11 或更高版本
- uv 包管理器

### 安装 uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 安装依赖

```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# 安装依赖
uv pip install -r requirements.txt
```

### 运行应用

```bash
# 使用 uv 运行
uv run python main.py

# 或者激活虚拟环境后运行
python main.py
```

应用将在 `http://0.0.0.0:8000` 启动。

### 访问 API 文档

启动应用后，访问以下 URL：

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

## 📡 API 端点

### 1. 根端点

**GET /**

检查 API 是否运行。

**响应示例**:
```json
{
  "message": "Code-Sentinel API is running"
}
```

### 2. 健康检查

**GET /health**

用于容器健康检查和负载均衡器探测。

**响应示例**:
```json
{
  "status": "healthy"
}
```

### 3. 代码审查

**POST /api/review**

提交代码进行审查，返回检测到的代码坏味道。

**请求体**:
```json
{
  "code": "def hello():\n    print('Hello, World!')",
  "language": "python"
}
```

**字段说明**:
- `code` (string, 必需): 待审查的代码文本
  - 最小长度: 1 字符
  - 最大长度: 100,000 字符
- `language` (string, 可选): 编程语言标识
  - 默认值: "python"
  - 示例: "python", "javascript", "java", "go"

**响应示例**:
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

**错误响应**:

- **422 Unprocessable Entity**: 请求数据验证失败
```json
{
  "detail": [
    {
      "loc": ["body", "code"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## ⚙️ 环境配置

应用支持三个环境：**Dev**、**Stage**、**Prd**。

### 环境变量

| 变量名 | 说明 | 默认值 | 示例 |
|--------|------|--------|------|
| `ENVIRONMENT` | 运行环境 | `dev` | `dev`, `stage`, `prd` |
| `API_HOST` | API 主机地址 | `0.0.0.0` | `127.0.0.1` |
| `API_PORT` | API 端口 | `8000` | `9000` |

### 环境差异

#### Dev 环境
- CORS: 允许所有来源 (`*`)
- 日志级别: `DEBUG`
- 用途: 本地开发

#### Stage 环境
- CORS: 允许特定域名（stage.code-sentinel.com, localhost:3000）
- 日志级别: `INFO`
- 用途: 预发布测试

#### Prd 环境
- CORS: 仅允许生产域名（code-sentinel.com）
- 日志级别: `WARNING`
- 用途: 生产环境

### 设置环境

```bash
# 设置为 stage 环境
export ENVIRONMENT=stage

# 设置自定义端口
export API_PORT=9000

# 运行应用
uv run python main.py
```

## 💻 开发指南

### 项目结构

```
apps/api/
├── main.py              # FastAPI 应用主文件
├── config.py            # 环境配置模块
├── requirements.txt     # Python 依赖
├── pytest.ini          # pytest 配置
├── README.md           # 本文档
└── tests/              # 测试目录
    ├── conftest.py     # pytest 配置和 fixtures
    ├── test_*.py       # 测试文件
    └── ...
```

### 添加新依赖

```bash
# 安装新包
uv pip install <package-name>

# 更新 requirements.txt
uv pip freeze > requirements.txt
```

### 代码风格

项目遵循 PEP 8 代码风格规范。

### 日志记录

应用使用结构化日志（JSON 格式），自动记录：
- 请求开始和完成
- HTTP 方法和路径
- 响应状态码
- 请求处理时间
- 环境信息

日志示例：
```json
{
  "timestamp": "2024-01-15 10:30:45,123",
  "level": "INFO",
  "logger": "code-sentinel",
  "message": "Request completed: POST /api/review",
  "environment": "dev",
  "request_id": "1705315845.123",
  "method": "POST",
  "path": "/api/review",
  "status_code": 200,
  "duration_ms": 15.42
}
```

## 🧪 测试

### 运行所有测试

```bash
# 运行所有测试
uv run pytest

# 运行测试并显示详细输出
uv run pytest -v

# 运行测试并生成覆盖率报告
uv run pytest --cov=. --cov-report=html
```

### 运行特定测试

```bash
# 运行特定测试文件
uv run pytest tests/test_app_config.py

# 运行特定测试类
uv run pytest tests/test_app_config.py::TestFastAPIAppConfiguration

# 运行特定测试函数
uv run pytest tests/test_app_config.py::TestFastAPIAppConfiguration::test_app_title_is_code_sentinel_api
```

### 测试覆盖率

项目维持 98%+ 的测试覆盖率。查看覆盖率报告：

```bash
# 生成 HTML 覆盖率报告
uv run pytest --cov=. --cov-report=html

# 在浏览器中打开报告
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### 测试类型

项目使用双重测试策略：

1. **单元测试**: 验证特定示例和边缘情况
2. **属性测试**: 使用 Hypothesis 验证通用属性

## 🐳 部署

### Docker 部署

创建 `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装 uv
RUN pip install uv

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN uv pip install --system -r requirements.txt

# 复制应用代码
COPY . .

# 暴露端口
EXPOSE 8000

# 设置环境变量
ENV ENVIRONMENT=prd

# 运行应用
CMD ["python", "main.py"]
```

构建和运行：

```bash
# 构建镜像
docker build -t code-sentinel-api .

# 运行容器
docker run -p 8000:8000 -e ENVIRONMENT=prd code-sentinel-api
```

### AWS 部署

根据项目约束，应用将部署到 AWS。推荐使用：

- **ECS (Elastic Container Service)**: 容器编排
- **ECR (Elastic Container Registry)**: 镜像存储
- **ALB (Application Load Balancer)**: 负载均衡
- **CloudWatch**: 日志和监控

部署流程将通过 Terraform（IaC）和 GitHub Actions（CI/CD）自动化。

## 📊 监控和可观测性

### 日志

- 格式: JSON 结构化日志
- 输出: stdout（容器环境）
- 聚合: CloudWatch Logs（AWS）

### 指标

关键指标：
- 请求数量
- 响应时间
- 错误率
- 代码审查请求数

### 健康检查

使用 `/health` 端点进行：
- 容器健康检查
- 负载均衡器健康探测
- 监控系统检查

## 🔒 安全

- ✅ 输入验证（Pydantic）
- ✅ CORS 配置（环境特定）
- ✅ 依赖扫描（CI/CD）
- ✅ 环境变量管理
- ✅ 最小权限原则

## 📝 许可证

本项目用于学习目的。

## 🤝 贡献

这是一个学习项目，用于掌握：
1. AI Agent 开发实现
2. FastAPI 最佳实践
3. 测试驱动开发（TDD）
4. 属性测试（Property-Based Testing）
5. DevOps 和 CI/CD
6. 云原生部署

## 📞 联系

如有问题或建议，请提交 Issue。

---

**注意**: 这是一个模拟 API，返回固定的模拟数据。在实际生产环境中，应集成真实的 AI 模型进行代码分析。
