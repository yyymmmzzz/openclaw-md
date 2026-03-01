#!/usr/bin/env python3
"""
邮件发送工具
支持SMTP协议，已配置QQ邮箱
"""

import os
import sys
import json
import smtplib
import ssl
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

CONFIG_PATH = Path.home() / ".openclaw" / "config.json"

def load_config():
    """加载配置"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            config = json.load(f)
            # 优先使用email-sender配置，其次使用notification.email配置
            return config.get("email-sender", config.get("notification", {}).get("email", {}))
    return {}

def send_email(subject: str, body: str, to: str = None, 
               html: bool = False, attachment: str = None,
               smtp_host: str = None, smtp_port: int = None,
               username: str = None, password: str = None) -> bool:
    """
    发送邮件
    
    Args:
        subject: 邮件主题
        body: 邮件正文
        to: 收件人（默认使用发件人）
        html: 是否为HTML格式
        attachment: 附件路径
        smtp_host: SMTP服务器
        smtp_port: SMTP端口
        username: 发件人邮箱
        password: 邮箱密码/授权码
    
    Returns:
        发送成功返回True
    """
    # 加载配置
    config = load_config()
    
    # 使用传入参数或配置
    smtp_host = smtp_host or config.get("smtp_host", "smtp.qq.com")
    smtp_port = smtp_port or config.get("smtp_port", 465)
    username = username or config.get("username", "78899690@qq.com")
    password = password or config.get("password", "yoqflhregdevbjaj")
    to = to or config.get("default_to", username)
    
    if not all([smtp_host, username, password]):
        print("❌ 邮件配置不完整")
        print("请配置 ~/.openclaw/config.json")
        return False
    
    try:
        # 创建邮件
        msg = MIMEMultipart()
        msg['From'] = username
        msg['To'] = to
        msg['Subject'] = subject
        
        # 添加正文
        content_type = 'html' if html else 'plain'
        msg.attach(MIMEText(body, content_type, 'utf-8'))
        
        # 添加附件
        if attachment and os.path.exists(attachment):
            with open(attachment, 'rb') as f:
                attachment_part = MIMEBase('application', 'octet-stream')
                attachment_part.set_payload(f.read())
            encoders.encode_base64(attachment_part)
            attachment_part.add_header(
                'Content-Disposition',
                f'attachment; filename="{os.path.basename(attachment)}"'
            )
            msg.attach(attachment_part)
            print(f"📎 附件: {os.path.basename(attachment)}")
        
        # 发送邮件
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context, timeout=60) as server:
            server.login(username, password)
            server.send_message(msg)
        
        print(f"✅ 邮件发送成功！")
        print(f"   收件人: {to}")
        print(f"   主题: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")
        return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="发送邮件")
    parser.add_argument("--subject", "-s", help="邮件主题")
    parser.add_argument("--body", "-b", help="邮件正文")
    parser.add_argument("--to", help="收件人邮箱")
    parser.add_argument("--html", action="store_true", help="HTML格式")
    parser.add_argument("--attach", help="附件路径")
    parser.add_argument("--test", action="store_true", help="发送测试邮件")
    
    args = parser.parse_args()
    
    if args.test:
        # 发送测试邮件
        success = send_email(
            subject="邮件功能测试",
            body=f"这是一封测试邮件。\n\n发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n如果收到这封邮件，说明邮件发送功能正常工作。",
            to=args.to if args.to else "78899690@qq.com"
        )
        sys.exit(0 if success else 1)
    else:
        if not args.subject or not args.body:
            print("❌ 错误: 必须提供 --subject 和 --body 参数")
            print("示例: python3 send_email.py --subject '主题' --body '内容'")
            sys.exit(1)
        
        send_email(
            subject=args.subject,
            body=args.body,
            to=args.to,
            html=args.html,
            attachment=args.attach
        )

if __name__ == "__main__":
    main()
