#!/usr/bin/env python3
"""
安全审计工具
"""

import os
import sys
import re
import subprocess
from pathlib import Path

# 敏感模式
SENSITIVE_PATTERNS = {
    "api_key": r'(api[_-]?key|apikey)\s*[:=]\s*["\']?[a-zA-Z0-9]{16,}["\']?',
    "password": r'(password|passwd|pwd)\s*[:=]\s*["\'][^"\']{4,}["\']',
    "token": r'(token|access_token)\s*[:=]\s*["\']?[a-zA-Z0-9]{20,}["\']?',
    "secret": r'(secret|app_secret)\s*[:=]\s*["\']?[a-zA-Z0-9]{16,}["\']?',
    "private_key": r'-----BEGIN (RSA |DSA |EC |OPENSSH )?PRIVATE KEY-----',
}

# 注入检测模式
INJECTION_PATTERNS = [
    r'ignore\s+(previous|above|all)\s+instructions',
    r'forget\s+(everything|all|your)\s+(instructions|training)',
    r'system\s*:\s*you\s+are\s+now',
    r'developer\s*:\s*',
    r'<\s*system\s*>',
    r'act\s+as\s+(if\s+)?you\s+(are|were)',
]

def check_secrets(path="."):
    """检查密钥泄露"""
    print("🔍 检查密钥泄露...")
    
    found = []
    p = Path(path)
    
    for ext in [".py", ".js", ".ts", ".json", ".yaml", ".yml", ".env", ".sh"]:
        for file in p.rglob(f"*{ext}"):
            if ".git" in str(file):
                continue
            
            try:
                content = file.read_text(encoding='utf-8', errors='ignore')
                for pattern_name, pattern in SENSITIVE_PATTERNS.items():
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        # 忽略示例/文档
                        line_num = content[:match.start()].count('\n') + 1
                        line = content.split('\n')[line_num - 1]
                        if 'example' not in line.lower() and 'placeholder' not in line.lower():
                            found.append({
                                "file": file,
                                "line": line_num,
                                "type": pattern_name,
                                "match": match.group()[:50] + "..."
                            })
            except:
                pass
    
    if found:
        print(f"⚠️  发现 {len(found)} 个潜在密钥泄露:\n")
        for f in found[:10]:  # 最多显示10个
            print(f"   {f['file']}:{f['line']} - {f['type']}")
            print(f"      {f['match']}")
        if len(found) > 10:
            print(f"   ... 还有 {len(found) - 10} 个")
    else:
        print("✅ 未发现明显密钥泄露")
    
    return len(found)

def check_permissions(path="."):
    """检查文件权限"""
    print("\n🔍 检查文件权限...")
    
    issues = []
    p = Path(path)
    
    for file in p.rglob("*"):
        if file.is_file():
            stat = file.stat()
            mode = oct(stat.st_mode)[-3:]
            
            # 检查过于开放的权限
            if mode in ["777", "666", "644"] and file.suffix in [".key", ".pem", ".env"]:
                issues.append({"file": file, "mode": mode, "issue": "敏感文件权限过宽"})
    
    if issues:
        print(f"⚠️  发现 {len(issues)} 个权限问题:\n")
        for i in issues[:5]:
            print(f"   {i['file']} - 权限{i['mode']} - {i['issue']}")
    else:
        print("✅ 文件权限检查通过")
    
    return len(issues)

def check_injection(text: str):
    """检查提示词注入"""
    print("\n🔍 检查提示词注入风险...")
    
    risks = []
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            risks.append(pattern)
    
    if risks:
        print(f"⚠️  发现 {len(risks)} 个潜在注入模式")
        return True
    else:
        print("✅ 未发现明显注入风险")
        return False

def check_config():
    """检查配置文件"""
    print("\n🔍 检查配置文件...")
    
    config_path = Path.home() / ".openclaw" / "config.json"
    
    if not config_path.exists():
        print("⚠️  配置文件不存在")
        return 1
    
    try:
        import json
        with open(config_path) as f:
            config = json.load(f)
        
        # 检查敏感配置
        issues = 0
        config_str = json.dumps(config)
        for pattern_name, pattern in SENSITIVE_PATTERNS.items():
            if re.search(pattern, config_str, re.IGNORECASE):
                print(f"⚠️  配置文件可能包含硬编码{p pattern_name}")
                issues += 1
        
        if issues == 0:
            print("✅ 配置文件检查通过")
        
        return issues
    except Exception as e:
        print(f"❌ 配置文件解析错误: {e}")
        return 1

def full_audit():
    """全面安全审计"""
    print("=" * 60)
    print("🔒 ClawSec 安全审计")
    print("=" * 60)
    print()
    
    total_issues = 0
    
    total_issues += check_secrets()
    total_issues += check_permissions()
    total_issues += check_config()
    
    print("\n" + "=" * 60)
    if total_issues == 0:
        print("✅ 审计完成，未发现安全问题")
    else:
        print(f"⚠️  审计完成，发现 {total_issues} 个潜在问题")
    print("=" * 60)
    
    return total_issues

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="安全审计工具")
    parser.add_argument("--full", action="store_true", help="全面审计")
    parser.add_argument("--check-secrets", action="store_true", help="检查密钥泄露")
    parser.add_argument("--check-perms", action="store_true", help="检查权限")
    parser.add_argument("--check-config", action="store_true", help="检查配置")
    parser.add_argument("text", nargs="?", help="检查文本注入")
    
    args = parser.parse_args()
    
    if args.full:
        full_audit()
    elif args.check_secrets:
        check_secrets()
    elif args.check_perms:
        check_permissions()
    elif args.check_config:
        check_config()
    elif args.text:
        check_injection(args.text)
    else:
        full_audit()
