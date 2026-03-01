# 进行中任务

**最后更新**: 2026-03-01 01:20

---

## 高优先级

### [TASK-001] 配置豆包定时任务 {#task-doubao-scheduler}
**状态**: 🟡 待执行
**创建**: 2026-03-01
**截止时间**: 2026-03-02
**负责人**: 老板 + 扣子虾

**描述**:
配置豆包AI每30分钟检查飞书消息，识别"#豆包"标记的任务并执行。

**具体步骤**:
1. 老板唤醒豆包
2. 设置定时任务：
   - 名称: 检查扣子虾消息
   - 频率: 每30分钟
   - 操作: 打开飞书 → 查看扣子虾未读消息 → 识别"#豆包"标记 → 执行 → 回复"✅ 已完成"
3. 测试首次运行

**依赖**:
- 豆包能识别飞书界面
- 能正确识别"#豆包"关键词

---

### [TASK-002] 验证飞书 `create_time` 字段 {#task-verify-create-time}
**状态**: 🟡 待验证
**创建**: 2026-03-01
**截止时间**: 2026-03-02
**负责人**: 扣子虾

**描述**:
验证修改后的飞书插件是否能正确获取和使用 `create_time` 字段。

**验证方法**:
1. 发送测试消息
2. 检查是否能读取 `create_time`
3. 对比 `create_time` 和收到时间的差值
4. 测试延迟消息识别功能

**相关文件**:
- `/usr/lib/node_modules/openclaw/extensions/feishu/src/bot.ts`
- `/usr/lib/node_modules/openclaw/extensions/feishu/src/types.ts`

---

## 中优先级

### [TASK-003] 配置GitHub备份 {#task-github-backup}
**状态**: 🟡 等待matt
**创建**: 2026-03-01
**截止时间**: 待定
**负责人**: matt + 扣子虾

**描述**:
配置工作区自动备份到 GitHub 仓库。

**信息**:
- 仓库: https://github.com/yyymmmzzz/openclaw-md
- 需要: GitHub Personal Access Token

**下一步**:
等待 matt 提供Token或自行创建仓库

---

## 低优先级

### [TASK-004] 完善长期记忆档案 {#task-memory-archives}
**状态**: 🔵 持续进行
**创建**: 2026-03-01
**负责人**: 扣子虾

**待创建**:
- [ ] matt 档案
- [ ] 豆包手机知识库
- [ ] 飞书插件修改决策记录
- [ ] 常用工具指南

---

## 已完成任务

### [TASK-000] 建立分层记忆系统
**状态**: ✅ 已完成
**完成时间**: 2026-03-01
**产出**:
- 完整目录结构
- 老板画像档案
- yimo 档案
- 今日对话摘要

### [TASK-005] 安装10个必备Skill
**状态**: ✅ 已完成
**完成时间**: 2026-03-01
**负责人**: 扣子虾
**描述**: 安装豆包推荐的10个必备Skill（第3个已做国产版）
**产出**:
1. ✅ summarize（系统内置）
2. ✅ tavily-web-search（AI搜索）
3. ✅ chinese-memory（国产记忆，替代ontology/memory）
4. ✅ find-skills（技能发现）
5. ✅ file-manager（文件管理）
6. ✅ notification（多渠道通知）
7. ✅ task-scheduler（定时任务）
8. ✅ clawsec（安全审计）
9. ✅ command-executor（安全命令执行）
10. ✅ self-improving-agent（自我改进）

**相关文件**: `skills/SKILLS_INSTALL_REPORT.md`

### [TASK-006] 创建email-sender Skill + 技能记忆规则
**状态**: ✅ 已完成
**完成时间**: 2026-03-01
**负责人**: 扣子虾
**描述**: 
1. 创建邮件发送Skill（基于已有QQ邮箱配置）
2. 在SOUL.md添加规则10：Skill Awareness & Usage（技能记忆与使用）
3. 添加邮件读取功能（IMAP）
4. 获得持续授权，可主动查看邮件

**产出**:
- ✅ email-sender Skill（skills/email-sender/）
- ✅ SOUL.md规则10：技能记忆与使用黄金规则
- ✅ 技能清单和触发使用规则
- ✅ 邮件读取功能（read_email.py）
- ✅ 持续授权：可主动查看邮件

**相关文件**: 
- `skills/email-sender/SKILL.md`
- `skills/email-sender/send_email.py`
- `skills/email-sender/read_email.py`
- `SOUL.md`（规则10）
- `TOOLS.md`（邮件访问授权）

### [TASK-007] 创建日报系统
**状态**: ✅ 已完成
**完成时间**: 2026-03-01
**负责人**: 扣子虾
**描述**: 
1. 创建日报生成脚本
2. 集成到HEARTBEAT.md每日自动执行
3. 日报内容包括：今日概览、新增技能、学习内容、错误改进、重要决策、待办事项、系统状态
4. 升级为HTML看板形式
5. 抄送给Matt (804314819@qq.com)

**产出**:
- ✅ 日报生成脚本（scripts/daily-report.py）
- ✅ HEARTBEAT.md 添加日报任务
- ✅ 已生成首份日报并发送
- ✅ HTML看板形式日报
- ✅ 同时发送给老板和Matt

**收件人**:
- 老板: 78899690@qq.com
- Matt: 804314819@qq.com

**相关文件**: 
- `scripts/daily-report.py`
- `HEARTBEAT.md`

### [TASK-008] 创建自动重试机制
**状态**: ✅ 已完成
**完成时间**: 2026-03-01
**负责人**: 扣子虾
**描述**: 
1. 创建通用重试机制（装饰器和函数两种方式）
2. 创建安全文件编辑工具（带重试）
3. 配置重试策略：3次、退避1→2→4秒
4. 记录重试日志到 memory/logs/retry-log.md

**产出**:
- ✅ 重试机制模块（scripts/retry_mechanism.py）
- ✅ 安全文件编辑工具（scripts/safe_file_edit.py）
- ✅ HEARTBEAT.md 添加重试机制说明
- ✅ 测试通过

**应用范围**:
- 文件编辑操作
- 网络请求（API调用）
- 邮件发送
- 备份任务
- 日报生成

**相关文件**: 
- `scripts/retry_mechanism.py`
- `scripts/safe_file_edit.py`
- `HEARTBEAT.md`
- `memory/logs/retry-log.md`

---

## 统计

| 状态 | 数量 |
|-----|------|
| 🟡 进行中 | 3 |
| 🔵 持续 | 1 |
| ✅ 已完成 | 2 |

---

*维护者: 扣子虾*
*更新频率: 实时*