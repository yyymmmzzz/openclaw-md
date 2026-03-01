#!/usr/bin/env python3
"""
多渠道通知发送
"""

import os
import sys
import json
import requests
import smtplib
from pathlib import Path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

CONFIG_PATH = Path.home() / ".openclaw" / "config.json"

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f).get("notification", {})
    return {}

class Notifier:
    def __init__(self):
        self.config = load_config()
    
    def send_feishu(self, title: str, content: str):
        """发送飞书机器人消息"""
        webhook = self.config.get("feishu", {}).get("webhook")
        
        if not webhook:
            print("❌ 未配置飞书Webhook")
            print("请配置: notification.feishu.webhook")
            return False
        
        data = {
            "msg_type": "text",
            "content": {
                "text": f"{title}\n\n{content}"
            }
        }
        
        try:
            resp = requests.post(webhook, json=data)
            resp.raise_for_status()
            print("✅ 飞书通知已发送")
            return True
        except Exception as e:
            print(f"❌ 发送失败: {e}")
            return False
    
    def send_email(self, to: str, subject: str, content: str):
        """发送邮件"""
        email_cfg = self.config.get("email", {})
        
        smtp_host = email_cfg.get("smtp_host")
        smtp_port = email_cfg.get("smtp_port", 587)
        username = email_cfg.get("username")
        password = email_cfg.get("password")
        
        if not all([smtp_host, username, password]):
            print("❌ 邮件配置不完整")
            return False
        
        try:
            msg = MIMEMultipart()
            msg['From'] = username
            msg['To'] = to
            msg['Subject'] = subject
            msg.attach(MIMEText(content, 'plain', 'utf-8'))
            
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
            
            print(f"✅ 邮件已发送至 {to}")
            return True
        except Exception as e:
            print(f"❌ 邮件发送失败: {e}")
            return False
    
    def send_system(self, title: str, content: str):
        """发送系统通知"""
        try:
            # macOS
            if sys.platform == "darwin":
                os.system(f"osascript -e 'display notification \"{content}\" with title \"{title}\"'")
                print("✅ 系统通知已发送")
                return True
            # Linux
            elif sys.platform == "linux":
                os.system(f'notify-send "{title}" "{content}"')
                print("✅ 系统通知已发送")
                return True
            else:
                print("⚠️ 不支持当前平台的系统通知")
                return False
        except Exception as e:
            print(f"❌ 系统通知失败: {e}")
            return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="发送通知")
    parser.add_argument("--channel", choices=["feishu", "email", "system"], required=True,
                       help="通知渠道")
    parser.add_argument("--title", default="通知", help="标题")
    parser.add_argument("--content", required=True, help="内容")
    parser.add_argument("--to", help="收件人（邮件）")
    parser.add_argument("--subject", help="邮件主题")
    
    args = parser.parse_args()
    
    notifier = Notifier()
    
    if args.channel == "feishu":
        notifier.send_feishu(args.title, args.content)
    elif args.channel == "email":
        if not args.to or not args.subject:
            print("邮件通知需要 --to 和 --subject 参数")
            sys.exit(1)
        notifier.send_email(args.to, args.subject, args.content)
    elif args.channel == "system":
        notifier.send_system(args.title, args.content)
