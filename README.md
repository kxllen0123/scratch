# Code-Sentinel - 学习项目

此存储库是一个综合性学习项目，通过构建 Code-Sentinel 代码审查系统来实践现代软件工程的完整流程。

## 学习目标

1. **Github 仓库的规划** - Monorepo 结构、分支策略、代码组织
2. **AI Agent 的开发实现** - Python + FastAPI 构建智能代理
3. **黄金评测集的评测过程** - The "Evals" 评测方法论
4. **Github Actions 工作流规划** - CI/CD 自动化流程
5. **Docker 部署流程** - 容器化与 AWS 部署
6. **生产环境跟踪评测** - Observability 可观测性实践
7. **Dev，Stage，Prd 环境的隔离** - 多环境管理策略
8. **基础设施即代码 (IaC)** - Terraform 实践
9. **Prompt 的版本控制与"配置化"** - Prompt 工程管理
10. **安全扫描 (DevSecOps)** - 安全最佳实践

## 项目结构

```
.
├── apps/
│   ├── web/          # 前端 - Next.js 16 应用
│   └── api/          # 后端 - Python API
├── packages/
│   └── types/        # 共享 TypeScript 类型定义
└── data/
    └── golden_set/   # Agent 黄金评测集
```

## 技术栈

### 前端
- **框架**: Next.js 16
- **包管理器**: Bun
- **部署**: Vercel

### 后端
- **语言**: Python
- **框架**: FastAPI
- **包管理器**: uv
- **部署**: Docker + AWS

### 共享
- **类型定义**: TypeScript

## 开发指南

### 前端开发
```bash
cd apps/web
bun install
bun dev
```

### 后端开发
```bash
cd apps/api
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
uv run main.py
```

## 部署

- **前端**: 自动部署到 Vercel
- **后端**: 通过 Docker 容器部署到 AWS