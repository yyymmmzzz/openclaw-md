---
name: email-sender
description: 邮件发送和读取技能，支持SMTP发送和IMAP读取。支持QQ邮箱、163邮箱、Gmail等主流邮箱。
---

# Email Sender - 邮件发送与读取

支持邮件的**发送**和**读取**功能。

## 已配置的邮箱

**QQ邮箱**（已配置）
- SMTP服务器: smtp.qq.com:465（发送）
- IMAP服务器: imap.qq.com:993（读取）
- 账号: 78899690@qq.com

## 发送邮件

```bash
# 发送简单邮件
python3 send_email.py --subject "测试邮件" --body "这是一封测试邮件"

# 发送带附件的邮件
python3 send_email.py --subject "备份文件" --body "请查收附件" --attach /path/to/file.txt

# 发送HTML邮件
python3 send_email.py --subject "HTML测试" --html --body "<h1>标题</h1><p>内容</p>"

# 发送测试邮件
python3 send_email.py --test
```

## 读取邮件

```bash
# 查看收件箱未读邮件
python3 read_email.py --unread

# 查看最近10封邮件
python3 read_email.py --limit 10

# 搜索邮件
python3 read_email.py --search "扣子虾"

# 查看邮件详情
python3 read_email.py --id 12345

# 标记已读
python3 read_email.py --mark-read 12345
```

## Python API

```python
from email_sender import send_email, read_emails

# 发送邮件
send_email(subject="工作汇报", body="今日工作总结...")

# 读取邮件
emails = read_emails(unread_only=True, limit=5)
for email in emails:
    print(f"来自: {email['from']}")
    print(f"主题: {email['subject']}")
    print(f"内容: {email['body'][:200]}...")
```

## 配置其他邮箱

编辑 `~/.openclaw/config.json`：

```json
{
  "email-sender": {
    "smtp_host": "smtp.example.com",
    "smtp_port": 465,
    "imap_host": "imap.example.com",
    "imap_port": 993,
    "username": "your@example.com",
    "password": "your-password"
  }
}
```

## 安全声明

- ✅ 邮件内容仅用于服务老板
- ✅ 不会未经授权转发或泄露邮件
- ✅ **已获得持续授权，可主动查看邮件**
- ✅ 所有访问记录可追溯

## 授权范围

**老板已授权：**
- ✅ 主动查看邮件（无需每次请示）
- ✅ 定时检查邮件（用于自动化功能）
- ✅ 基于邮件内容执行后续任务

**使用场景：**
- 定时备份时检查备份确认邮件
- 自动提取邮件中的待办事项
- 监控重要通知并提醒
- 其他自动化邮件处理任务

## 常见使用场景

1. **自动检查邮件** - 定时查看是否有重要通知
2. **备份通知确认** - 发送备份后确认收到
3. **任务提醒** - 从邮件中提取待办事项
4. **信息汇总** - 整理一段时间内的邮件摘要
