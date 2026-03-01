---
name: tavily-web-search
description: AI优化联网搜索，使用Tavily API进行高质量网页搜索和内容提取。比传统搜索更智能，能返回结构化结果和相关引用。
---

# Tavily Web Search - AI优化联网搜索

使用Tavily API进行智能网页搜索，提供比传统搜索更高质量的结果。

## 安装依赖

```bash
pip install tavily-python
```

## 配置

编辑 `~/.openclaw/config.json`：

```json
{
  "tavily-web-search": {
    "api_key": "tvly-your-api-key"
  }
}
```

获取API Key: https://tavily.com

## 使用方法

```bash
# 基本搜索
python3 search.py "OpenClaw最新功能"

# 深度搜索（包含内容提取）
python3 search.py "AI agent发展趋势" --depth advanced

# 搜索并回答特定问题
python3 search.py "什么是向量数据库" --question "用最简单的语言解释"
```

## 与coze-web-search的区别

| 特性 | coze-web-search | tavily-web-search |
|-----|-----------------|-------------------|
| 搜索源 | 通用搜索引擎 | Tavily AI优化索引 |
| 结果质量 | 基础 | 更高质量，结构化 |
| 引用支持 | 有限 | 完整引用溯源 |
| 内容提取 | 需额外处理 | 内置智能提取 |

## 定价

Tavily提供免费额度：
- 免费版: 1000次/月
- 付费版: $0.025/次
