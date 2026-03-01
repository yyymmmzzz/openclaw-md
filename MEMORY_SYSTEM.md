# MEMORY_SYSTEM.md - 记忆系统规则

## 🎯 记录原则

1. **全文本备份**：所有对话自动保存到 `memory/raw/YYYY-MM-DD.md`
2. **每日总结**：每天结束时生成 `memory/daily/YYYY-MM-DD-summary.md`
3. **分类归档**：任务、规则、知识分别存入对应目录
4. **不强制查询**：平时用现有上下文，特殊情况才查大文件

---

## 📁 目录说明

### 1. raw/ - 原始记录（全文本）
- **用途**：完整备份，防止丢失
- **更新**：自动追加，不修改
- **查询**：极少使用，仅特殊情况追溯
- **清理**：每季度归档一次，压缩存储

### 2. daily/ - 每日总结
- **用途**：快速回顾今日重点
- **内容**：
  - 今日讨论主题
  - 关键决策
  - 新增/完成任务
  - 规则变更
  - 明日待办
- **更新**：每天结束时生成

### 3. tasks/ - 任务追踪
- **active.md**：当前进行中任务
- **completed.md**：今日/本周完成任务
- **archive/**：历史任务（按YYYY-MM归档）

### 4. rules/ - 规则记录
- **changes.md**：每次规则修改记录
- **current/**：各规则文件的版本快照

### 5. knowledge/ - 知识库
- **solutions.md**：常见问题解决方案
- **preferences.md**：老板偏好（邮箱、习惯等）
- **people.md**：联系人信息（yimo, matt等）
- **decisions.md**：重要决策及原因

---

## 🔄 更新流程

### 每次对话后自动执行：
```
1. 追加到 memory/raw/YYYY-MM-DD.md
2. 检查是否有新任务 → 更新 tasks/active.md
3. 检查是否有规则变更 → 更新 rules/changes.md
4. 检查是否有新知识 → 更新对应 knowledge/ 文件
```

### 每天结束时（23:59）：
```
1. 生成 memory/daily/YYYY-MM-DD-summary.md
2. 归档已完成的任务到 tasks/archive/
3. 更新 memory/index.md 索引
```

---

## 📝 记录格式

### 原始记录格式（raw/）
```markdown
## 2026-03-01 00:14
**老板**: 你有办法操作我手机吗
**扣子虾**: 我无法操作你的手机...
[思考过程...]
[工具调用...]
```

### 每日总结格式（daily/）
```markdown
# 2026-03-01 总结

## 讨论主题
1. 飞书消息延迟问题调查
2. 豆包手机协作方案设计
3. 记忆系统设计

## 关键决策
- ✅ 添加 create_time 字段到飞书插件
- ✅ 豆包定时任务频率：30分钟
- ✅ 建立完整记忆系统

## 完成任务
- [x] 调查消息延迟原因
- [x] 设计豆包协作方案
- [x] 设计记忆系统

## 新增规则
- 记录所有对话到 memory/raw/
- 每日生成总结到 memory/daily/

## 明日待办
- [ ] 配置豆包定时任务
- [ ] 测试豆包协作流程
```

---

## 🔍 查询指南

| 查询场景 | 查找位置 |
|---------|---------|
| "昨天说了什么" | memory/daily/昨天-summary.md |
| "某个任务进度" | memory/tasks/active.md |
| "为什么做这个决策" | memory/knowledge/decisions.md |
| "老板邮箱是什么" | memory/knowledge/preferences.md |
| "完整对话内容" | memory/raw/YYYY-MM-DD.md |
| "规则什么时候改的" | memory/rules/changes.md |

---

## ⚠️ 重要提醒

1. **不主动查询**：平时用现有上下文，不频繁查文件
2. **老板要求时**：才去大文件中找特定信息
3. **定期维护**：每月清理 raw/，每季度归档旧文件
4. **隐私保护**：敏感信息（密码、token）不记录或脱敏

---

## ✅ 实施状态

**实施时间**: 2026-03-01 01:20
**状态**: ✅ 已完成初始搭建

### 生命周期管理 (新增 2026-03-01)
- ✅ 创建生命周期策略文档 `memory/lifecycle-policy.md`
- ✅ 创建生命周期管理脚本 `scripts/memory-lifecycle.sh`
- ✅ 集成到 HEARTBEAT.md 每日自动执行

**生命周期规则:**
| 记忆类型 | 生命周期 | 过期处理 |
|---------|---------|---------|
| working/ | 1 天 | 自动删除 |
| short-term/conversations/ | 30 天 | 归档到 vault/ |
| short-term/tasks/completed.md | 90 天 | 归档到 vault/ |
| raw/ | 90 天 | 压缩为 tar.gz |
| vault/ | 365 天 | 永久删除 |
| long-term/ | 永久 | 不删除 |

### 已创建文件
- ✅ `memory/index.md` - 总索引
- ✅ `memory/long-term/identity/boss-profile.md` - 老板画像
- ✅ `memory/long-term/identity/people/yimo.md` - yimo档案
- ✅ `memory/long-term/decisions/architecture.md` - 架构决策
- ✅ `memory/short-term/conversations/2026-03-01.md` - 今日对话
- ✅ `memory/short-term/tasks/active.md` - 进行中任务
- ✅ `memory/raw/2026-03/2026-03-01-full.md` - 原始记录

### 目录结构
```
memory/
├── working/              ✅ 已创建
├── short-term/           ✅ 已创建
│   ├── tasks/            ✅
│   └── conversations/    ✅
├── long-term/            ✅ 已创建
│   ├── identity/         ✅
│   │   └── people/       ✅
│   ├── knowledge/        ✅ (待填充)
│   ├── decisions/        ✅
│   └── vault/            ✅
├── raw/                  ✅ 已创建
└── index.md              ✅
```

---

*系统创建: 2026-03-01*
*最后更新: 2026-03-01*