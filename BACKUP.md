# 🔄 工作区自动备份指南

本目录已配置自动备份系统，可将 OpenClaw 工作区定期备份到 GitHub/GitLab。

## 📁 备份内容

以下文件会被自动备份：
- ✅ `AGENTS.md` - 代理配置
- ✅ `SOUL.md` - 核心行为准则
- ✅ `TOOLS.md` - 工具配置
- ✅ `IDENTITY.md` - 身份信息
- ✅ `USER.md` - 用户信息
- ✅ `skills/` - 自定义技能目录
- ✅ `scripts/` - 脚本文件
- ❌ 敏感凭证（已排除）
- ❌ 运行时日志（已排除）

## 🚀 快速开始

### 1. 创建远程仓库

**GitHub:**
1. 访问 https://github.com/new
2. 填写仓库名称（如 `openclaw-backup`）
3. 选择私有仓库（建议）
4. 点击创建

**GitLab:**
1. 访问 https://gitlab.com/projects/new
2. 填写项目名称
3. 选择私有项目
4. 点击创建

### 2. 生成访问令牌

**GitHub Token:**
1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 生成并复制令牌（以 `ghp_` 开头）

**GitLab Token:**
1. 访问 https://gitlab.com/-/profile/personal_access_tokens
2. 点击 "Add new token"
3. 勾选 `api` 和 `write_repository`
4. 生成并复制令牌

### 3. 配置远程仓库

运行配置脚本：

```bash
# GitHub 示例
./scripts/setup-remote.sh github https://github.com/你的用户名/openclaw-backup.git ghp_你的令牌

# GitLab 示例
./scripts/setup-remote.sh gitlab https://gitlab.com/你的用户名/openclaw-backup.git glpat-你的令牌
```

### 4. 测试备份

```bash
source .env/backup.env
./scripts/backup.sh
```

看到 "Backup completed and pushed!" 表示成功！

## ⏰ 定时任务设置

由于当前环境不支持 crontab，请使用以下方式之一：

### 方式1：OpenClaw 心跳任务（推荐）

已配置在 `HEARTBEAT.md` 中，每次心跳检查时会自动运行备份。

### 方式2：手动执行脚本

```bash
# 手动运行备份
./scripts/backup.sh
```

### 方式3：添加到系统定时任务（如果有权限）

```bash
# 编辑 crontab
crontab -e

# 添加以下行（每天凌晨2点备份）
0 2 * * * /workspace/projects/workspace/scripts/backup.sh >> /workspace/projects/workspace/.backup.log 2>&1
```

## 📝 查看备份日志

```bash
cat .backup.log
```

## 🔒 安全提示

1. **令牌安全**: 访问令牌相当于密码，不要分享给他人
2. **私有仓库**: 建议将备份仓库设为私有
3. **定期更换**: 建议定期更换访问令牌
4. **本地存储**: 令牌存储在 `.env/backup.env`，已添加到 `.gitignore`

## 🆘 故障排除

### 问题：推送失败

**解决：**
```bash
# 检查远程配置
git remote -v

# 重新配置
./scripts/setup-remote.sh github https://github.com/用户名/仓库.git 令牌
```

### 问题：没有权限

**解决：**
- 检查令牌是否正确
- 确认令牌有 `repo` (GitHub) 或 `write_repository` (GitLab) 权限
- 确认仓库存在且可访问

### 问题：网络错误

**解决：**
- 检查网络连接
- 如果使用代理，配置 git 代理：
```bash
git config --global http.proxy http://代理地址:端口
```

## 📊 备份状态

查看当前备份状态：
```bash
git status
git log --oneline -5
```

---

**最后更新**: 2026-02-28
**备份脚本**: `./scripts/backup.sh`
