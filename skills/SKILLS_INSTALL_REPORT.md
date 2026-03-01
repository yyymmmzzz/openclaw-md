# 龙虾必备技能安装报告

**安装日期**: 2026-03-01  
**状态**: ✅ 9个技能已安装

---

## 📦 已安装技能清单

### 1. ✅ summarize（系统内置）
- **功能**: 文本摘要，支持URL/PDF/YouTube
- **使用**: `summarize "https://example.com"`
- **状态**: 已存在，无需安装

### 2. ✅ tavily-web-search（新安装）
- **功能**: AI优化联网搜索，高质量结果
- **使用**: `python3 skills/tavily-web-search/search.py "查询内容"`
- **配置**: 需设置 TAVILY_API_KEY
- **路径**: `skills/tavily-web-search/`

### 3. ✅ find-skills（新安装）
- **功能**: 智能发现适配技能，输入描述找技能
- **使用**: `python3 skills/find-skills/find.py "我想搜索网页"`
- **路径**: `skills/find-skills/`

### 4. ✅ file-manager（新安装）
- **功能**: 文件管理，读写/搜索/分类
- **使用**: `python3 skills/file-manager/manage.py [ls/find/cp/mv/rm/info/organize]`
- **路径**: `skills/file-manager/`

### 5. ✅ notification（新安装）
- **功能**: 多渠道提醒，飞书/邮件/系统通知
- **使用**: `python3 skills/notification/send.py --channel feishu --content "提醒内容"`
- **配置**: 需配置 webhook 或 SMTP
- **路径**: `skills/notification/`

### 6. ✅ task-scheduler（新安装）
- **功能**: 定时任务自动执行
- **使用**: `python3 skills/task-scheduler/schedule.py add "任务名" --command "命令" --cron "0 2 * * *"`
- **路径**: `skills/task-scheduler/`

### 7. ✅ clawsec（新安装）
- **功能**: 安全套件，防注入/审计
- **使用**: `python3 skills/clawsec/audit.py --full`
- **路径**: `skills/clawsec/`

### 8. ✅ command-executor（新安装）
- **功能**: 安全执行系统命令
- **使用**: `python3 skills/command-executor/exec.py "ls -la"`
- **路径**: `skills/command-executor/`

### 9. ✅ self-improving-agent（新安装）
- **功能**: 自我改进，持续学习
- **使用**: `python3 skills/self-improving-agent/improve.py analyze`
- **路径**: `skills/self-improving-agent/`

### 10. ✅ chinese-memory（之前已安装）
- **功能**: 国产化记忆系统（替代ontology/memory）
- **使用**: `python3 skills/chinese-memory/scripts/memory_store.py "内容"`
- **路径**: `skills/chinese-memory/`

---

## 🚀 快速测试

```bash
# 测试1: 查找技能
cd /workspace/projects/workspace
python3 skills/find-skills/find.py "怎么搜索网页"

# 测试2: 文件管理
python3 skills/file-manager/manage.py ls

# 测试3: 安全检查
python3 skills/clawsec/audit.py --check-config

# 测试4: 安全执行命令
python3 skills/command-executor/exec.py "echo Hello"

# 测试5: 分析改进点
python3 skills/self-improving-agent/improve.py report
```

---

## 📁 目录结构

```
skills/
├── chinese-memory/         # 国产化记忆系统
│   ├── scripts/
│   │   ├── memory_store.py
│   │   ├── memory_search.py
│   │   ├── knowledge_graph.py
│   │   └── setup.sh
│   └── SKILL.md
├── tavily-web-search/      # AI搜索
│   ├── search.py
│   └── SKILL.md
├── find-skills/            # 技能发现
│   ├── find.py
│   └── SKILL.md
├── file-manager/           # 文件管理
│   ├── manage.py
│   └── SKILL.md
├── notification/           # 通知
│   ├── send.py
│   └── SKILL.md
├── task-scheduler/         # 定时任务
│   ├── schedule.py
│   └── SKILL.md
├── clawsec/                # 安全
│   ├── audit.py
│   └── SKILL.md
├── command-executor/       # 命令执行
│   ├── exec.py
│   └── SKILL.md
├── self-improving-agent/   # 自我改进
│   ├── improve.py
│   └── SKILL.md
└── summarize/              # 系统内置
    └── SKILL.md
```

---

## ⚙️ 配置建议

### 1. Tavily搜索配置
```json
{
  "tavily-web-search": {
    "api_key": "tvly-your-api-key"
  }
}
```

### 2. 通知配置
```json
{
  "notification": {
    "feishu": {
      "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
    }
  }
}
```

---

## 📝 后续优化

1. **Tavily**: 需要申请API Key才能使用
2. **Notification**: 需要配置飞书Webhook或邮件SMTP
3. **Task Scheduler**: 建议结合系统cron实现自动检查
4. **Chinese Memory**: 首次使用需下载BGE模型（约1.5GB）

---

**安装完成！** 🎉
