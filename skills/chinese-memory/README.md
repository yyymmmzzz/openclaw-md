# 龙虾国产化记忆系统 - 完整文档

## 🎯 系统概述

国产版记忆系统，完全替代 OpenAI 依赖：
- **向量记忆**: BGE中文Embedding + LanceDB本地存储
- **知识图谱**: 飞书Bitable三元组存储

## 📁 文件结构

```
chinese-memory/
├── SKILL.md                          # Skill主文档
├── scripts/
│   ├── setup.sh                      # 安装脚本
│   ├── memory_store.py               # 存储向量记忆
│   ├── memory_search.py              # 搜索向量记忆
│   ├── knowledge_graph.py            # 知识图谱操作
│   └── init_bitable.py               # 初始化Bitable
└── references/
    └── bitable_schema.md             # Bitable表结构说明
```

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /workspace/projects/workspace/skills/chinese-memory/scripts
bash setup.sh
```

或手动安装：
```bash
pip install sentence-transformers lancedb pyarrow requests numpy
```

### 2. 配置文件

编辑 `~/.openclaw/config.json`：

```json
{
  "chinese-memory": {
    "embedding_model": "BAAI/bge-large-zh-v1.5",
    "vector_db_path": "~/.openclaw/memory/vectors",
    "use_local_model": true,
    "bitable_app_token": "YOUR_BITABLE_APP_TOKEN",
    "bitable_table_id": "YOUR_TABLE_ID",
    "feishu_app_id": "YOUR_FEISHU_APP_ID",
    "feishu_app_secret": "YOUR_FEISHU_APP_SECRET"
  }
}
```

### 3. 初始化飞书Bitable（可选）

```bash
python3 init_bitable.py \
  --app-id cli_xxxxxx \
  --app-secret xxxxxxxxx \
  --name "龙虾记忆系统"
```

## 💾 使用示例

### 向量记忆（语义搜索）

```bash
# 存储记忆
cd /workspace/projects/workspace/skills/chinese-memory/scripts
python3 memory_store.py "老板喜欢吃川菜，特别是麻辣火锅" --category preference

# 搜索记忆（语义匹配）
python3 memory_search.py "老板的饮食偏好"
# 输出示例：
# 找到 1 条相关记忆：
# 1. [preference] 老板喜欢吃川菜，特别是麻辣火锅
#    相似度: 95.2% | 重要度: 0.7
```

### 知识图谱（结构化查询）

```bash
# 存储三元组
python3 knowledge_graph.py store 老板 喜欢吃 川菜 --confidence 0.95
python3 knowledge_graph.py store 老板 特别喜欢 麻辣火锅 --confidence 0.90

# 查询
python3 knowledge_graph.py query --subject 老板
# 输出示例：
# 找到 2 条记录：
#   老板 --[喜欢吃]--> 川菜
#   老板 --[特别喜欢]--> 麻辣火锅

# 简单推理
python3 knowledge_graph.py reason 老板 --predicate 喜欢吃
# 输出示例：
# 推理结果 (1 条)：
#   老板 --[喜欢吃]--> 川菜
```

## 🔧 核心原理

### BGE Embedding模型

```
文本输入: "老板喜欢吃川菜"
    ↓
BGE-large-zh模型编码
    ↓
输出向量: [0.12, -0.34, 0.89, ...] (1024维)
    ↓
存储到LanceDB
```

**为什么选BGE？**
- ✅ 开源免费，可本地部署
- ✅ 专为中文优化，效果超过OpenAI
- ✅ 模型轻量，16G内存可流畅运行
- ✅ 支持长文本（512 tokens）

### 向量搜索原理

```
查询: "老板爱吃什么"
    ↓
BGE编码 → 查询向量
    ↓
LanceDB向量相似度计算（L2距离）
    ↓
返回最相似的记忆
```

### 知识图谱原理

```
自然语言: "老板昨天说他爱吃火锅"
    ↓
提取三元组: (老板, 喜欢吃, 火锅)
    ↓
存储到飞书Bitable
    ↓
支持精确查询和简单推理
```

## 📊 两种记忆对比

| 特性 | 向量记忆 | 知识图谱 |
|-----|---------|---------|
| **存储内容** | 自然语言文本 | 结构化三元组 |
| **搜索方式** | 语义相似度 | 精确匹配 |
| **适用场景** | 模糊查询、语境理解 | 精确事实、关系推理 |
| **示例查询** | "老板喜欢什么" | 老板喜欢吃什么 |
| **返回结果** | 语义相关的内容 | 精确匹配的事实 |
| **存储位置** | 本地LanceDB | 飞书Bitable |

## 🔒 隐私与成本

### 隐私保护
- ✅ **数据不出境**: 全部在国内处理
- ✅ **本地存储**: 向量数据存在本地磁盘
- ✅ **可控透明**: 所有代码开源可见

### 成本对比

| 项目 | OpenAI版 | 国产版(本系统) |
|-----|---------|--------------|
| Embedding调用 | $0.0001/次 | ¥0（本地计算） |
| 向量存储 | 本地免费 | 本地免费 |
| 知识图谱存储 | 依赖外部 | 飞书Bitable免费额度 |
| 月度估算(1万次) | ~$1 | ~¥0 |

## 🛠️ 故障排除

### 问题1: 模型下载失败
```
解决方法: 设置国内镜像
export HF_ENDPOINT=https://hf-mirror.com
python3 memory_store.py ...
```

### 问题2: 内存不足
```
解决方法: 使用轻量级模型
# 修改配置，使用base模型（768维，内存占用减半）
"embedding_model": "BAAI/bge-base-zh-v1.5"
```

### 问题3: 飞书API报错
```
检查清单:
1. App ID 和 App Secret 是否正确
2. 应用是否有Bitable权限
3. 网络是否能访问飞书API
```

## 📈 性能指标

**BGE-large-zh 在中文场景的表现:**
- 语义相似度任务: 优于OpenAI text-embedding-3-small
- 编码速度: ~100条/秒 (CPU)
- 内存占用: ~1.5GB (模型加载后)
- 向量维度: 1024维

**LanceDB 性能:**
- 查询延迟: <50ms (万级数据)
- 存储效率: 每条记忆约4KB

## 🎓 进阶用法

### Python API调用

```python
# 向量记忆
from memory_store import ChineseMemory

memory = ChineseMemory()

# 存储
result = memory.store("老板周末喜欢去爬山", category="preference")

# 搜索
results = memory.search("老板的爱好", limit=3)
for r in results:
    print(f"{r['text']} (相似度: {r['score']:.1%})")

# 知识图谱
from knowledge_graph import FeishuKnowledgeGraph

kg = FeishuKnowledgeGraph()

# 存储
kg.store_triple("老板", "周末喜欢", "爬山")

# 查询
facts = kg.query(subject="老板", predicate="周末喜欢")
for f in facts:
    print(f"{f['subject']} {f['predicate']} {f['object']}")
```

## 📝 更新日志

**v1.0 (2026-03-01)**
- ✅ 实现BGE中文Embedding
- ✅ 集成LanceDB向量存储
- ✅ 实现飞书Bitable知识图谱
- ✅ 提供完整CLI工具

## 🤝 相关资源

- BGE模型: https://github.com/FlagOpen/FlagEmbedding
- LanceDB: https://lancedb.github.io/
- 飞书Bitable API: https://open.feishu.cn/document/uAjLw4CM/

---
*Made with ❤️ for Chinese users*
