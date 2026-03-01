# 记忆生命周期策略

**生效日期**: 2026-03-01  
**版本**: 1.0  
**执行脚本**: `scripts/memory-lifecycle.sh`

---

## 🎯 策略目标

1. **防止存储爆炸** — 控制记忆系统总体积
2. **保持查询效率** — 移除过时/低频访问的记忆
3. **保留核心价值** — 长期记忆永久保存

---

## 📋 生命周期规则

| 记忆类型 | 位置 | 生命周期 | 过期处理 |
|---------|------|---------|---------|
| **工作记忆** | `working/` | 1 天 | 自动删除 |
| **短期对话** | `short-term/conversations/` | 30 天 | 归档到 `vault/conversations/` |
| **已完成任务** | `short-term/tasks/completed.md` | 90 天 | 归档到 `vault/tasks/` |
| **原始记录** | `raw/YYYY-MM/` | 90 天 | 压缩为 `.tar.gz` 并存入 `vault/raw/` |
| **归档文件** | `vault/` | 365 天 (1年) | 永久删除 |
| **长期记忆** | `long-term/` | 永久 | 不删除，定期整理 |
| **进行中任务** | `short-term/tasks/active.md` | 永久 | 完成后移至 completed |

---

## 🔄 执行流程

### 每日自动执行 (通过 heartbeat)

```
1. 清理 working/ 中超过 1 天的文件
2. 归档 short-term/conversations/ 中超过 30 天的对话
3. 归档 completed.md（如果超过 90 天）
4. 压缩 raw/ 中超过 90 天的月份目录
5. 删除 vault/ 中超过 1 年的归档
6. 更新统计信息到 index.md
```

### 手动触发

```bash
sh /workspace/projects/workspace/scripts/memory-lifecycle.sh
```

---

## 📁 目录结构（含生命周期）

```
memory/
├── working/              # 1天生命周期
│   └── current-session.md
│
├── short-term/           # 30-90天生命周期
│   ├── conversations/    # 30天后归档
│   │   ├── 2026-03-01.md
│   │   └── 2026-03-02.md
│   └── tasks/
│       ├── active.md     # 永久（直到完成）
│       └── completed.md  # 90天后归档
│
├── long-term/            # 永久保存
│   ├── identity/
│   ├── knowledge/
│   └── decisions/
│
├── raw/                  # 90天后压缩
│   └── 2026-03/
│       └── 2026-03-01-full.md
│
├── vault/                # 1年后删除
│   ├── conversations/    # 归档的对话
│   ├── tasks/            # 归档的任务
│   └── raw/              # 压缩的原始记录
│       └── 2026-03.tar.gz
│
└── index.md              # 统计索引
```

---

## 📝 日志记录

所有生命周期操作记录到：`memory/.lifecycle-log`

示例日志：
```
🧹 记忆系统生命周期管理 - 2026-03-01
================================

📂 [1/5] 清理 working/ 目录 (保留 1 天)
  ✅ 无需清理

📂 [2/5] 归档短期对话 (超过 30 天)
  ✅ 无需归档

📂 [3/5] 归档已完成任务 (超过 90 天)
  ✅ 无需归档 (仅 5 天)

📂 [4/5] 压缩原始记录 (超过 90 天)
  ✅ 无需压缩

📂 [5/5] 清理 vault/ 过期归档 (超过 365 天)
  ✅ 无需清理

📊 [统计] 更新记忆系统状态
  📁 working/: 1 文件
  📁 short-term/: 3 文件
  📁 long-term/: 4 文件
  📁 raw/: 1 文件
  📁 vault/: 0 文件

✅ 生命周期管理完成！
```

---

## ⚙️ 配置调整

如需调整生命周期参数，编辑脚本中的配置部分：

```bash
# 在 scripts/memory-lifecycle.sh 中修改

WORKING_MAX_AGE_DAYS=1           # 工作记忆保留天数
CONVERSATION_MAX_AGE_DAYS=30     # 对话保留天数
COMPLETED_TASK_MAX_AGE_DAYS=90   # 已完成任务保留天数
RAW_MAX_AGE_DAYS=90              # 原始记录保留天数
VAULT_MAX_AGE_DAYS=365           # 归档保留天数
```

---

## 🚨 注意事项

1. **删除不可逆** — 超过生命周期的文件会被永久删除（除归档外）
2. **长期记忆不受影响** — `long-term/` 中的文件永不删除
3. **手动备份建议** — 重要信息建议手动备份到 `long-term/`
4. **日志可审计** — 所有操作都有日志记录，可追溯

---

**创建**: 2026-03-01  
**维护者**: 扣子虾
