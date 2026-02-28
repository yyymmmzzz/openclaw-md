# HEARTBEAT.md

## 每日备份检查任务

每天检查工作区备份状态，执行以下操作：

### 1. GitHub 备份
```bash
cd /workspace/projects/workspace
git add -A
git diff --cached --quiet || git commit -m "Auto backup: $(date '+%Y-%m-%d %H:%M:%S')"
git push origin main
```

### 2. 邮件备份
```bash
/workspace/projects/workspace/scripts/backup-email.sh
```

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.
