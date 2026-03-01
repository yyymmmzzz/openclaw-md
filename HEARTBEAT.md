# HEARTBEAT.md

## 备份任务 (每6小时一次)

自动备份工作区配置到 GitHub 和邮箱。

运行备份调度器：
```bash
/workspace/projects/workspace/scripts/backup-scheduler.sh
```

备份频率：每6小时自动检查并执行
下次备份时间：记录在 `.last-backup-time`

---

## 记忆生命周期管理 (每日一次)

自动清理过期记忆，防止存储爆炸。

运行生命周期管理：
```bash
/workspace/projects/workspace/scripts/memory-lifecycle.sh
```

执行频率：每日一次
生命周期策略：详见 `memory/lifecycle-policy.md`

| 记忆类型 | 生命周期 | 过期处理 |
|---------|---------|---------|
| working/ | 1 天 | 删除 |
| short-term/conversations/ | 30 天 | 归档 |
| short-term/tasks/completed.md | 90 天 | 归档 |
| raw/ | 90 天 | 压缩 |
| vault/ | 365 天 | 删除 |

---

## 日报生成 (每日08:00)

每天早上8点自动生成前一天日报并发送邮件。

运行日报生成：
```bash
# 自动生成（早上8点运行生成前一天日报）
python3 /workspace/projects/workspace/scripts/daily-report.py

# 指定生成昨天日报
python3 /workspace/projects/workspace/scripts/daily-report.py --yesterday

# 指定日期
python3 /workspace/projects/workspace/scripts/daily-report.py --date 2026-03-01
```

执行频率：每日08:00（生成前一天日报）
日报内容：
- 📅 前日概览（日期、对话主题）
- 🛠️ 新增技能
- 📚 学习内容
- ⚠️ 错误与改进
- 📋 重要决策
- 📌 待办事项
- 💰 Token使用统计
- 📊 系统状态

发送方式：邮件发送至 78899690@qq.com
保存位置：`memory/daily/YYYY-MM-DD-daily-report.md`

---

## 自动重试机制

所有关键操作都配置了自动重试，确保任务不遗漏。

**重试策略:**
- 最大重试次数: 3次
- 初始延迟: 1秒
- 退避因子: 2倍（即1s → 2s → 4s）

**应用范围:**
- ✅ 文件编辑操作
- ✅ 网络请求（API调用）
- ✅ 邮件发送
- ✅ 备份任务
- ✅ 日报生成

**重试日志:** `memory/logs/retry-log.md`

**使用方法:**
```python
from retry_mechanism import retry_with_backoff, retry_task

# 装饰器方式
@retry_with_backoff(max_attempts=3)
def my_function():
    # 可能失败的操作
    pass

# 函数方式
def task():
    # 任务逻辑
    pass

success, result, error = retry_task(task, "任务名称", max_attempts=3)
```

**失败处理:**
- 重试3次仍失败 → 记录到待办任务 → 通知老板
- 不会静默失败，确保您知道任务状态

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.
