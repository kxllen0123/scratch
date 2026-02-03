# GitHub Actions Workflows

本目录包含 Code-Sentinel 项目的 CI/CD 工作流配置。

## 工作流概览

### 1. API CI (`api-ci.yml`)

后端 Python FastAPI 应用的持续集成流程。

**触发条件**：
- Push 到 `main`、`develop` 或 `feature/**` 分支
- Pull Request 到 `main` 或 `develop` 分支
- 仅当 `apps/api/**` 路径下的文件发生变化时触发

**工作流程**：

1. **Lint & Code Quality** - 代码质量检查
   - 使用 Ruff 进行代码检查和格式化验证

2. **Test** - 测试
   - 运行 pytest 测试套件
   - 生成代码覆盖率报告
   - 上传覆盖率报告为 artifact

3. **Security Scan** - 安全扫描
   - Safety: 检查依赖项漏洞
   - Bandit: 检查代码安全问题

4. **Build** - 构建 Docker 镜像
   - 构建并测试 Docker 镜像
   - 验证健康检查端点

### 2. Dependabot Auto-merge (`dependabot-auto-merge.yml`)

自动合并 Dependabot 创建的依赖更新 PR。

**触发条件**：
- Dependabot 创建的 Pull Request

**行为**：
- 自动合并 patch 和 minor 版本更新
- major 版本更新需要手动审查

## 必需的 GitHub Secrets

目前不需要配置任何 secrets，所有 jobs 都在 GitHub Actions 环境中运行。

未来部署时需要的 secrets（暂未启用）：
- AWS credentials (用于 API 部署)
- Vercel tokens (用于 Web 部署)

## 分支策略

```
main (生产)
  ├── develop (开发)
  │   ├── feature/xxx (功能分支)
  │   ├── feature/yyy
  │   └── ...
  └── hotfix/xxx (紧急修复)
```

**工作流程**：

1. 从 `develop` 创建 `feature/*` 分支进行开发
2. 完成后创建 PR 合并到 `develop`
3. CI 自动运行测试和检查
4. 测试通过后，合并 PR
5. 准备发布时，从 `develop` 合并到 `main`

## 本地测试

### API

```bash
cd apps/api

# 安装依赖
make install

# 运行 lint
make lint

# 运行测试
make test-local

# 构建 Docker 镜像
make build

# 运行 Docker 容器
make run
```

## 监控和日志

- **测试覆盖率**: 查看 Actions 中的 artifacts
- **安全扫描**: 查看 GitHub Security 标签页
- **CI 状态**: 查看 Actions 标签页
- **依赖更新**: 查看 Dependabot 标签页

## 故障排查

### Workflow 失败

1. 查看 Actions 标签页中的失败日志
2. 验证代码是否通过本地测试
3. 检查是否有语法错误或测试失败

### 安全扫描警告

1. 查看安全扫描报告
2. 更新有漏洞的依赖项
3. 如果是误报，可以在配置中添加忽略规则

## 最佳实践

1. **小而频繁的提交**: 保持 PR 小而专注
2. **测试先行**: 确保所有测试通过后再合并
3. **代码审查**: 所有 PR 都应经过代码审查
4. **安全第一**: 定期更新依赖项，修复安全漏洞
5. **本地验证**: 提交前在本地运行测试和 lint

## 未来计划

以下功能将在后续添加：
- [ ] 部署到 AWS (API)
- [ ] 部署到 Vercel (Web)
- [ ] Web 前端 CI/CD
- [ ] 代码覆盖率上传到 Codecov
- [ ] 环境配置 (Dev/Stage/Prod)

## 相关文档

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Dependabot 文档](https://docs.github.com/en/code-security/dependabot)
- [项目约束](../../.kiro/steering/project-constraints.md)
