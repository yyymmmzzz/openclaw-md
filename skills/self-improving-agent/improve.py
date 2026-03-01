#!/usr/bin/env python3
"""
自我改进Agent
分析历史对话，持续优化
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime
from collections import Counter

SESSIONS_DIR = Path.home() / ".openclaw" / "agents" / "main" / "sessions"
IMPROVEMENTS_FILE = Path.home() / ".openclaw" / "improvements.json"

def load_sessions(limit=10):
    """加载最近的会话"""
    if not SESSIONS_DIR.exists():
        return []
    
    sessions = []
    for file in sorted(SESSIONS_DIR.glob("*.jsonl"), reverse=True)[:limit]:
        try:
            with open(file) as f:
                lines = f.readlines()
                messages = [json.loads(line) for line in lines if line.strip()]
                sessions.append({
                    "file": file.name,
                    "messages": messages
                })
        except:
            pass
    
    return sessions

def analyze_sessions(sessions):
    """分析会话模式"""
    print(f"🔍 分析 {len(sessions)} 个会话...\n")
    
    stats = {
        "total_messages": 0,
        "user_messages": 0,
        "assistant_messages": 0,
        "tool_calls": 0,
        "avg_response_length": [],
        "common_keywords": [],
    }
    
    keywords = []
    
    for session in sessions:
        for msg in session["messages"]:
            stats["total_messages"] += 1
            
            if msg.get("message", {}).get("role") == "user":
                stats["user_messages"] += 1
                content = msg.get("message", {}).get("content", [])
                for c in content:
                    if c.get("type") == "text":
                        text = c.get("text", "")
                        keywords.extend(text.lower().split())
                        
            elif msg.get("message", {}).get("role") == "assistant":
                stats["assistant_messages"] += 1
                content = msg.get("message", {}).get("content", [])
                for c in content:
                    if c.get("type") == "text":
                        text = c.get("text", "")
                        stats["avg_response_length"].append(len(text))
            
            # 检查工具调用
            for c in msg.get("message", {}).get("content", []):
                if c.get("type") == "toolCall":
                    stats["tool_calls"] += 1
    
    # 统计关键词
    common_words = Counter(keywords).most_common(20)
    stats["common_keywords"] = common_words
    
    # 计算平均响应长度
    if stats["avg_response_length"]:
        stats["avg_response_length"] = sum(stats["avg_response_length"]) / len(stats["avg_response_length"])
    
    return stats

def generate_suggestions(stats):
    """生成改进建议"""
    suggestions = []
    
    # 基于统计生成建议
    if stats["tool_calls"] > stats["user_messages"] * 2:
        suggestions.append({
            "category": "效率",
            "issue": "工具调用次数过多",
            "suggestion": "尝试批量处理或优化工具使用策略"
        })
    
    if stats["avg_response_length"] > 2000:
        suggestions.append({
            "category": "简洁性",
            "issue": "响应过长",
            "suggestion": "尝试更简洁的回复，突出重点"
        })
    
    if stats["avg_response_length"] < 100:
        suggestions.append({
            "category": "详细度",
            "issue": "响应过短",
            "suggestion": "提供更多细节和上下文"
        })
    
    # 常见关键词分析
    task_keywords = ["错误", "失败", "问题", "bug", "无法"]
    if any(kw in [w[0] for w in stats["common_keywords"]] for kw in task_keywords):
        suggestions.append({
            "category": "错误处理",
            "issue": "用户经常报告问题",
            "suggestion": "加强错误处理和预防性提示"
        })
    
    return suggestions

def save_improvements(suggestions):
    """保存改进建议"""
    data = {
        "generated_at": datetime.now().isoformat(),
        "suggestions": suggestions
    }
    
    with open(IMPROVEMENTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_improvements():
    """加载改进建议"""
    if IMPROVEMENTS_FILE.exists():
        with open(IMPROVEMENTS_FILE) as f:
            return json.load(f)
    return None

def print_report(stats, suggestions):
    """打印分析报告"""
    print("=" * 60)
    print("📊 自我改进分析报告")
    print("=" * 60)
    print()
    
    print("📈 会话统计:")
    print(f"   总消息数: {stats['total_messages']}")
    print(f"   用户消息: {stats['user_messages']}")
    print(f"   助手回复: {stats['assistant_messages']}")
    print(f"   工具调用: {stats['tool_calls']}")
    if stats['avg_response_length']:
        print(f"   平均响应长度: {stats['avg_response_length']:.0f}字符")
    print()
    
    print("🔥 常见关键词:")
    for word, count in stats['common_keywords'][:10]:
        if len(word) > 2:  # 忽略短词
            print(f"   {word}: {count}次")
    print()
    
    print("💡 改进建议:")
    for i, s in enumerate(suggestions, 1):
        print(f"   {i}. [{s['category']}] {s['issue']}")
        print(f"      → {s['suggestion']}")
        print()
    
    print("=" * 60)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="自我改进Agent")
    parser.add_argument("command", choices=["analyze", "suggest", "report", "apply"],
                       help="命令")
    parser.add_argument("--sessions", type=int, default=10, help="分析的会话数量")
    parser.add_argument("--category", help="应用改进的类别")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        sessions = load_sessions(args.sessions)
        if not sessions:
            print("❌ 未找到会话数据")
            sys.exit(1)
        
        stats = analyze_sessions(sessions)
        suggestions = generate_suggestions(stats)
        save_improvements(suggestions)
        
        print(f"✅ 分析了 {len(sessions)} 个会话")
        print(f"✅ 生成了 {len(suggestions)} 条改进建议")
        print(f"📁 已保存到: {IMPROVEMENTS_FILE}")
    
    elif args.command == "suggest":
        improvements = load_improvements()
        if not improvements:
            print("❌ 请先运行 analyze 生成建议")
            sys.exit(1)
        
        print("💡 改进建议:\n")
        for i, s in enumerate(improvements["suggestions"], 1):
            print(f"{i}. [{s['category']}] {s['issue']}")
            print(f"   → {s['suggestion']}\n")
    
    elif args.command == "report":
        sessions = load_sessions(args.sessions)
        stats = analyze_sessions(sessions)
        suggestions = generate_suggestions(stats)
        print_report(stats, suggestions)
    
    elif args.command == "apply":
        print("📝 应用改进...")
        print("注: 此功能需要手动审查和应用建议")
        print(f"请查看: {IMPROVEMENTS_FILE}")
