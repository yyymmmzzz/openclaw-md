#!/bin/bash
# Daily backup script for OpenClaw workspace
# Run this script to backup workspace to GitHub/GitLab

set -e

WORKSPACE_DIR="/workspace/projects/workspace"
BACKUP_LOG="/workspace/projects/workspace/.backup.log"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "[$DATE] Starting backup..." >> "$BACKUP_LOG"

cd "$WORKSPACE_DIR"

# Configure git (if not already configured)
if [ -z "$(git config user.name)" ]; then
    git config user.name "OpenClaw Bot"
    git config user.email "bot@openclaw.local"
fi

# Add all tracked and new files
git add -A

# Check if there are changes to commit
if git diff --cached --quiet; then
    echo "[$DATE] No changes to commit." >> "$BACKUP_LOG"
    echo "No changes to backup today."
    exit 0
fi

# Commit with timestamp
COMMIT_MSG="Auto backup: $DATE"
git commit -m "$COMMIT_MSG"

# Push to remote (configure REMOTE_URL and BRANCH below)
REMOTE_URL="${REMOTE_URL:-}"
BRANCH="${BRANCH:-main}"

if [ -n "$REMOTE_URL" ]; then
    # Check if remote exists
    if ! git remote | grep -q origin; then
        git remote add origin "$REMOTE_URL"
    fi
    
    # Push to remote
    if git push origin "$BRANCH"; then
        echo "[$DATE] Backup pushed successfully to $REMOTE_URL" >> "$BACKUP_LOG"
        echo "Backup completed and pushed!"
    else
        echo "[$DATE] Failed to push backup" >> "$BACKUP_LOG"
        echo "Backup committed locally but push failed."
        exit 1
    fi
else
    echo "[$DATE] No remote configured. Commit saved locally only." >> "$BACKUP_LOG"
    echo "Backup committed locally. Remote URL not configured."
    echo "To push to remote, set REMOTE_URL environment variable or configure git remote."
fi

echo "[$DATE] Backup process completed." >> "$BACKUP_LOG"
