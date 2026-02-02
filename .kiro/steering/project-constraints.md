# 项目约束与规范

本文档定义了 Code-Sentinel 学习项目的技术约束和开发规范。

## 项目结构

```
.
├── apps/
│   ├── web/          # 前端 - Next.js 16 应用
│   └── api/          # 后端 - Python FastAPI
├── packages/
│   └── types/        # 共享 TypeScript 类型定义
└── data/
    └── golden_set/   # Agent 黄金评测集
```

## 技术栈约束

### 前端技术栈
- **框架**: Next.js 16（必须使用此版本）
- **包管理器**: Bun（禁止使用 npm、yarn、pnpm）
- **语言**: TypeScript
- **部署平台**: Vercel

### 后端技术栈
- **语言**: Python
- **框架**: FastAPI
- **包管理器**: uv（禁止使用 pip、poetry、pipenv）
- **部署方式**: Docker 容器
- **部署平台**: AWS

### 共享代码
- **类型定义**: TypeScript（存放在 `packages/types/`）
- 前后端共享的接口定义必须放在此目录

## 包管理器使用规范

### 前端 (Bun)
```bash
# 安装依赖
bun install

# 开发服务器
bun dev

# 构建
bun run build

# 添加依赖
bun add <package>
```

### 后端 (uv)
```bash
# 创建虚拟环境
uv venv

# 激活虚拟环境
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows

# 安装依赖
uv pip install -r requirements.txt

# 运行应用
uv run main.py

# 添加依赖
uv pip install <package>
uv pip freeze > requirements.txt
```

## 环境隔离

项目必须支持三个独立环境：
- **Dev**: 开发环境
- **Stage**: 预发布环境
- **Prd**: 生产环境

每个环境应有独立的配置和资源。

## 基础设施即代码 (IaC)

- 使用 **Terraform** 管理所有云基础设施
- 所有基础设施配置必须代码化
- 禁止手动在 AWS 控制台创建资源

## CI/CD 规范

- 使用 **GitHub Actions** 进行自动化
- 必须包含以下工作流：
  - 代码检查（Linting）
  - 测试（Testing）
  - 安全扫描（Security Scanning）
  - 构建（Build）
  - 部署（Deploy）

## 安全规范 (DevSecOps)

- 所有代码提交前必须通过安全扫描
- 依赖项必须定期更新和扫描漏洞
- 敏感信息（API Keys、密码）必须使用环境变量或密钥管理服务

## Prompt 管理

- Prompt 必须版本控制
- Prompt 应配置化，不硬编码在代码中
- 使用配置文件管理不同版本的 Prompt

## 可观测性 (Observability)

生产环境必须实现：
- **日志记录**: 结构化日志
- **指标监控**: 性能和业务指标
- **链路追踪**: 分布式追踪
- **告警机制**: 异常情况及时通知

## 评测规范

- 黄金评测集存放在 `data/golden_set/`
- 评测结果必须可追踪和可复现
- 评测流程必须自动化

## 学习目标

本项目旨在学习以下内容：
1. Github 仓库的规划
2. AI Agent 的开发实现 (Python + FastAPI)
3. 黄金评测集的评测过程 (The "Evals")
4. Github Actions 工作流规划
5. Docker 部署流程 (AWS)
6. 生产环境跟踪评测 (Observability)
7. Dev，Stage，Prd 环境的隔离
8. 基础设施即代码 (IaC) - Terraform
9. Prompt 的版本控制与"配置化"
10. 安全扫描 (DevSecOps)
