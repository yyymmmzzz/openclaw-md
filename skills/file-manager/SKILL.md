---
name: file-manager
description: 文件管理，支持读写/搜索/分类。日常高频使用，零差评。
---

# File Manager - 文件管理

日常文件管理工具，支持常用文件操作。

## 使用方法

```bash
# 列出目录
python3 manage.py ls /path/to/dir

# 搜索文件
python3 manage.py find /path/to/search --name "*.py"

# 复制文件
python3 manage.py cp source.txt dest.txt

# 移动文件
python3 manage.py mv old.txt new.txt

# 删除文件（安全删除到回收站）
python3 manage.py rm file.txt

# 文件信息
python3 manage.py info file.txt

# 批量重命名
python3 manage.py rename "*.txt" --prefix "backup_"

# 按类型分类文件
python3 manage.py organize /path/to/dir
```

## 特点

- ✅ 安全操作（删除前确认）
- ✅ 支持批量操作
- ✅ 智能分类整理
- ✅ 跨平台支持
