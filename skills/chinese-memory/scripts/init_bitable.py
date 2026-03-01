#!/usr/bin/env python3
"""
初始化飞书Bitable知识图谱
创建必要的表结构
"""

import os
import sys
import json
import requests
from pathlib import Path

CONFIG_PATH = Path.home() / ".openclaw" / "config.json"

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH) as f:
            return json.load(f).get("chinese-memory", {})
    return {}


def init_bitable(app_id: str, app_secret: str, app_name: str = "龙虾记忆系统"):
    """初始化Bitable应用
    
    创建一个新的Bitable应用，包含知识图谱所需的表结构
    """
    
    # 1. 获取tenant_token
    token_url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(token_url, json={"app_id": app_id, "app_secret": app_secret})
    resp.raise_for_status()
    tenant_token = resp.json()["tenant_access_token"]
    
    headers = {
        "Authorization": f"Bearer {tenant_token}",
        "Content-Type": "application/json"
    }
    
    # 2. 创建Bitable应用
    print("正在创建Bitable应用...")
    create_app_url = "https://open.feishu.cn/open-apis/bitable/v1/apps"
    app_data = {
        "name": app_name,
        "description": "龙虾记忆系统 - 知识图谱存储",
        "folder_token": ""
    }
    resp = requests.post(create_app_url, headers=headers, json=app_data)
    resp.raise_for_status()
    app_info = resp.json().get("data", {})
    app_token = app_info.get("app_token")
    
    print(f"✅ 应用创建成功！App Token: {app_token}")
    
    # 3. 创建知识图谱表
    print("正在创建知识图谱表...")
    create_table_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables"
    
    table_data = {
        "table": {
            "name": "知识图谱",
            "description": "存储Subject-Predicate-Object三元组"
        },
        "fields": [
            {
                "field_name": "主语(Subject)",
                "type": 1,  # Text
                "property": {}
            },
            {
                "field_name": "谓语(Predicate)",
                "type": 1,  # Text
                "property": {}
            },
            {
                "field_name": "宾语(Object)",
                "type": 1,  # Text
                "property": {}
            },
            {
                "field_name": "置信度(Confidence)",
                "type": 2,  # Number
                "property": {"formatter": "0.00"}
            },
            {
                "field_name": "来源(Source)",
                "type": 1,  # Text
                "property": {}
            },
            {
                "field_name": "创建时间",
                "type": 5,  # DateTime
                "property": {"date_formatter": "yyyy-MM-dd HH:mm", "auto_fill": True}
            }
        ]
    }
    
    resp = requests.post(create_table_url, headers=headers, json=table_data)
    resp.raise_for_status()
    table_info = resp.json().get("data", {})
    table_id = table_info.get("table_id")
    
    print(f"✅ 表创建成功！Table ID: {table_id}")
    
    # 4. 更新配置文件
    print("\n请更新配置文件 ~/.openclaw/config.json：")
    print(json.dumps({
        "chinese-memory": {
            "bitable_app_token": app_token,
            "bitable_table_id": table_id,
            "feishu_app_id": app_id,
            "feishu_app_secret": app_secret
        }
    }, ensure_ascii=False, indent=2))
    
    return app_token, table_id


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="初始化飞书Bitable")
    parser.add_argument("--app-id", required=True, help="飞书App ID")
    parser.add_argument("--app-secret", required=True, help="飞书App Secret")
    parser.add_argument("--name", default="龙虾记忆系统", help="应用名称")
    
    args = parser.parse_args()
    
    try:
        app_token, table_id = init_bitable(args.app_id, args.app_secret, args.name)
        print("\n🎉 初始化完成！")
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
