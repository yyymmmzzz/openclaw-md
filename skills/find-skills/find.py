#!/usr/bin/env python3
"""
智能技能发现 - 根据需求推荐Skill
"""

import os
import sys
from pathlib import Path
from difflib import SequenceMatcher

# 技能数据库
SKILLS_DB = {
    "tavily-web-search": {
        "keywords": ["搜索", "网页", "互联网", "查找", "查询", "search", "web"],
        "description": "AI优化联网搜索，高质量网页内容提取",
        "usage": "python3 skills/tavily-web-search/search.py '查询内容'"
    },
    "coze-web-search": {
        "keywords": ["搜索", "网页", "国内", "百度", "search"],
        "description": "国内友好的网页搜索",
        "usage": "使用 coze-web-search skill"
    },
    "chinese-memory": {
        "keywords": ["记忆", "记住", "存储", "回忆", "memory", "向量"],
        "description": "国产化记忆系统，BGE中文Embedding",
        "usage": "python3 skills/chinese-memory/scripts/memory_store.py '内容'"
    },
    "summarize": {
        "keywords": ["摘要", "总结", "概括", "summarize", "summary"],
        "description": "文本摘要，支持URL、PDF、YouTube",
        "usage": "summarize 'https://example.com'"
    },
    "file-manager": {
        "keywords": ["文件", "管理", "复制", "移动", "删除", "file", "folder"],
        "description": "文件管理，读写/搜索/分类",
        "usage": "python3 skills/file-manager/manage.py [命令]"
    },
    "notification": {
        "keywords": ["通知", "提醒", "消息", "发送", "notify", "alert"],
        "description": "多渠道提醒，支持飞书/邮件等",
        "usage": "python3 skills/notification/send.py [选项]"
    },
    "task-scheduler": {
        "keywords": ["定时", "任务", "计划", "自动", "cron", "schedule"],
        "description": "定时任务自动执行",
        "usage": "python3 skills/task-scheduler/schedule.py [任务]"
    },
    "clawsec": {
        "keywords": ["安全", "审计", "检查", "security", "audit"],
        "description": "安全套件，防注入/审计",
        "usage": "python3 skills/clawsec/audit.py [检查项]"
    },
    "command-executor": {
        "keywords": ["命令", "执行", "shell", "cmd", "终端", "terminal"],
        "description": "安全执行系统命令",
        "usage": "python3 skills/command-executor/exec.py '命令'"
    },
    "healthcheck": {
        "keywords": ["健康", "检查", "状态", "health", "check"],
        "description": "系统健康检查和安全审计",
        "usage": "使用 healthcheck skill"
    },
    "weather": {
        "keywords": ["天气", "温度", "forecast", "weather"],
        "description": "获取天气和预报",
        "usage": "使用 weather skill"
    },
    "feishu-doc": {
        "keywords": ["飞书", "文档", "feishu", "doc"],
        "description": "飞书文档读写操作",
        "usage": "使用 feishu_doc 工具"
    },
    "feishu-wiki": {
        "keywords": ["飞书", "知识库", "wiki", "知识"],
        "description": "飞书知识库导航",
        "usage": "使用 feishu_wiki 工具"
    },
}

def similarity(a, b):
    """计算文本相似度"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def find_skills(query: str, top_k: int = 3):
    """
    根据查询推荐技能
    
    Args:
        query: 用户描述
        top_k: 返回前K个结果
    """
    scores = []
    
    for skill_name, skill_info in SKILLS_DB.items():
        score = 0
        
        # 关键词匹配
        for keyword in skill_info["keywords"]:
            if keyword.lower() in query.lower():
                score += 0.3
            # 相似度匹配
            score += similarity(query, keyword) * 0.2
        
        # 描述匹配
        score += similarity(query, skill_info["description"]) * 0.5
        
        if score > 0:
            scores.append((skill_name, score, skill_info))
    
    # 排序
    scores.sort(key=lambda x: x[1], reverse=True)
    
    return scores[:top_k]

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="智能技能发现")
    parser.add_argument("query", help="描述你想做什么")
    parser.add_argument("--top", type=int, default=3, help="返回结果数量")
    
    args = parser.parse_args()
    
    print(f"🔍 根据描述查找技能: \"{args.query}\"")
    print()
    
    results = find_skills(args.query, args.top)
    
    if not results:
        print("❌ 未找到匹配的技能")
        print("\n建议:")
        print("- 尝试使用不同的关键词")
        print("- 查看所有可用技能: openclaw skills list")
    else:
        print(f"✅ 找到 {len(results)} 个相关技能:\n")
        
        for i, (name, score, info) in enumerate(results, 1):
            match_level = "🟢" if score > 0.6 else "🟡" if score > 0.3 else "⚪"
            print(f"{i}. {match_level} {name}")
            print(f"   描述: {info['description']}")
            print(f"   用法: {info['usage']}")
            print(f"   匹配度: {score:.1%}")
            print()
