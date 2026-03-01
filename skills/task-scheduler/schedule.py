#!/usr/bin/env python3
"""
定时任务调度器
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from croniter import croniter

TASKS_FILE = Path.home() / ".openclaw" / "tasks.json"

def load_tasks():
    if TASKS_FILE.exists():
        with open(TASKS_FILE) as f:
            return json.load(f)
    return {}

def save_tasks(tasks):
    TASKS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

def add_task(name: str, command: str, cron: str):
    """添加定时任务"""
    try:
        # 验证cron表达式
        croniter(cron)
    except Exception as e:
        print(f"❌ 无效的cron表达式: {e}")
        return False
    
    tasks = load_tasks()
    tasks[name] = {
        "command": command,
        "cron": cron,
        "created": datetime.now().isoformat(),
        "last_run": None,
        "run_count": 0
    }
    save_tasks(tasks)
    
    print(f"✅ 任务已添加: {name}")
    print(f"   命令: {command}")
    print(f"   周期: {cron}")
    print(f"   下次执行: {croniter(cron).get_next(datetime)}")
    return True

def list_tasks():
    """列出所有任务"""
    tasks = load_tasks()
    
    if not tasks:
        print("📭 暂无定时任务")
        return
    
    print(f"📋 定时任务列表 ({len(tasks)}个):\n")
    print(f"{'名称':<20} {'Cron':<15} {'上次执行':<20} {'执行次数'}")
    print("-" * 70)
    
    for name, task in tasks.items():
        last_run = task.get("last_run", "从未") or "从未"
        if last_run != "从未":
            try:
                last_run = datetime.fromisoformat(last_run).strftime("%m-%d %H:%M")
            except:
                pass
        print(f"{name:<20} {task['cron']:<15} {last_run:<20} {task.get('run_count', 0)}")

def remove_task(name: str):
    """删除任务"""
    tasks = load_tasks()
    
    if name not in tasks:
        print(f"❌ 任务不存在: {name}")
        return False
    
    del tasks[name]
    save_tasks(tasks)
    print(f"✅ 任务已删除: {name}")
    return True

def run_task(name: str):
    """立即执行任务"""
    tasks = load_tasks()
    
    if name not in tasks:
        print(f"❌ 任务不存在: {name}")
        return False
    
    task = tasks[name]
    print(f"🚀 执行任务: {name}")
    print(f"   命令: {task['command']}")
    print()
    
    try:
        result = subprocess.run(
            task['command'],
            shell=True,
            capture_output=True,
            text=True,
            timeout=300
        )
        
        # 更新执行记录
        task["last_run"] = datetime.now().isoformat()
        task["run_count"] = task.get("run_count", 0) + 1
        tasks[name] = task
        save_tasks(tasks)
        
        if result.returncode == 0:
            print("✅ 执行成功")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ 执行失败")
            if result.stderr:
                print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 执行出错: {e}")
        return False

def check_and_run():
    """检查并执行到期的任务"""
    tasks = load_tasks()
    now = datetime.now()
    
    for name, task in tasks.items():
        cron = task.get("cron")
        last_run = task.get("last_run")
        
        if last_run:
            last_run_time = datetime.fromisoformat(last_run)
        else:
            last_run_time = datetime.min
        
        # 检查是否应该执行
        itr = croniter(cron, last_run_time)
        next_run = itr.get_next(datetime)
        
        if now >= next_run:
            print(f"⏰ 任务到期: {name}")
            run_task(name)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="定时任务调度器")
    parser.add_argument("command", choices=["add", "list", "remove", "run", "check"],
                       help="命令")
    parser.add_argument("name", nargs="?", help="任务名称")
    parser.add_argument("--cmd", "--command", dest="command_str", help="要执行的命令")
    parser.add_argument("--cron", help="cron表达式")
    
    args = parser.parse_args()
    
    if args.command == "add":
        if not args.name or not args.command_str or not args.cron:
            print("用法: add <名称> --command '命令' --cron '表达式'")
            sys.exit(1)
        add_task(args.name, args.command_str, args.cron)
    
    elif args.command == "list":
        list_tasks()
    
    elif args.command == "remove":
        if not args.name:
            print("用法: remove <名称>")
            sys.exit(1)
        remove_task(args.name)
    
    elif args.command == "run":
        if not args.name:
            print("用法: run <名称>")
            sys.exit(1)
        run_task(args.name)
    
    elif args.command == "check":
        check_and_run()
