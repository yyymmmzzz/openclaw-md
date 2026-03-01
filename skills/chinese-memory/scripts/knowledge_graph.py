#!/usr/bin/env python3
"""
知识图谱模块 - 使用飞书Bitable存储三元组
Subject-Predicate-Object 结构
"""

import os
import sys
import json
import requests
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# 配置
CONFIG_PATH = Path.home() / ".openclaw" / "config.json"

def load_config():
    """加载配置"""
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            config = json.load(f)
            return config.get("chinese-memory", {})
    return {}


class FeishuKnowledgeGraph:
    """飞书Bitable知识图谱"""
    
    def __init__(self):
        self.config = load_config()
        self.app_token = self.config.get("bitable_app_token")
        self.table_id = self.config.get("bitable_table_id", "tbltRiJtLVv0HJ8c")  # 默认表ID
        
        # 从环境或配置文件获取飞书token
        self.tenant_token = os.environ.get("FEISHU_TENANT_TOKEN") or self.config.get("feishu_tenant_token")
        self.app_id = os.environ.get("FEISHU_APP_ID") or self.config.get("feishu_app_id")
        self.app_secret = os.environ.get("FEISHU_APP_SECRET") or self.config.get("feishu_app_secret")
        
        if not self.tenant_token and (self.app_id and self.app_secret):
            self.tenant_token = self._get_tenant_token()
    
    def _get_tenant_token(self) -> str:
        """通过AppID和AppSecret获取TenantToken"""
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        headers = {"Content-Type": "application/json"}
        data = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }
        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()["tenant_access_token"]
    
    def _get_headers(self) -> dict:
        """获取请求头"""
        return {
            "Authorization": f"Bearer {self.tenant_token}",
            "Content-Type": "application/json"
        }
    
    def store_triple(self, subject: str, predicate: str, obj: str, 
                     confidence: float = 1.0, source: str = "") -> dict:
        """存储三元组
        
        Args:
            subject: 主语（实体）
            predicate: 谓语（关系）
            obj: 宾语（值）
            confidence: 置信度 0-1
            source: 来源
        
        Returns:
            存储结果
        """
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records"
        
        record = {
            "fields": {
                "主语(Subject)": subject,
                "谓语(Predicate)": predicate,
                "宾语(Object)": obj,
                "置信度(Confidence)": confidence,
                "来源(Source)": source,
                "创建时间": int(datetime.now().timestamp() * 1000),
            }
        }
        
        resp = requests.post(url, headers=self._get_headers(), json=record)
        resp.raise_for_status()
        return resp.json()
    
    def query(self, subject: str = None, predicate: str = None, 
              obj: str = None, limit: int = 100) -> List[Dict]:
        """查询知识图谱
        
        Args:
            subject: 主语筛选
            predicate: 谓语筛选
            obj: 宾语筛选
            limit: 返回数量
        
        Returns:
            匹配的三元组列表
        """
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token}/tables/{self.table_id}/records/search"
        
        # 构建过滤条件
        filters = []
        if subject:
            filters.append({"field_name": "主语(Subject)", "operator": "is", "value": [subject]})
        if predicate:
            filters.append({"field_name": "谓语(Predicate)", "operator": "is", "value": [predicate]})
        if obj:
            filters.append({"field_name": "宾语(Object)", "operator": "is", "value": [obj]})
        
        data = {
            "filter": {"conjunction": "and", "conditions": filters} if filters else None,
            "page_size": limit
        }
        
        resp = requests.post(url, headers=self._get_headers(), json=data)
        resp.raise_for_status()
        result = resp.json()
        
        # 格式化返回结果
        items = result.get("data", {}).get("items", [])
        return [
            {
                "record_id": item["record_id"],
                "subject": item["fields"].get("主语(Subject)", ""),
                "predicate": item["fields"].get("谓语(Predicate)", ""),
                "object": item["fields"].get("宾语(Object)", ""),
                "confidence": item["fields"].get("置信度(Confidence)", 1.0),
                "source": item["fields"].get("来源(Source)", ""),
                "created_at": item["fields"].get("创建时间", 0),
            }
            for item in items
        ]
    
    def simple_reasoning(self, subject: str, predicate: str = None) -> List[Dict]:
        """简单推理查询
        
        例如：已知"老板喜欢吃川菜"，查询"老板喜欢吃什么"
        
        Args:
            subject: 主语
            predicate: 谓语（可选）
        
        Returns:
            推理结果
        """
        # 直接查询
        results = self.query(subject=subject, predicate=predicate)
        
        # 简单推理扩展
        if predicate is None:
            # 查询所有相关关系
            return results
        
        return results
    
    def find_related(self, subject: str, depth: int = 1) -> List[Dict]:
        """查找相关实体（图遍历）
        
        Args:
            subject: 起始实体
            depth: 遍历深度（目前只支持1层）
        
        Returns:
            相关实体列表
        """
        # 查询以subject为主语的三元组
        as_subject = self.query(subject=subject)
        
        # 查询以subject为宾语的三元组
        as_object = self.query(obj=subject)
        
        return {
            "as_subject": as_subject,  # subject -> ?
            "as_object": as_object     # ? -> subject
        }


def main():
    """命令行入口"""
    import argparse
    
    parser = argparse.ArgumentParser(description="知识图谱操作")
    subparsers = parser.add_subparsers(dest="command", help="子命令")
    
    # store命令
    store_parser = subparsers.add_parser("store", help="存储三元组")
    store_parser.add_argument("subject", help="主语")
    store_parser.add_argument("predicate", help="谓语")
    store_parser.add_argument("object", help="宾语")
    store_parser.add_argument("--confidence", type=float, default=1.0, help="置信度")
    store_parser.add_argument("--source", default="", help="来源")
    
    # query命令
    query_parser = subparsers.add_parser("query", help="查询三元组")
    query_parser.add_argument("--subject", help="主语")
    query_parser.add_argument("--predicate", help="谓语")
    query_parser.add_argument("--object", help="宾语")
    
    # reason命令
    reason_parser = subparsers.add_parser("reason", help="简单推理")
    reason_parser.add_argument("subject", help="主语")
    reason_parser.add_argument("--predicate", help="谓语")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    kg = FeishuKnowledgeGraph()
    
    if args.command == "store":
        result = kg.store_triple(args.subject, args.predicate, args.object, 
                                args.confidence, args.source)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    elif args.command == "query":
        results = kg.query(args.subject, args.predicate, args.object)
        print(f"找到 {len(results)} 条记录：")
        for r in results:
            print(f"  {r['subject']} --[{r['predicate']}]--> {r['object']}")
    
    elif args.command == "reason":
        results = kg.simple_reasoning(args.subject, args.predicate)
        print(f"推理结果 ({len(results)} 条)：")
        for r in results:
            print(f"  {r['subject']} --[{r['predicate']}]--> {r['object']}")


if __name__ == "__main__":
    main()
