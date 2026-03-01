#!/usr/bin/env python3
"""
向量记忆搜索模块
使用BGE中文Embedding模型 + LanceDB
"""

import os
import sys
import json
from pathlib import Path

# 复用memory_store中的类
from memory_store import ChineseMemory


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="搜索向量记忆")
    parser.add_argument("query", help="查询文本")
    parser.add_argument("--limit", type=int, default=5, help="返回结果数量")
    parser.add_argument("--min-score", type=float, default=0.5, help="最小相似度阈值")
    parser.add_argument("--format", choices=["json", "text"], default="text", help="输出格式")
    
    args = parser.parse_args()
    
    memory = ChineseMemory()
    results = memory.search(args.query, limit=args.limit, min_score=args.min_score)
    
    if args.format == "json":
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        # 文本格式输出
        if not results:
            print("未找到相关记忆")
            return
        
        print(f"找到 {len(results)} 条相关记忆：")
        print("-" * 50)
        for i, r in enumerate(results, 1):
            print(f"{i}. [{r['category']}] {r['text']}")
            print(f"   相似度: {r['score']:.1%} | 重要度: {r['importance']}")
            print()


if __name__ == "__main__":
    main()
