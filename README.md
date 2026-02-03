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

## 快速开始

1. **克隆仓库**
   ```bash
   git clone https://github.com/your-org/code-sentinel.git
   cd code-sentinel
   ```

2. **设置后端**
   ```bash
   cd apps/api
   make install
   make dev
   ```

3. **设置前端**
   ```bash
   cd apps/web
   bun install
   bun dev
   ```

4. **运行测试**
   ```bash
   # API
   cd apps/api && make test-local
   
   # Web
   cd apps/web && bun test
   ```

## 文档

- [项目约束与规范](.kiro/steering/project-constraints.md)
- [GitHub Actions 配置](.github/SETUP.md)
- [API 文档](apps/api/README.md)
- [CI/CD 配置说明](docs/CI_CD_SETUP.md)

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

### 使用 Docker
```bash
cd apps/api
make build    # 构建镜像
make run      # 运行容器
make logs     # 查看日志
make stop     # 停止容器
```

### 运行测试
```bash
# API 测试
cd apps/api
make test-local

# Web 测试
cd apps/web
bun test
```

## CI/CD

项目使用 GitHub Actions 实现持续集成流程：

- ✅ 自动化测试和代码质量检查
- ✅ 安全扫描（依赖漏洞 + 代码安全）
- ✅ Docker 镜像构建和测试
- ✅ Dependabot 自动依赖更新

详细信息请查看：
- [GitHub Actions 配置指南](.github/SETUP.md)
- [Workflows 文档](.github/workflows/README.md)
- [快速参考](.github/QUICK_REFERENCE.md)

## 部署

- **前端**: 将来部署到 Vercel
- **后端**: 将来通过 Docker 容器部署到 AWS ECS

> 注：部署配置将在后续添加