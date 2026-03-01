---
name: task-scheduler
description: 定时任务自动执行，解放双手首选。支持cron表达式。
---

# Task Scheduler - 定时任务

自动化定时任务执行，支持cron表达式。

## 使用方法

```bash
# 添加定时任务
python3 schedule.py add "备份数据" --command "bash scripts/backup.sh" --cron "0 2 * * *"

# 列出所有任务
python3 schedule.py list

# 删除任务
python3 schedule.py remove "备份数据"

# 立即执行任务
python3 schedule.py run "备份数据"
```

## Cron表达式示例

| 表达式 | 含义 |
|-------|------|
| `0 2 * * *` | 每天凌晨2点 |
| `0 */6 * * *` | 每6小时 |
| `0 9 * * 1` | 每周一早9点 |
| `*/30 * * * *` | 每30分钟 |

## 特点

- ✅ 支持标准cron表达式
- ✅ 任务持久化存储
- ✅ 执行日志记录
- ✅ 支持立即执行
