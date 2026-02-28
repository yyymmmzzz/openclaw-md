#!/bin/bash
# GitHub backup script for OpenClaw workspace
# Pushes workspace to GitHub repository

set -e

WORKSPACE_DIR="/workspace/projects/workspace"
BACKUP_LOG="$WORKSPACE_DIR/.backup-github.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] Starting GitHub backup..." >> "$BACKUP_LOG"

cd "$WORKSPACE_DIR"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "[$DATE] Git not initialized, initializing..." >> "$BACKUP_LOG"
    git init
    git config user.name "扣子虾"
    git config user.email "bot@coze.local"
fi

# Add all changes
git add -A

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "[$DATE] No changes to commit." >> "$BACKUP_LOG"
else
    # Commit with timestamp
    COMMIT_MSG="Auto backup: $DATE"
    git commit -m "$COMMIT_MSG"
    echo "[$DATE] Committed: $COMMIT_MSG" >> "$BACKUP_LOG"
fi

# Check if remote is configured
if git remote | grep -q origin; then
    # Push to remote
    if git push origin main 2>&1 | tee -a "$BACKUP_LOG"; then
        echo "[$DATE] GitHub backup completed successfully!" >> "$BACKUP_LOG"
        echo "✅ GitHub 备份完成！"
    else
        echo "[$DATE] GitHub push failed!" >> "$BACKUP_LOG"
        echo "⚠️ GitHub 推送失败，请检查网络或授权"
        exit 1
    fi
else
    echo "[$DATE] No remote configured. Please run setup script first." >> "$BACKUP_LOG"
    echo "⏳ 远程仓库未配置，请先运行 setup-remote.sh"
fi

echo "[$DATE] Backup process completed." >> "$BACKUP_LOG"
