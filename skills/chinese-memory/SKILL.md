---
name: chinese-memory
description: 国产化记忆系统 - 使用BGE中文Embedding模型 + 飞书Bitable知识图谱，实现零国外依赖的智能记忆。支持向量语义搜索和结构化知识存储。
---

# Chinese Memory - 国产化记忆系统

基于中文Embedding模型（BGE）和飞书Bitable的国产记忆系统，完全替代OpenAI依赖。

## 功能特点

1. **向量语义搜索**（阶段一）
   - 使用BAAI/bge-large-zh-v1.5中文Embedding模型
   - 本地运行，无需国外API
   - LanceDB向量数据库存储
   - 支持语义相似度搜索

2. **知识图谱**（阶段二）
   - 飞书Bitable存储三元组（Subject-Predicate-Object）
   - 支持简单推理查询
   - 与向量记忆互补

## 安装依赖

```bash
# 安装Python依赖
pip install sentence-transformers lancedb numpy

# 首次运行会自动下载BGE模型（约1.5GB）
```

## 使用方法

### 存储记忆
```python
# 向量记忆（语义搜索）
store_vector_memory("老板喜欢吃川菜，特别是火锅")

# 知识图谱（结构化事实）
store_knowledge_triple("老板", "喜欢吃", "川菜")
store_knowledge_triple("老板", "特别喜欢", "火锅")
```

### 搜索记忆
```python
# 语义搜索
search_vector_memory("老板的饮食偏好")

# 知识图谱查询
query_knowledge_graph(subject="老板", predicate="喜欢吃")
```

## 文件结构

```
chinese-memory/
├── SKILL.md
├── scripts/
│   ├── memory_store.py      # 存储记忆
│   ├── memory_search.py     # 搜索记忆
│   ├── knowledge_graph.py   # 知识图谱操作
│   └── init_bitable.py      # 初始化飞书Bitable
└── references/
    └── bitable_schema.md    # Bitable表结构说明
```

## 配置

编辑 `~/.openclaw/config.json`：

```json
{
  "chinese-memory": {
    "embedding_model": "BAAI/bge-large-zh-v1.5",
    "vector_db_path": "~/.openclaw/memory/vectors",
    "bitable_app_token": "your_bitable_token",
    "use_local_model": true
  }
}
```

## 工作原理

### 向量记忆流程
```
用户输入 → BGE Embedding → 向量 → LanceDB存储
                              ↓
查询输入 → BGE Embedding → 向量 → 相似度搜索 → 返回相关记忆
```

### 知识图谱流程
```
提取三元组 → 飞书Bitable存储
                  ↓
查询条件 → Bitable筛选 → 返回结构化知识
```

## 与原版对比

| 特性 | OpenAI版 | 国产版(本Skill) |
|-----|---------|---------------|
| Embedding模型 | text-embedding-3-small | BGE-large-zh |
| 成本 | $0.0001/次 | ¥0（本地） |
| 网络依赖 | 需要国外网络 | 纯国内 |
| 中文效果 | 良好 | 优秀（专为中文优化） |
| 隐私 | 上传到OpenAI | 完全本地 |

## 注意

- 首次下载BGE模型需要约1.5GB磁盘空间和良好网络
- 推荐使用16GB内存机器运行large模型，8GB可运行base模型
- Bitable需要提前创建，使用init_bitable.py初始化
