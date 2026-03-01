---
name: command-executor
description: 安全执行系统命令，权限可控，官方内置核心技能。
---

# Command Executor - 安全命令执行

安全可控的系统命令执行工具。

## 使用方法

```bash
# 执行命令（需要确认）
python3 exec.py "ls -la"

# 强制执行（无需确认）
python3 exec.py "rm file.txt" --force

# 带超时执行
python3 exec.py "sleep 10" --timeout 5

# dry-run模式（模拟执行）
python3 exec.py "rm -rf /" --dry-run
```

## 安全特性

- ✅ 危险命令自动检测
- ✅ 执行前确认
- ✅ 超时控制
- ✅ 执行日志
- ✅ 权限检查
