# 设计文档

## 概述

本设计文档描述了模拟 AI Agent 代码审查 API 的技术实现。该 API 使用 FastAPI 框架构建，提供 RESTful 端点来接收代码提交并返回模拟的代码质量问题检测结果。

### 设计目标

1. **简单性**: 提供清晰的 API 接口，易于前端集成
2. **可扩展性**: 为未来集成真实 AI 模型预留接口
3. **性能**: 快速响应（< 500ms），适合开发和测试
4. **标准化**: 遵循 REST API 最佳实践和 FastAPI 规范

### 技术栈

- **语言**: Python 3.11+
- **框架**: FastAPI
- **数据验证**: Pydantic v2
- **ASGI 服务器**: Uvicorn
- **包管理**: uv（根据项目约束）

## 架构

### 系统架构

```
┌─────────────┐
│   前端客户端  │
│  (Next.js)  │
└──────┬──────┘
       │ HTTP/JSON
       ↓
┌─────────────────────────────┐
│      FastAPI 应用            │
│  ┌─────────────────────┐   │
│  │  CORS 中间件         │   │
│  └──────────┬──────────┘   │
│             ↓               │
│  ┌─────────────────────┐   │
│  │  路由层              │   │
│  │  - GET /            │   │
│  │  - GET /health      │   │
│  │  - POST /api/review │   │
│  └──────────┬──────────┘   │
│             ↓               │
│  ┌─────────────────────┐   │
│  │  业务逻辑层          │   │
│  │  - 请求验证          │   │
│  │  - 模拟数据生成      │   │
│  │  - 响应构建          │   │
│  └─────────────────────┘   │
└─────────────────────────────┘
```

### 分层设计

1. **中间件层**: 处理 CORS、请求日志等横切关注点
2. **路由层**: 定义 API 端点和请求映射
3. **业务逻辑层**: 实现核心功能（当前为模拟数据生成）
4. **数据模型层**: 使用 Pydantic 定义请求/响应结构

## 组件和接口

### 核心组件

#### 1. FastAPI 应用实例

```python
app = FastAPI(
    title="Code-Sentinel API",
    version="1.0.0",
    description="模拟 AI Agent 代码审查 API"
)
```

**职责**:
- 应用程序生命周期管理
- 路由注册
- 中间件配置

#### 2. CORS 中间件

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**职责**:
- 处理跨域请求
- 允许前端（Next.js）访问 API

**配置说明**:
- `allow_origins=["*"]`: 开发环境允许所有来源（生产环境应限制为特定域名）
- `allow_credentials=True`: 允许携带凭证
- `allow_methods=["*"]`: 允许所有 HTTP 方法
- `allow_headers=["*"]`: 允许所有请求头

#### 3. 路由处理器

##### 根端点 (GET /)

```python
@app.get("/")
async def root():
    return {"message": "Code-Sentinel API is running"}
```

**用途**: API 可用性检查
**响应时间**: < 100ms

##### 健康检查端点 (GET /health)

```python
@app.get("/health")
async def health():
    return {"status": "healthy"}
```

**用途**: 容器健康检查、负载均衡器探测
**响应时间**: < 100ms

##### 代码审查端点 (POST /api/review)

```python
@app.post("/api/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    # 业务逻辑
    pass
```

**用途**: 接收代码并返回审查结果
**响应时间**: < 500ms
**验证**: 自动通过 Pydantic 模型验证

#### 4. 模拟数据生成器

**职责**: 生成固定的模拟代码坏味道数据

**实现策略**:
- 返回三个预定义的 Code Smell 对象
- 每个对象包含不同的严重程度和类型
- 生成包含输入统计信息的摘要

**模拟数据规格**:
```python
mock_smells = [
    CodeSmell(
        type="Long Method",
        severity="medium",
        line=10,
        message="方法过长，建议拆分",
        suggestion="将此方法拆分为多个小方法，每个方法只负责一个功能"
    ),
    CodeSmell(
        type="Magic Number",
        severity="low",
        line=15,
        message="发现魔法数字",
        suggestion="将硬编码的数字提取为常量"
    ),
    CodeSmell(
        type="Duplicate Code",
        severity="high",
        line=25,
        message="发现重复代码",
        suggestion="提取重复代码到公共方法中"
    )
]
```

## 数据模型

### CodeReviewRequest

**用途**: 代码审查请求的输入模型

```python
class CodeReviewRequest(BaseModel):
    code: str
    language: str = "python"
```

**字段说明**:
- `code` (str, 必需): 待审查的代码文本
  - 最大长度: 100,000 字符
  - 不能为空字符串
- `language` (str, 可选): 编程语言标识
  - 默认值: "python"
  - 示例: "python", "javascript", "java", "go"

**验证规则**:
- Pydantic 自动验证类型
- FastAPI 自动返回 422 错误（验证失败时）

### CodeSmell

**用途**: 单个代码坏味道的数据结构

```python
class CodeSmell(BaseModel):
    type: str
    severity: str
    line: int
    message: str
    suggestion: str
```

**字段说明**:
- `type` (str): 坏味道类型
  - 最小长度: 3 字符
  - 示例: "Long Method", "Magic Number", "Duplicate Code"
- `severity` (str): 严重程度
  - 允许值: "low", "medium", "high"
- `line` (int): 问题所在行号
  - 必须 > 0
- `message` (str): 问题描述
  - 最小长度: 5 字符
- `suggestion` (str): 修复建议
  - 最小长度: 10 字符

### CodeReviewResponse

**用途**: 代码审查结果的输出模型

```python
class CodeReviewResponse(BaseModel):
    status: str
    smells: list[CodeSmell]
    summary: str
```

**字段说明**:
- `status` (str): 处理状态
  - 固定值: "success"（当前实现）
- `smells` (list[CodeSmell]): 检测到的代码坏味道列表
  - 最小长度: 1
  - 当前实现: 固定返回 3 个元素
- `summary` (str): 分析摘要
  - 最小长度: 10 字符
  - 格式: "分析了 {字符数} 个字符的 {语言} 代码，发现 {数量} 个潜在问题"

**示例响应**:
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
  "summary": "分析了 150 个字符的 python 代码，发现 3 个潜在问题"
}
```


## 正确性属性

*属性是一个特征或行为，应该在系统的所有有效执行中保持为真——本质上是关于系统应该做什么的形式化陈述。属性充当人类可读规范和机器可验证正确性保证之间的桥梁。*

### 属性 1: API 配置正确性

*对于* API 应用实例，它应该具有标题 "Code-Sentinel API" 和版本 "1.0.0"，并且应该配置 CORS 中间件允许所有来源

**验证需求: 1.1, 1.2**

### 属性 2: 健康检查端点可访问性

*对于* 根路径 "/" 和健康检查路径 "/health" 的 GET 请求，API 应该返回 HTTP 状态码 200 和预期的 JSON 响应结构

**验证需求: 2.1, 2.2, 2.3, 2.4**

### 属性 3: 输入验证拒绝无效请求

*对于任何* 无效的 Code_Review_Request（缺少必需字段、类型错误、超长代码），API 应该返回 HTTP 状态码 422 和详细的验证错误信息

**验证需求: 3.2, 3.4, 7.3**

### 属性 4: 默认语言值应用

*对于任何* 不包含 "language" 字段的 Code_Review_Request，API 应该将语言默认设置为 "python"

**验证需求: 3.3**

### 属性 5: 有效请求返回成功响应

*对于任何* 有效的 Code_Review_Request，API 应该返回 HTTP 状态码 200 和包含 status="success" 的 Code_Review_Response

**验证需求: 4.1, 4.2**

### 属性 6: 响应结构完整性

*对于任何* 成功的代码审查响应，它应该包含恰好 3 个 Code_Smell 对象的 smells 列表，以及长度至少为 10 个字符的 summary 字段

**验证需求: 4.3, 4.4, 4.5**

### 属性 7: Code Smell 结构有效性

*对于任何* 返回的 Code_Smell 对象，它应该包含：
- type 字段（长度 ≥ 3 字符）
- severity 字段（值为 "low"、"medium" 或 "high"）
- line 字段（整数 > 0）
- message 字段（长度 ≥ 5 字符）
- suggestion 字段（长度 ≥ 10 字符）

**验证需求: 5.1, 5.2, 5.3, 5.4, 5.5**

### 属性 8: 模拟数据一致性

*对于任何* Code_Review_Request，返回的三个 Code_Smell 对象应该始终是：
1. Long Method (severity="medium", line=10)
2. Magic Number (severity="low", line=15)
3. Duplicate Code (severity="high", line=25)

**验证需求: 6.1, 6.2, 6.3**

### 属性 9: Summary 字段准确性

*对于任何* Code_Review_Request，返回的 summary 字段应该准确包含：
- 提交代码的精确字符数
- 请求中的编程语言名称
- 检测到的坏味道数量（3 个）

**验证需求: 6.4, 6.5, 6.6**

## 错误处理

### 验证错误

**场景**: 客户端发送无效的请求数据

**处理策略**:
1. FastAPI 自动捕获 Pydantic 验证错误
2. 返回 HTTP 422 Unprocessable Entity
3. 响应体包含详细的验证错误信息

**错误响应格式**:
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

### 服务器错误

**场景**: 内部处理异常

**处理策略**:
1. FastAPI 自动捕获未处理的异常
2. 返回 HTTP 500 Internal Server Error
3. 生产环境不暴露详细错误信息

**当前实现**: 由于是简单的模拟逻辑，不太可能出现运行时错误

### CORS 错误

**场景**: 浏览器阻止跨域请求

**处理策略**:
1. CORS 中间件自动处理预检请求（OPTIONS）
2. 在响应头中添加适当的 CORS 标头
3. 允许所有来源（开发环境）

## 测试策略

### 测试方法

本项目采用**双重测试方法**：

1. **单元测试**: 验证特定示例、边缘情况和错误条件
2. **属性测试**: 验证跨所有输入的通用属性

两者是互补的，对于全面覆盖都是必要的。

### 单元测试重点

单元测试应该专注于：
- **特定示例**: 演示正确行为的具体案例
- **集成点**: 组件之间的集成
- **边缘情况**: 空字符串、超长输入等
- **错误条件**: 验证错误、异常处理

**避免过多单元测试** - 属性测试通过随机化处理大量输入覆盖

### 属性测试配置

**测试库**: pytest + Hypothesis (Python 的属性测试库)

**配置要求**:
- 每个属性测试最少 100 次迭代（由于随机化）
- 每个属性测试必须引用其设计文档属性
- 标签格式: **Feature: mock-agent-api, Property {number}: {property_text}**

**示例属性测试结构**:
```python
from hypothesis import given, strategies as st
import pytest

# Feature: mock-agent-api, Property 3: 输入验证拒绝无效请求
@given(
    code=st.one_of(
        st.none(),  # 缺少字段
        st.integers(),  # 错误类型
        st.text(min_size=100001)  # 超长
    )
)
def test_invalid_requests_return_422(code):
    # 测试逻辑
    pass
```

### 测试覆盖范围

**必须测试的场景**:

1. **API 配置** (属性 1)
   - 单元测试: 验证 FastAPI 应用配置
   - 单元测试: 验证 CORS 中间件存在

2. **端点可访问性** (属性 2)
   - 单元测试: GET / 返回正确消息
   - 单元测试: GET /health 返回健康状态

3. **输入验证** (属性 3, 4)
   - 属性测试: 各种无效输入都返回 422
   - 单元测试: 空字符串边缘情况
   - 单元测试: 默认语言值应用

4. **成功响应** (属性 5, 6)
   - 属性测试: 任何有效输入返回 200 和正确结构
   - 单元测试: 具体的有效请求示例

5. **数据结构** (属性 7, 8, 9)
   - 属性测试: 所有 Code_Smell 对象符合结构要求
   - 属性测试: 模拟数据一致性
   - 属性测试: Summary 字段准确性
   - 单元测试: 验证具体的模拟数据值

### 测试工具

- **测试框架**: pytest
- **属性测试**: Hypothesis
- **HTTP 测试**: FastAPI TestClient
- **覆盖率**: pytest-cov

### CI/CD 集成

根据项目约束，测试应该集成到 GitHub Actions 工作流中：

```yaml
- name: Run tests
  run: |
    uv pip install pytest pytest-cov hypothesis
    uv run pytest tests/ --cov=apps/api --cov-report=xml
```

### 性能测试

虽然需求中指定了响应时间（100ms/500ms），但这些更适合：
- 负载测试（使用 Locust 或 k6）
- 性能监控（生产环境）
- 而非单元测试或属性测试

性能测试应该在独立的测试套件中进行。
