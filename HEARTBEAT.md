# HEARTBEAT.md

## 备份任务 (每6小时一次)

自动备份工作区配置到 GitHub 和邮箱。

运行备份调度器：
```bash
/workspace/projects/workspace/scripts/backup-scheduler.sh
```

备份频率：每6小时自动检查并执行
下次备份时间：记录在 `.last-backup-time`

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.
