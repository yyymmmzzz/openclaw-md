#!/bin/bash
# 记忆系统生命周期管理脚本
# 运行频率：每日一次（通过 heartbeat 触发）

set -e

WORKSPACE_DIR="/workspace/projects/workspace"
MEMORY_DIR="$WORKSPACE_DIR/memory"
LOG_FILE="$MEMORY_DIR/.lifecycle-log"
CURRENT_TIME=$(date +%s)
CURRENT_DATE=$(date "+%Y-%m-%d")

echo "🧹 记忆系统生命周期管理 - $CURRENT_DATE" | tee -a "$LOG_FILE"
echo "================================" | tee -a "$LOG_FILE"

# ==================== 配置 ====================

# working/ 目录：1天生命周期
WORKING_MAX_AGE_DAYS=1
WORKING_MAX_AGE_SECONDS=$((WORKING_MAX_AGE_DAYS * 86400))

# short-term/conversations/ 目录：30天生命周期  
CONVERSATION_MAX_AGE_DAYS=30
CONVERSATION_MAX_AGE_SECONDS=$((CONVERSATION_MAX_AGE_DAYS * 86400))

# short-term/tasks/completed/ 目录：90天生命周期
COMPLETED_TASK_MAX_AGE_DAYS=90
COMPLETED_TASK_MAX_AGE_SECONDS=$((COMPLETED_TASK_MAX_AGE_DAYS * 86400))

# raw/ 目录：90天后压缩归档
RAW_MAX_AGE_DAYS=90
RAW_MAX_AGE_SECONDS=$((RAW_MAX_AGE_DAYS * 86400))

# vault/ 归档目录：365天后删除（1年）
VAULT_MAX_AGE_DAYS=365
VAULT_MAX_AGE_SECONDS=$((VAULT_MAX_AGE_DAYS * 86400))

# ==================== 函数 ====================

get_file_age_days() {
    local file="$1"
    local file_time=$(stat -c %Y "$file" 2>/dev/null || echo 0)
    local age_seconds=$((CURRENT_TIME - file_time))
    echo $((age_seconds / 86400))
}

get_file_age_seconds() {
    local file="$1"
    local file_time=$(stat -c %Y "$file" 2>/dev/null || echo 0)
    echo $((CURRENT_TIME - file_time))
}

# ==================== 1. 清理 working/ 目录 ====================
echo "" | tee -a "$LOG_FILE"
echo "📂 [1/5] 清理 working/ 目录 (保留 $WORKING_MAX_AGE_DAYS 天)" | tee -a "$LOG_FILE"

if [ -d "$MEMORY_DIR/working" ]; then
    WORKING_CLEANED=0
    find "$MEMORY_DIR/working" -type f -name "*.md" 2>/dev/null | while IFS= read -r file; do
        [ -z "$file" ] && continue
        age=$(get_file_age_seconds "$file")
        if [ $age -gt $WORKING_MAX_AGE_SECONDS ]; then
            echo "  🗑️  删除: $(basename "$file") (已存在 $((age/86400)) 天)" | tee -a "$LOG_FILE"
            rm "$file"
            WORKING_CLEANED=$((WORKING_CLEANED + 1))
        fi
    done
    
    if [ $WORKING_CLEANED -eq 0 ]; then
        echo "  ✅ 无需清理" | tee -a "$LOG_FILE"
    else
        echo "  ✓ 清理完成: $WORKING_CLEANED 个文件" | tee -a "$LOG_FILE"
    fi
else
    echo "  ⚠️ 目录不存在" | tee -a "$LOG_FILE"
fi

# ==================== 2. 归档 short-term/conversations/ ====================
echo "" | tee -a "$LOG_FILE"
echo "📂 [2/5] 归档短期对话 (超过 $CONVERSATION_MAX_AGE_DAYS 天)" | tee -a "$LOG_FILE"

mkdir -p "$MEMORY_DIR/vault/conversations"

if [ -d "$MEMORY_DIR/short-term/conversations" ]; then
    CONV_ARCHIVED=0
    find "$MEMORY_DIR/short-term/conversations" -type f -name "*.md" 2>/dev/null | while IFS= read -r file; do
        [ -z "$file" ] && continue
        age=$(get_file_age_seconds "$file")
        if [ $age -gt $CONVERSATION_MAX_AGE_SECONDS ]; then
            filename=$(basename "$file")
            echo "  📦 归档: $filename (已存在 $((age/86400)) 天)" | tee -a "$LOG_FILE"
            mv "$file" "$MEMORY_DIR/vault/conversations/"
            CONV_ARCHIVED=$((CONV_ARCHIVED + 1))
        fi
    done
    
    if [ $CONV_ARCHIVED -eq 0 ]; then
        echo "  ✅ 无需归档" | tee -a "$LOG_FILE"
    else
        echo "  ✓ 归档完成: $CONV_ARCHIVED 个文件" | tee -a "$LOG_FILE"
    fi
else
    echo "  ⚠️ 目录不存在" | tee -a "$LOG_FILE"
fi

# ==================== 3. 归档已完成的任务 ====================
echo "" | tee -a "$LOG_FILE"
echo "📂 [3/5] 归档已完成任务 (超过 $COMPLETED_TASK_MAX_AGE_DAYS 天)" | tee -a "$LOG_FILE"

mkdir -p "$MEMORY_DIR/vault/tasks"

if [ -f "$MEMORY_DIR/short-term/tasks/completed.md" ]; then
    COMPLETED_AGE=$(get_file_age_days "$MEMORY_DIR/short-term/tasks/completed.md")
    if [ $COMPLETED_AGE -gt $COMPLETED_TASK_MAX_AGE_DAYS ]; then
        archive_name="completed-$(date -r "$MEMORY_DIR/short-term/tasks/completed.md" "+%Y-%m").md"
        echo "  📦 归档 completed.md → $archive_name (已存在 ${COMPLETED_AGE} 天)" | tee -a "$LOG_FILE"
        mv "$MEMORY_DIR/short-term/tasks/completed.md" "$MEMORY_DIR/vault/tasks/$archive_name"
        echo "  ✓ 已归档" | tee -a "$LOG_FILE"
    else
        echo "  ✅ 无需归档 (仅 ${COMPLETED_AGE} 天)" | tee -a "$LOG_FILE"
    fi
else
    echo "  ℹ️ completed.md 不存在" | tee -a "$LOG_FILE"
fi

# ==================== 4. 压缩 raw/ 目录 ====================
echo "" | tee -a "$LOG_FILE"
echo "📂 [4/5] 压缩原始记录 (超过 $RAW_MAX_AGE_DAYS 天)" | tee -a "$LOG_FILE"

mkdir -p "$MEMORY_DIR/vault/raw"

if [ -d "$MEMORY_DIR/raw" ]; then
    RAW_COMPRESSED=0
    # 遍历 raw/ 下的所有子目录（按月份组织）
    find "$MEMORY_DIR/raw" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | while IFS= read -r month_dir; do
        [ -z "$month_dir" ] && continue
        age=$(get_file_age_seconds "$month_dir")
        if [ $age -gt $RAW_MAX_AGE_SECONDS ]; then
            dirname=$(basename "$month_dir")
            echo "  🗜️  压缩: $dirname/ (已存在 $((age/86400)) 天)" | tee -a "$LOG_FILE"
            
            # 压缩为 tar.gz
            tar -czf "$MEMORY_DIR/vault/raw/${dirname}.tar.gz" -C "$MEMORY_DIR/raw" "$dirname"
            
            # 删除原目录
            rm -rf "$month_dir"
            
            RAW_COMPRESSED=$((RAW_COMPRESSED + 1))
        fi
    done
    
    if [ $RAW_COMPRESSED -eq 0 ]; then
        echo "  ✅ 无需压缩" | tee -a "$LOG_FILE"
    else
        echo "  ✓ 压缩完成: $RAW_COMPRESSED 个目录" | tee -a "$LOG_FILE"
    fi
else
    echo "  ⚠️ 目录不存在" | tee -a "$LOG_FILE"
fi

# ==================== 5. 清理 vault/ 中过旧的归档 ====================
echo "" | tee -a "$LOG_FILE"
echo "📂 [5/5] 清理 vault/ 过期归档 (超过 $VAULT_MAX_AGE_DAYS 天)" | tee -a "$LOG_FILE"

if [ -d "$MEMORY_DIR/vault" ]; then
    VAULT_CLEANED=0
    find "$MEMORY_DIR/vault" -type f 2>/dev/null | while IFS= read -r file; do
        [ -z "$file" ] && continue
        age=$(get_file_age_seconds "$file")
        if [ $age -gt $VAULT_MAX_AGE_SECONDS ]; then
            echo "  🗑️  删除: $(basename "$file") (已存在 $((age/86400)) 天，超过1年)" | tee -a "$LOG_FILE"
            rm -rf "$file"
            VAULT_CLEANED=$((VAULT_CLEANED + 1))
        fi
    done
    
    if [ $VAULT_CLEANED -eq 0 ]; then
        echo "  ✅ 无需清理" | tee -a "$LOG_FILE"
    else
        echo "  ✓ 清理完成: $VAULT_CLEANED 个文件" | tee -a "$LOG_FILE"
    fi
else
    echo "  ⚠️ 目录不存在" | tee -a "$LOG_FILE"
fi

# ==================== 6. 更新统计信息 ====================
echo "" | tee -a "$LOG_FILE"
echo "📊 [统计] 更新记忆系统状态" | tee -a "$LOG_FILE"

# 计算各目录文件数
WORKING_COUNT=$(find "$MEMORY_DIR/working" -type f 2>/dev/null | wc -l)
SHORT_TERM_COUNT=$(find "$MEMORY_DIR/short-term" -type f 2>/dev/null | wc -l)
LONG_TERM_COUNT=$(find "$MEMORY_DIR/long-term" -type f 2>/dev/null | wc -l)
RAW_COUNT=$(find "$MEMORY_DIR/raw" -type f 2>/dev/null | wc -l)
VAULT_COUNT=$(find "$MEMORY_DIR/vault" -type f 2>/dev/null | wc -l)

echo "  📁 working/: $WORKING_COUNT 文件" | tee -a "$LOG_FILE"
echo "  📁 short-term/: $SHORT_TERM_COUNT 文件" | tee -a "$LOG_FILE"
echo "  📁 long-term/: $LONG_TERM_COUNT 文件" | tee -a "$LOG_FILE"
echo "  📁 raw/: $RAW_COUNT 文件" | tee -a "$LOG_FILE"
echo "  📁 vault/: $VAULT_COUNT 文件" | tee -a "$LOG_FILE"

# 更新 memory/index.md 中的统计（简单替换）
if [ -f "$MEMORY_DIR/index.md" ]; then
    # 使用临时文件更新统计
    sed -i "s/- 工作记忆: .*/- 工作记忆: $WORKING_COUNT 文件/" "$MEMORY_DIR/index.md" 2>/dev/null || true
    sed -i "s/- 短期记忆: .*/- 短期记忆: $SHORT_TERM_COUNT 文件/" "$MEMORY_DIR/index.md" 2>/dev/null || true
    sed -i "s/- 长期记忆: .*/- 长期记忆: $LONG_TERM_COUNT 文件/" "$MEMORY_DIR/index.md" 2>/dev/null || true
    echo "  ✓ 已更新 index.md 统计" | tee -a "$LOG_FILE"
fi

# ==================== 完成 ====================
echo "" | tee -a "$LOG_FILE"
echo "✅ 生命周期管理完成！" | tee -a "$LOG_FILE"
echo "下次运行: $(date -d "+1 day" "+%Y-%m-%d %H:%M:%S")" | tee -a "$LOG_FILE"
echo "================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"
