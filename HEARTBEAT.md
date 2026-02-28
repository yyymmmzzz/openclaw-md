# HEARTBEAT.md

## 每日备份检查任务

每天检查工作区备份状态，执行以下操作：
1. 检查 git 仓库状态
2. 如果有未提交的更改，自动提交
3. 如果配置了远程仓库，自动推送

运行备份命令：
```bash
source /workspace/projects/workspace/.env/backup.env 2>/dev/null || true
/workspace/projects/workspace/scripts/backup.sh
```

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.
