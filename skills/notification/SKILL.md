---
name: notification
description: 多渠道提醒，支持飞书/邮件/系统通知。时间管理刚需。
---

# Notification - 多渠道通知

支持多种通知渠道，及时提醒重要事项。

## 使用方法

```bash
# 飞书通知
python3 send.py --channel feishu --title "提醒" --content "该开会了"

# 邮件通知
python3 send.py --channel email --to boss@example.com --subject "日报" --content "今日工作总结"

# 系统通知
python3 send.py --channel system --title "任务完成" --content "备份已完成"
```

## 配置

编辑 `~/.openclaw/config.json`：

```json
{
  "notification": {
    "feishu": {
      "webhook": "https://open.feishu.cn/open-apis/bot/v2/hook/xxx"
    },
    "email": {
      "smtp_host": "smtp.example.com",
      "smtp_port": 587,
      "username": "user@example.com",
      "password": "password"
    }
  }
}
```
