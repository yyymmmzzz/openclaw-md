#!/bin/bash
# Backup scheduler - runs every 6 hours
# Checks if 6 hours have passed since last backup

WORKSPACE_DIR="/workspace/projects/workspace"
LAST_BACKUP_FILE="$WORKSPACE_DIR/.last-backup-time"
INTERVAL_HOURS=6
INTERVAL_SECONDS=$((INTERVAL_HOURS * 3600))

# Get current timestamp
CURRENT_TIME=$(date +%s)

# Check if last backup time exists
if [ -f "$LAST_BACKUP_FILE" ]; then
    LAST_BACKUP=$(cat "$LAST_BACKUP_FILE")
    TIME_DIFF=$((CURRENT_TIME - LAST_BACKUP))
    
    # Check if 6 hours have passed
    if [ $TIME_DIFF -lt $INTERVAL_SECONDS ]; then
        HOURS_PASSED=$((TIME_DIFF / 3600))
        MINUTES_PASSED=$(((TIME_DIFF % 3600) / 60))
        echo "⏳ 距离上次备份仅过去 ${HOURS_PASSED}小时${MINUTES_PASSED}分钟，跳过本次备份（每6小时一次）"
        exit 0
    fi
fi

# Run backups
echo "🔄 开始备份 (每6小时一次)..."

# 1. GitHub Backup
echo "📤 GitHub 备份..."
$WORKSPACE_DIR/scripts/backup-github.sh

# 2. Email Backup
echo "📧 邮件备份..."
$WORKSPACE_DIR/scripts/backup-email.sh

# Update last backup time
echo $CURRENT_TIME > "$LAST_BACKUP_FILE"

echo "✅ 备份完成！下次备份: $(date -d "+6 hours" "+%Y-%m-%d %H:%M:%S")"
