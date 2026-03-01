#!/usr/bin/env python3
"""
向量记忆存储模块
使用BGE中文Embedding模型 + LanceDB
"""

import os
import sys
import json
import numpy as np
from pathlib import Path
from datetime import datetime

# 添加依赖路径
try:
    from sentence_transformers import SentenceTransformer
    import lancedb
except ImportError:
    print("请先安装依赖: pip install sentence-transformers lancedb")
    sys.exit(1)

# 配置
CONFIG_PATH = Path.home() / ".openclaw" / "config.json"
DEFAULT_DB_PATH = Path.home() / ".openclaw" / "memory" / "vectors"
DEFAULT_MODEL = "BAAI/bge-large-zh-v1.5"

def load_config():
    """加载配置"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            config = json.load(f)
            return config.get("chinese-memory", {})
    return {}

class ChineseMemory:
    def __init__(self):
        self.config = load_config()
        self.db_path = Path(self.config.get("vector_db_path", DEFAULT_DB_PATH)).expanduser()
        self.model_name = self.config.get("embedding_model", DEFAULT_MODEL)
        self.use_local = self.config.get("use_local_model", True)
        
        # 确保目录存在
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # 延迟加载模型（首次使用时加载）
        self._model = None
        self._db = None
        self._table = None
    
    @property
    def model(self):
        """懒加载Embedding模型"""
        if self._model is None:
            print(f"正在加载BGE模型: {self.model_name}...")
            print("首次加载需要下载模型（约1.5GB），请耐心等待...")
            self._model = SentenceTransformer(self.model_name)
            print("模型加载完成！")
        return self._model
    
    @property
    def db(self):
        """懒加载LanceDB"""
        if self._db is None:
            self._db = lancedb.connect(str(self.db_path))
        return self._db
    
    @property
    def table(self):
        """懒加载数据表"""
        if self._table is None:
            table_name = "memories"
            if table_name in self.db.table_names():
                self._table = self.db.open_table(table_name)
            else:
                # 创建新表
                import pyarrow as pa
                schema = pa.schema([
                    ("id", pa.string()),
                    ("text", pa.string()),
                    ("vector", pa.list_(pa.float32(), 1024 if "large" in self.model_name else 768)),
                    ("category", pa.string()),
                    ("importance", pa.float32()),
                    ("created_at", pa.int64()),
                    ("access_count", pa.int32()),
                ])
                self._table = self.db.create_table(table_name, schema=schema)
        return self._table
    
    def embed(self, text: str) -> np.ndarray:
        """生成文本的Embedding向量"""
        # BGE模型建议添加前缀
        prefixed_text = f"为这个句子生成表示：{text}"
        embedding = self.model.encode(prefixed_text, normalize_embeddings=True)
        return embedding
    
    def store(self, text: str, category: str = "other", importance: float = 0.7) -> dict:
        """存储记忆
        
        Args:
            text: 要存储的文本
            category: 记忆类别 (preference/fact/decision/entity/other)
            importance: 重要程度 0-1
        
        Returns:
            存储的记忆记录
        """
        import uuid
        
        # 生成向量
        vector = self.embed(text)
        
        # 检查重复
        if self._check_duplicate(vector, text):
            return {"status": "duplicate", "message": "相似记忆已存在"}
        
        # 创建记录
        record = {
            "id": str(uuid.uuid4()),
            "text": text,
            "vector": vector.tolist(),
            "category": category,
            "importance": importance,
            "created_at": int(datetime.now().timestamp() * 1000),
            "access_count": 0,
        }
        
        # 存储到LanceDB
        self.table.add([record])
        
        return {"status": "success", "id": record["id"], "text": text}
    
    def _check_duplicate(self, vector: np.ndarray, text: str, threshold: float = 0.95) -> bool:
        """检查是否存在相似记忆"""
        try:
            results = self.search(vector, limit=1)
            if results and results[0]["score"] > threshold:
                return True
        except Exception:
            pass
        return False
    
    def search(self, query, limit: int = 5, min_score: float = 0.5) -> list:
        """搜索相关记忆
        
        Args:
            query: 查询文本或向量
            limit: 返回结果数量
            min_score: 最小相似度阈值
        
        Returns:
            相关记忆列表
        """
        # 如果是文本，先转换为向量
        if isinstance(query, str):
            query_vector = self.embed(query)
        else:
            query_vector = query
        
        # 执行向量搜索
        results = self.table.search(query_vector).limit(limit).to_list()
        
        # 过滤和格式化结果
        memories = []
        for r in results:
            score = r.get("_distance", 0)
            # LanceDB使用L2距离，转换为相似度分数 (0-1)
            similarity = 1 / (1 + score)
            
            if similarity >= min_score:
                memories.append({
                    "id": r["id"],
                    "text": r["text"],
                    "category": r["category"],
                    "importance": r["importance"],
                    "score": similarity,
                    "created_at": r["created_at"],
                })
        
        return memories


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="存储向量记忆")
    parser.add_argument("text", help="要存储的文本")
    parser.add_argument("--category", default="other", 
                       choices=["preference", "fact", "decision", "entity", "other"],
                       help="记忆类别")
    parser.add_argument("--importance", type=float, default=0.7, help="重要程度0-1")
    
    args = parser.parse_args()
    
    memory = ChineseMemory()
    result = memory.store(args.text, args.category, args.importance)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
