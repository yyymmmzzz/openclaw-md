#!/usr/bin/env python3
"""
记忆系统演示脚本
展示向量记忆和知识图谱的基本用法
"""

import sys
import os

# 添加scripts目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def demo_vector_memory():
    """演示向量记忆"""
    print("=" * 60)
    print("🧠 演示1: 向量记忆（语义搜索）")
    print("=" * 60)
    
    try:
        from memory_store import ChineseMemory
        
        memory = ChineseMemory()
        
        # 存储几条记忆
        print("\n📥 存储记忆...")
        memories = [
            ("老板喜欢吃川菜，特别是麻辣火锅", "preference", 0.9),
            ("老板不喜欢吃香菜", "preference", 0.8),
            ("扣子虾是老板的AI助手", "fact", 1.0),
            ("我们决定使用飞书作为协作平台", "decision", 0.95),
        ]
        
        for text, cat, imp in memories:
            result = memory.store(text, category=cat, importance=imp)
            status = "✅" if result["status"] == "success" else "⚠️"
            print(f"  {status} {text[:30]}...")
        
        # 语义搜索
        print("\n🔍 语义搜索示例:")
        queries = [
            "老板的饮食偏好",
            "老板讨厌什么",
            "扣子虾是什么",
            "我们做了什么决定",
        ]
        
        for query in queries:
            print(f"\n  查询: '{query}'")
            results = memory.search(query, limit=2, min_score=0.3)
            if results:
                for r in results:
                    print(f"    → {r['text']} (相似度: {r['score']:.1%})")
            else:
                print("    → 未找到相关记忆")
        
    except Exception as e:
        print(f"❌ 向量记忆演示失败: {e}")
        print("   提示: 首次运行需要下载BGE模型（约1.5GB）")


def demo_knowledge_graph():
    """演示知识图谱"""
    print("\n" + "=" * 60)
    print("🕸️  演示2: 知识图谱（结构化查询）")
    print("=" * 60)
    
    try:
        from knowledge_graph import FeishuKnowledgeGraph
        
        kg = FeishuKnowledgeGraph()
        
        # 检查是否配置了Bitable
        if not kg.app_token:
            print("\n⚠️ 未配置飞书Bitable，跳过知识图谱演示")
            print("   请运行: python3 init_bitable.py --app-id xxx --app-secret xxx")
            return
        
        print("\n📥 存储三元组...")
        triples = [
            ("老板", "喜欢吃", "川菜", 0.95),
            ("老板", "特别喜欢", "麻辣火锅", 0.90),
            ("老板", "不喜欢", "香菜", 0.85),
            ("扣子虾", "是", "AI助手", 1.0),
            ("扣子虾", "服务于", "老板", 1.0),
        ]
        
        for s, p, o, c in triples:
            try:
                kg.store_triple(s, p, o, confidence=c)
                print(f"  ✅ {s} --[{p}]--> {o}")
            except Exception as e:
                print(f"  ⚠️ {s} --[{p}]--> {o} (错误: {e})")
        
        # 查询示例
        print("\n🔍 查询示例:")
        
        # 查询老板的所有信息
        print("\n  查询老板的所有信息:")
        results = kg.query(subject="老板")
        for r in results:
            print(f"    → {r['subject']} {r['predicate']} {r['object']}")
        
        # 查询特定关系
        print("\n  查询'老板喜欢吃什么':")
        results = kg.query(subject="老板", predicate="喜欢吃")
        for r in results:
            print(f"    → {r['object']}")
        
    except Exception as e:
        print(f"❌ 知识图谱演示失败: {e}")


def main():
    print("🦞 龙虾国产化记忆系统 - 功能演示")
    print("本演示展示向量语义搜索 + 知识图谱的结构化查询")
    print()
    
    demo_vector_memory()
    demo_knowledge_graph()
    
    print("\n" + "=" * 60)
    print("🎉 演示完成!")
    print("=" * 60)
    print()
    print("📖 更多用法:")
    print("  - 存储记忆: python3 memory_store.py '文本' --category preference")
    print("  - 搜索记忆: python3 memory_search.py '查询文本'")
    print("  - 存储三元组: python3 knowledge_graph.py store S P O")
    print("  - 查询三元组: python3 knowledge_graph.py query --subject S")
    print()


if __name__ == "__main__":
    main()
