---
name: clawsec
description: 安全套件，防注入/审计。社区强推"安全第一"。
---

# ClawSec - 安全套件

安全检查工具，帮助识别潜在风险和安全问题。

## 使用方法

```bash
# 全面安全审计
python3 audit.py --full

# 检查特定项目
python3 audit.py --check-config    # 配置文件检查
python3 audit.py --check-secrets   # 密钥泄露检查
python3 audit.py --check-perms     # 权限检查
python3 audit.py --check-network   # 网络暴露检查

# 检查文本是否含注入风险
python3 audit.py text "要检查的文本"
```

## 检查项

- ✅ API密钥硬编码检测
- ✅ 敏感文件权限检查
- ✅ 配置文件安全审计
- ✅ 提示词注入检测
- ✅ 网络端口暴露检查
