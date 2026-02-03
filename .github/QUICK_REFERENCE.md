# GitHub Actions 快速参考

## 🚀 常用命令

### 本地开发

```bash
# API
cd apps/api
make install          # 安装依赖
make dev             # 运行开发服务器
make test-local      # 运行测试
make lint            # 代码检查
make build           # 构建 Docker 镜像
make run             # 运行 Docker 容器
```

### Git 工作流

```bash
# 创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/my-feature

# 提交代码
git add .
git commit -m "feat: add new feature"
git push origin feature/my-feature

# 创建 PR (使用 GitHub CLI)
gh pr create --base develop --title "feat: add new feature"

# 合并到 develop
gh pr merge --merge

# 发布到 main
git checkout main
git merge develop
git push origin main
```

## 📋 Workflows 触发条件

| Workflow | 触发分支 | 触发路径 | 运行内容 |
|----------|----------|----------|----------|
| API CI | main, develop, feature/** | apps/api/** | Lint + Test + Security + Build |
| Dependabot | - | - | 自动合并 patch/minor 更新 |

## 🔍 检查状态

### 查看 Workflow 运行

```bash
# 列出最近的 workflow runs
gh run list

# 查看特定 run 的详情
gh run view <run-id>

# 查看 run 的日志
gh run view <run-id> --log

# 重新运行失败的 workflow
gh run rerun <run-id>
```

## 🐛 故障排查

### Workflow 失败

1. 查看日志：`gh run view <run-id> --log`
2. 本地运行测试：`make test-local`
3. 检查代码格式：`make lint`
4. 验证 Docker 构建：`make build`

### 测试失败

1. 本地运行测试：`make test-local`
2. 检查依赖版本
3. 清理缓存：`rm -rf .pytest_cache`
4. 重新安装依赖：`make install`

## 📊 监控

### 测试覆盖率
- GitHub Actions Artifacts: 下载 coverage-report

### 安全扫描
- GitHub Security: Settings > Security > Code scanning alerts

### 依赖更新
- Dependabot: Pull requests > Dependabot

## 🔄 常见任务

### 更新依赖

```bash
# API
cd apps/api
uv pip install --upgrade <package>
uv pip freeze > requirements.txt
```

### 本地测试 Docker

```bash
cd apps/api
make build           # 构建镜像
make run            # 运行容器
make logs           # 查看日志
curl http://localhost:8000/health  # 测试健康检查
make stop           # 停止容器
```

## 📚 快速链接

- [Workflows 文档](.github/workflows/README.md)
- [配置指南](.github/SETUP.md)
- [项目约束](../.kiro/steering/project-constraints.md)
- [API 文档](../apps/api/README.md)

## 💡 最佳实践

1. ✅ 小而频繁的提交
2. ✅ 有意义的 commit 消息
3. ✅ 所有测试通过后再合并
4. ✅ 代码审查
5. ✅ 定期更新依赖
6. ✅ 及时修复安全漏洞

## 🆘 获取帮助

- 查看文档：`.github/` 目录
- 创建 Issue：使用 Issue 模板
- 查看 Actions 日志

---

**提示**: 将此文件加入书签以便快速访问！
