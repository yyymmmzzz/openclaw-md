#!/bin/bash
# Email backup script for OpenClaw workspace settings
# Backs up configuration files and sends via email using QQ SMTP

set -e

WORKSPACE_DIR="/workspace/projects/workspace"
BACKUP_DIR="/tmp/openclaw-backup-$(date +%Y%m%d-%H%M%S)"
EMAIL="78899690@qq.com"
DATE=$(date '+%Y-%m-%d %H:%M:%S')
BACKUP_LOG="$WORKSPACE_DIR/.backup-email.log"

echo "[$DATE] Starting email backup..." >> "$BACKUP_LOG"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Copy only configuration files (not sensitive data)
cp "$WORKSPACE_DIR/AGENTS.md" "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE_DIR/SOUL.md" "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE_DIR/TOOLS.md" "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE_DIR/IDENTITY.md" "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE_DIR/USER.md" "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE_DIR/HEARTBEAT.md" "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE_DIR/BOOTSTRAP.md" "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE_DIR/BACKUP.md" "$BACKUP_DIR/" 2>/dev/null || true
cp "$WORKSPACE_DIR/README.md" "$BACKUP_DIR/" 2>/dev/null || true

# Copy skills directory (SKILL.md files only)
mkdir -p "$BACKUP_DIR/skills"
for skill_dir in "$WORKSPACE_DIR"/skills/*/; do
    if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        mkdir -p "$BACKUP_DIR/skills/$skill_name"
        cp "$skill_dir"SKILL.md "$BACKUP_DIR/skills/$skill_name/" 2>/dev/null || true
    fi
done

# Copy scripts directory
mkdir -p "$BACKUP_DIR/scripts"
cp "$WORKSPACE_DIR/scripts/backup.sh" "$BACKUP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE_DIR/scripts/setup-remote.sh" "$BACKUP_DIR/scripts/" 2>/dev/null || true
cp "$WORKSPACE_DIR/scripts/backup-email.sh" "$BACKUP_DIR/scripts/" 2>/dev/null || true

# Create archive
ARCHIVE_NAME="openclaw-settings-$(date +%Y%m%d-%H%M%S).tar.gz"
ARCHIVE_PATH="/tmp/$ARCHIVE_NAME"
cd /tmp
tar -czf "$ARCHIVE_NAME" "$(basename $BACKUP_DIR)"

# Get file size
FILE_SIZE=$(du -h "$ARCHIVE_PATH" | cut -f1)
echo "[$DATE] Archive created: $ARCHIVE_NAME ($FILE_SIZE)" >> "$BACKUP_LOG"

# Send email using Python
python3 << PYEOF
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os

# QQ Mail settings
smtp_server = "smtp.qq.com"
smtp_port = 465
sender_email = "78899690@qq.com"
auth_code = "wtmkhteyhuktbgfh"
receiver_email = "78899690@qq.com"
archive_path = "$ARCHIVE_PATH"
archive_name = "$ARCHIVE_NAME"

# Create message
msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = f"OpenClaw 工作区设置备份 - {os.path.basename(archive_name).replace('openclaw-settings-', '').replace('.tar.gz', '')}"

body = f"""
这是扣子工作区的设置文件备份。

备份时间: $DATE
文件大小: $FILE_SIZE
包含内容:
- AGENTS.md (代理配置)
- SOUL.md (核心行为准则)
- TOOLS.md (工具配置)
- IDENTITY.md (身份信息)
- USER.md (用户信息)
- HEARTBEAT.md (定时任务)
- BACKUP.md (备份说明)
- skills/ (技能配置)
- scripts/ (脚本文件)

此邮件由 OpenClaw 自动发送。
"""

msg.attach(MIMEText(body, 'plain', 'utf-8'))

# Attach backup file
if os.path.exists(archive_path):
    with open(archive_path, 'rb') as f:
        attachment = MIMEBase('application', 'octet-stream')
        attachment.set_payload(f.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment', filename=archive_name)
    msg.attach(attachment)

try:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context, timeout=60) as server:
        server.login(sender_email, auth_code)
        server.send_message(msg)
    print("✅ 邮件发送成功！")
    exit(0)
except Exception as e:
    print(f"❌ 邮件发送失败: {e}")
    # Save email to file for manual inspection
    email_file = "/tmp/openclaw-backup-failed.eml"
    with open(email_file, 'wb') as f:
        f.write(msg.as_bytes())
    print(f"邮件已保存到: {email_file}")
    exit(1)
PYEOF

RESULT=$?

if [ $RESULT -eq 0 ]; then
    echo "[$DATE] Email sent successfully to $EMAIL" >> "$BACKUP_LOG"
    # Cleanup
    rm -rf "$BACKUP_DIR" "$ARCHIVE_PATH"
else
    echo "[$DATE] Email sending failed, archive kept at $ARCHIVE_PATH" >> "$BACKUP_LOG"
fi

echo "[$DATE] Backup process completed." >> "$BACKUP_LOG"
