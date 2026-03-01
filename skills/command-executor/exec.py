#!/usr/bin/env python3
"""
安全命令执行器
"""

import os
import sys
import subprocess
import shlex
from datetime import datetime
from pathlib import Path

# 危险命令模式
DANGEROUS_PATTERNS = [
    "rm -rf /",
    "rm -rf /*",
    "> /dev/sda",
    "dd if=/dev/zero",
    "mkfs.",
    ":(){:|:&};:", # fork bomb
]

# 需要确认的命令
CONFIRM_PATTERNS = [
    "rm -r",
    "rm -f",
    "drop",
    "delete",
    "chmod 777",
]

LOG_FILE = Path.home() / ".openclaw" / "command_log.txt"

class CommandExecutor:
    def __init__(self, dry_run=False, force=False, timeout=60):
        self.dry_run = dry_run
        self.force = force
        self.timeout = timeout
    
    def is_dangerous(self, command: str) -> bool:
        """检查是否危险命令"""
        cmd_lower = command.lower()
        for pattern in DANGEROUS_PATTERNS:
            if pattern.lower() in cmd_lower:
                return True
        return False
    
    def needs_confirm(self, command: str) -> bool:
        """检查是否需要确认"""
        cmd_lower = command.lower()
        for pattern in CONFIRM_PATTERNS:
            if pattern.lower() in cmd_lower:
                return True
        return False
    
    def log(self, command: str, status: str, output: str = ""):
        """记录执行日志"""
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.now()}] {status}: {command}\n")
            if output:
                f.write(f"  Output: {output[:200]}...\n")
    
    def execute(self, command: str) -> bool:
        """执行命令"""
        print(f"📝 命令: {command}")
        
        # 检查危险命令
        if self.is_dangerous(command):
            print("❌ 检测到危险命令，已阻止")
            self.log(command, "BLOCKED")
            return False
        
        # 检查是否需要确认
        if not self.force and self.needs_confirm(command):
            confirm = input("⚠️  此命令可能有风险，确认执行? [y/N]: ")
            if confirm.lower() != 'y':
                print("已取消")
                return False
        
        # dry-run模式
        if self.dry_run:
            print("[DRY-RUN] 模拟执行，不实际运行")
            return True
        
        # 执行命令
        print(f"🚀 执行中... (超时: {self.timeout}s)")
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if result.returncode == 0:
                print("✅ 执行成功")
                if result.stdout:
                    print(result.stdout)
                self.log(command, "SUCCESS", result.stdout)
                return True
            else:
                print("❌ 执行失败")
                if result.stderr:
                    print(result.stderr)
                self.log(command, "FAILED", result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print(f"⏱️  执行超时 (> {self.timeout}s)")
            self.log(command, "TIMEOUT")
            return False
        except Exception as e:
            print(f"❌ 执行错误: {e}")
            self.log(command, "ERROR", str(e))
            return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="安全命令执行器")
    parser.add_argument("command", help="要执行的命令")
    parser.add_argument("-f", "--force", action="store_true", help="强制执行，无需确认")
    parser.add_argument("-d", "--dry-run", action="store_true", help="模拟执行")
    parser.add_argument("-t", "--timeout", type=int, default=60, help="超时时间(秒)")
    
    args = parser.parse_args()
    
    executor = CommandExecutor(
        dry_run=args.dry_run,
        force=args.force,
        timeout=args.timeout
    )
    
    success = executor.execute(args.command)
    sys.exit(0 if success else 1)
