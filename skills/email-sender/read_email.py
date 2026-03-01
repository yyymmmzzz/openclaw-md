#!/usr/bin/env python3
"""
邮件读取工具
支持IMAP协议，已配置QQ邮箱
"""

import os
import sys
import json
import imaplib
import email
from pathlib import Path
from email.header import decode_header
from datetime import datetime, timedelta

CONFIG_PATH = Path.home() / ".openclaw" / "config.json"

def load_config():
    """加载配置"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            config = json.load(f)
            return config.get("email-sender", config.get("notification", {}).get("email", {}))
    return {}

def decode_str(s):
    """解码邮件主题/发件人等"""
    if s is None:
        return ""
    decoded = decode_header(s)
    result = ""
    for text, charset in decoded:
        if isinstance(text, bytes):
            if charset:
                result += text.decode(charset)
            else:
                result += text.decode('utf-8', errors='ignore')
        else:
            result += text
    return result

def get_email_body(msg):
    """获取邮件正文"""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                try:
                    return part.get_payload(decode=True).decode('utf-8', errors='ignore')
                except:
                    pass
            elif content_type == "text/html":
                try:
                    return part.get_payload(decode=True).decode('utf-8', errors='ignore')
                except:
                    pass
    else:
        try:
            return msg.get_payload(decode=True).decode('utf-8', errors='ignore')
        except:
            pass
    return "[无法读取邮件内容]"

class EmailReader:
    def __init__(self):
        self.config = load_config()
        self.imap_host = self.config.get("imap_host", "imap.qq.com")
        self.imap_port = self.config.get("imap_port", 993)
        self.username = self.config.get("username", "78899690@qq.com")
        self.password = self.config.get("password", "yoqflhregdevbjaj")
    
    def connect(self):
        """连接IMAP服务器"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_host, self.imap_port)
            mail.login(self.username, self.password)
            return mail
        except Exception as e:
            print(f"❌ 连接邮件服务器失败: {e}")
            return None
    
    def list_folders(self):
        """列出所有文件夹"""
        mail = self.connect()
        if not mail:
            return []
        
        try:
            _, folders = mail.list()
            mail.logout()
            return [f.decode().split('"/"')[-1].strip().strip('"') for f in folders]
        except Exception as e:
            print(f"❌ 获取文件夹列表失败: {e}")
            return []
    
    def read_emails(self, folder="INBOX", limit=10, unread_only=False, 
                    since_days=None, search_keyword=None):
        """
        读取邮件
        
        Args:
            folder: 邮件文件夹（默认INBOX收件箱）
            limit: 返回邮件数量
            unread_only: 仅返回未读邮件
            since_days: 只返回N天内的邮件
            search_keyword: 搜索关键词
        
        Returns:
            邮件列表
        """
        mail = self.connect()
        if not mail:
            return []
        
        try:
            # 选择文件夹
            status, _ = mail.select(folder)
            if status != 'OK':
                print(f"❌ 无法访问文件夹: {folder}")
                return []
            
            # 构建搜索条件
            search_criteria = []
            
            if unread_only:
                search_criteria.append('UNSEEN')
            
            if since_days:
                date = (datetime.now() - timedelta(days=since_days)).strftime("%d-%b-%Y")
                search_criteria.append(f'SINCE {date}')
            
            if search_keyword:
                search_criteria.append(f'SUBJECT "{search_keyword}"')
            
            # 执行搜索
            if search_criteria:
                search_str = ' '.join(search_criteria)
            else:
                search_str = 'ALL'
            
            status, messages = mail.search(None, search_str)
            if status != 'OK':
                print("❌ 搜索邮件失败")
                return []
            
            email_ids = messages[0].split()
            
            # 只取最近的N封
            email_ids = email_ids[-limit:]
            
            emails = []
            for email_id in reversed(email_ids):  # 最新的在前
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                if status != 'OK':
                    continue
                
                msg = email.message_from_bytes(msg_data[0][1])
                
                email_info = {
                    "id": email_id.decode(),
                    "from": decode_str(msg.get("From")),
                    "to": decode_str(msg.get("To")),
                    "subject": decode_str(msg.get("Subject")),
                    "date": msg.get("Date"),
                    "body": get_email_body(msg),
                }
                emails.append(email_info)
            
            mail.logout()
            return emails
            
        except Exception as e:
            print(f"❌ 读取邮件失败: {e}")
            return []
    
    def mark_as_read(self, email_id):
        """标记邮件为已读"""
        mail = self.connect()
        if not mail:
            return False
        
        try:
            mail.select("INBOX")
            mail.store(email_id.encode(), '+FLAGS', '\\Seen')
            mail.logout()
            print(f"✅ 已标记为已读: {email_id}")
            return True
        except Exception as e:
            print(f"❌ 标记已读失败: {e}")
            return False

def print_emails(emails, show_body=False):
    """打印邮件列表"""
    if not emails:
        print("📭 没有找到邮件")
        return
    
    print(f"📧 找到 {len(emails)} 封邮件:\n")
    print("-" * 60)
    
    for i, e in enumerate(emails, 1):
        print(f"\n{i}. 📨 ID: {e['id']}")
        print(f"   来自: {e['from']}")
        print(f"   主题: {e['subject']}")
        print(f"   时间: {e['date']}")
        if show_body:
            print(f"\n   内容:\n   {e['body'][:500]}...")
        print("-" * 60)

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="读取邮件")
    parser.add_argument("--unread", action="store_true", help="仅未读邮件")
    parser.add_argument("--limit", type=int, default=10, help="邮件数量")
    parser.add_argument("--days", type=int, help="N天内的邮件")
    parser.add_argument("--search", help="搜索关键词")
    parser.add_argument("--id", help="查看特定ID邮件详情")
    parser.add_argument("--mark-read", help="标记邮件为已读")
    parser.add_argument("--folders", action="store_true", help="列出所有文件夹")
    
    args = parser.parse_args()
    
    reader = EmailReader()
    
    if args.folders:
        folders = reader.list_folders()
        print("📁 邮件文件夹:")
        for f in folders:
            print(f"  - {f}")
    
    elif args.mark_read:
        reader.mark_as_read(args.mark_read)
    
    elif args.id:
        # 查看特定邮件详情
        emails = reader.read_emails(limit=100)
        for e in emails:
            if e['id'] == args.id:
                print_emails([e], show_body=True)
                return
        print(f"❌ 未找到ID为 {args.id} 的邮件")
    
    else:
        # 读取邮件列表
        emails = reader.read_emails(
            limit=args.limit,
            unread_only=args.unread,
            since_days=args.days,
            search_keyword=args.search
        )
        print_emails(emails)

if __name__ == "__main__":
    main()
