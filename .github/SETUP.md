# GitHub Actions 配置指南

本文档提供了配置 Code-Sentinel 项目 GitHub Actions 的完整指南。

## 📋 目录

1. [前置要求](#前置要求)
2. [启用 Dependabot](#启用-dependabot)
3. [配置分支保护](#配置分支保护)
4. [验证配置](#验证配置)

## 前置要求

在开始之前，请确保你有：

- [x] GitHub 仓库的管理员权限

## 启用 Dependabot

Dependabot 配置文件已创建在 `.github/dependabot.yml`。

### 启用 Dependabot Alerts

1. 进入 `Settings` > `Code security and analysis`
2. 启用以下选项：
   - `Dependabot alerts`
   - `Dependabot security updates`
   - `Dependabot version updates`

### 配置 Auto-merge

1. 进入 `Settings` > `Actions` > `General`
2. 在 `Workflow permissions` 中选择：
   - `Read and write permissions`
3. 勾选 `Allow GitHub Actions to create and approve pull requests`

## 配置分支保护

### Main 分支保护

1. 进入 `Settings` > `Branches`
2. 点击 `Add rule`
3. 在 `Branch name pattern` 中输入 `main`
4. 启用以下规则：
   - ✅ `Require a pull request before merging`
     - ✅ `Require approvals` (至少 1 个)
     - ✅ `Dismiss stale pull request approvals when new commits are pushed`
   - ✅ `Require status checks to pass before merging`
     - 添加必需的检查：
       - `Lint & Code Quality`
       - `Test`
       - `Security Scan`
       - `Build Docker Image`
   - ✅ `Require conversation resolution before merging`
   - ✅ `Include administrators`
5. 点击 `Create` 保存规则

### Develop 分支保护

重复上述步骤，但对 `develop` 分支：
- 可以降低审查要求（例如：0 个审查者）
- 保持状态检查要求

## 验证配置

### 步骤 1: 测试 Workflows

1. 创建一个测试分支：
   ```bash
   git checkout -b test/github-actions
   ```

2. 做一个小改动并推送：
   ```bash
   echo "# Test" >> README.md
   git add README.md
   git commit -m "test: verify GitHub Actions"
   git push origin test/github-actions
   ```

3. 检查 Actions 标签页，确认 workflows 运行

### 步骤 2: 验证测试

在 workflow 运行日志中，确认：
- ✅ Lint 检查通过
- ✅ 所有测试通过
- ✅ 安全扫描完成
- ✅ Docker 镜像构建成功

### 步骤 3: 测试 Dependabot

1. 等待 Dependabot 创建第一个 PR（通常在启用后几分钟内）
2. 验证 PR 自动创建
3. 检查 auto-merge 是否工作（对于 patch/minor 更新）

## 常见问题

### Q: Workflow 失败，提示 "Resource not accessible by integration"

**A:** 检查 Actions 权限设置：
1. `Settings` > `Actions` > `General`
2. 确保 `Workflow permissions` 设置为 `Read and write permissions`

### Q: 测试失败

**A:** 验证：
1. 本地运行测试是否通过
2. 依赖是否正确安装
3. Python 版本是否匹配 (3.11)

### Q: Dependabot PR 没有自动合并

**A:** 检查：
1. Auto-merge workflow 是否启用
2. PR 是否通过了所有状态检查
3. 更新类型是否为 patch 或 minor（major 需要手动审查）

## 下一步

配置完成后，你可以：

1. ✅ 开始使用 feature 分支进行开发
2. ✅ 创建 PR 并观察自动化测试
3. ✅ 合并到 develop 或 main
4. ✅ 监控 Dependabot 的依赖更新

## 未来配置

当准备部署时，需要配置：
- [ ] AWS credentials (API 部署)
- [ ] Vercel tokens (Web 部署)
- [ ] GitHub Environments (Dev/Stage/Prod)
- [ ] 部署 workflows

## 相关文档

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Dependabot 配置](https://docs.github.com/en/code-security/dependabot)
- [Workflows 说明](.github/workflows/README.md)

## 支持

如果遇到问题，请：
1. 查看 [Workflows README](.github/workflows/README.md)
2. 检查 Actions 运行日志
3. 创建 Issue 寻求帮助
