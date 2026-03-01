#!/usr/bin/env python3
"""
安全的文件编辑工具（带自动重试）
"""

import sys
sys.path.insert(0, '/workspace/projects/workspace/scripts')
from retry_mechanism import retry_edit_file, retry_task

def safe_edit_file(file_path, old_text, new_text, max_attempts=3):
    """
    安全编辑文件（带自动重试）
    
    Args:
        file_path: 文件路径
        old_text: 要替换的原文本
        new_text: 新文本
        max_attempts: 最大重试次数
    
    Returns:
        (success, message)
    """
    def edit_func(content):
        if old_text not in content:
            raise ValueError(f"找不到要替换的文本: {old_text[:50]}...")
        return content.replace(old_text, new_text)
    
    result = retry_edit_file(file_path, edit_func, max_attempts)
    
    if result[0]:
        return (True, f"✅ 文件编辑成功（尝试{result[2]}次）")
    else:
        return (False, f"❌ 文件编辑失败: {str(result[2])}")

def safe_write_file(file_path, content, max_attempts=3):
    """
    安全写入文件（带自动重试）
    """
    def task():
        with open(file_path, 'w') as f:
            f.write(content)
        return True
    
    success, result, error = retry_task(
        task, 
        f"写入文件 {file_path}", 
        max_attempts=max_attempts
    )
    
    if success:
        return (True, f"✅ 文件写入成功")
    else:
        return (False, f"❌ 文件写入失败: {str(error)}")

def safe_read_file(file_path, max_attempts=3):
    """
    安全读取文件（带自动重试）
    """
    def task():
        with open(file_path, 'r') as f:
            return f.read()
    
    success, result, error = retry_task(
        task,
        f"读取文件 {file_path}",
        max_attempts=max_attempts
    )
    
    if success:
        return (True, result)
    else:
        return (False, str(error))

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="安全文件操作（带重试）")
    parser.add_argument("command", choices=["edit", "write", "read"], help="操作类型")
    parser.add_argument("file", help="文件路径")
    parser.add_argument("--old", help="要替换的原文本（edit命令）")
    parser.add_argument("--new", help="新文本（edit/write命令）")
    parser.add_argument("--attempts", type=int, default=3, help="最大重试次数")
    
    args = parser.parse_args()
    
    if args.command == "edit":
        if not args.old or not args.new:
            print("❌ edit命令需要 --old 和 --new 参数")
            sys.exit(1)
        success, msg = safe_edit_file(args.file, args.old, args.new, args.attempts)
        print(msg)
    
    elif args.command == "write":
        if not args.new:
            print("❌ write命令需要 --new 参数")
            sys.exit(1)
        success, msg = safe_write_file(args.file, args.new, args.attempts)
        print(msg)
    
    elif args.command == "read":
        success, result = safe_read_file(args.file, args.attempts)
        if success:
            print(result)
        else:
            print(f"❌ 读取失败: {result}")
