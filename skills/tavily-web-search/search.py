#!/usr/bin/env python3
"""
Tavily AI搜索 - 高质量网页搜索
"""

import os
import sys
import json
from pathlib import Path

try:
    from tavily import TavilyClient
except ImportError:
    print("请先安装依赖: pip install tavily-python")
    sys.exit(1)

CONFIG_PATH = Path.home() / ".openclaw" / "config.json"

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f).get("tavily-web-search", {})
    return {}

def search(query: str, depth: str = "basic", include_answer: bool = True):
    """
    执行Tavily搜索
    
    Args:
        query: 搜索查询
        depth: 搜索深度 (basic/advanced)
        include_answer: 是否包含AI生成的答案
    """
    config = load_config()
    api_key = config.get("api_key") or os.environ.get("TAVILY_API_KEY")
    
    if not api_key:
        print("错误: 请配置Tavily API Key")
        print("获取API Key: https://tavily.com")
        return
    
    client = TavilyClient(api_key=api_key)
    
    try:
        response = client.search(
            query=query,
            search_depth=depth,
            include_answer=include_answer,
            include_images=False,
            max_results=10
        )
        
        # 格式化输出
        print(f"🔍 搜索: {query}")
        print(f"⏱️  耗时: {response.get('response_time', 0):.2f}秒")
        print()
        
        if include_answer and response.get("answer"):
            print("🤖 AI总结:")
            print(response["answer"])
            print()
        
        print("📄 相关结果:")
        for i, result in enumerate(response.get("results", []), 1):
            print(f"\n{i}. {result['title']}")
            print(f"   URL: {result['url']}")
            print(f"   内容: {result['content'][:200]}...")
            print(f"   相关度: {result.get('score', 0):.2f}")
        
        return response
        
    except Exception as e:
        print(f"搜索失败: {e}")
        return None

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Tavily AI搜索")
    parser.add_argument("query", help="搜索查询")
    parser.add_argument("--depth", choices=["basic", "advanced"], default="basic", help="搜索深度")
    parser.add_argument("--no-answer", action="store_true", help="不包含AI答案")
    
    args = parser.parse_args()
    
    search(args.query, args.depth, not args.no_answer)
