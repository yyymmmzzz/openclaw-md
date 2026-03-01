#!/usr/bin/env python3
"""
文件管理工具
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime

class FileManager:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
    
    def ls(self, path=".", recursive=False):
        """列出目录内容"""
        p = Path(path)
        if not p.exists():
            print(f"❌ 路径不存在: {path}")
            return
        
        items = list(p.rglob("*")) if recursive else list(p.iterdir())
        
        print(f"📁 {p.absolute()}")
        print("-" * 60)
        
        for item in sorted(items):
            prefix = "📁" if item.is_dir() else "📄"
            size = item.stat().st_size if item.is_file() else 0
            size_str = f"{size:,}B" if size < 1024 else f"{size/1024:.1f}KB" if size < 1024*1024 else f"{size/(1024*1024):.1f}MB"
            mtime = datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m-%d %H:%M")
            print(f"{prefix} {item.name:40} {size_str:>10} {mtime}")
    
    def find(self, path, name=None, ext=None, size=None):
        """搜索文件"""
        p = Path(path)
        matches = []
        
        for item in p.rglob("*"):
            if item.is_file():
                match = True
                if name and name not in item.name:
                    match = False
                if ext and not item.suffix.endswith(ext):
                    match = False
                if match:
                    matches.append(item)
        
        print(f"🔍 在 {path} 中找到 {len(matches)} 个匹配文件:\n")
        for m in matches:
            print(f"  {m}")
    
    def cp(self, src, dst):
        """复制文件/目录"""
        s, d = Path(src), Path(dst)
        
        if self.dry_run:
            print(f"[模拟] 复制: {s} → {d}")
            return
        
        try:
            if s.is_dir():
                shutil.copytree(s, d)
            else:
                shutil.copy2(s, d)
            print(f"✅ 复制成功: {s} → {d}")
        except Exception as e:
            print(f"❌ 复制失败: {e}")
    
    def mv(self, src, dst):
        """移动文件/目录"""
        s, d = Path(src), Path(dst)
        
        if self.dry_run:
            print(f"[模拟] 移动: {s} → {d}")
            return
        
        try:
            shutil.move(str(s), str(d))
            print(f"✅ 移动成功: {s} → {d}")
        except Exception as e:
            print(f"❌ 移动失败: {e}")
    
    def rm(self, path, force=False):
        """删除文件/目录（安全删除）"""
        p = Path(path)
        
        if not p.exists():
            print(f"❌ 路径不存在: {path}")
            return
        
        if not force:
            confirm = input(f"⚠️ 确认删除 {p}? [y/N]: ")
            if confirm.lower() != 'y':
                print("已取消")
                return
        
        if self.dry_run:
            print(f"[模拟] 删除: {p}")
            return
        
        try:
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            print(f"✅ 已删除: {p}")
        except Exception as e:
            print(f"❌ 删除失败: {e}")
    
    def info(self, path):
        """显示文件信息"""
        p = Path(path)
        
        if not p.exists():
            print(f"❌ 路径不存在: {path}")
            return
        
        stat = p.stat()
        print(f"📄 {p.absolute()}")
        print("-" * 60)
        print(f"类型: {'目录' if p.is_dir() else '文件'}")
        print(f"大小: {stat.st_size:,} bytes")
        print(f"创建时间: {datetime.fromtimestamp(stat.st_ctime)}")
        print(f"修改时间: {datetime.fromtimestamp(stat.st_mtime)}")
        print(f"访问时间: {datetime.fromtimestamp(stat.st_atime)}")
        print(f"权限: {oct(stat.st_mode)[-3:]}")
    
    def organize(self, path):
        """按类型整理文件"""
        p = Path(path)
        
        # 文件类型映射
        type_dirs = {
            '.jpg': '图片', '.jpeg': '图片', '.png': '图片', '.gif': '图片',
            '.mp4': '视频', '.mov': '视频', '.avi': '视频',
            '.mp3': '音频', '.wav': '音频', '.flac': '音频',
            '.pdf': '文档', '.doc': '文档', '.docx': '文档',
            '.txt': '文本', '.md': '文本',
            '.py': '代码', '.js': '代码', '.ts': '代码',
            '.zip': '压缩', '.rar': '压缩', '.7z': '压缩',
        }
        
        moved = 0
        for item in p.iterdir():
            if item.is_file():
                ext = item.suffix.lower()
                dir_name = type_dirs.get(ext, '其他')
                
                target_dir = p / dir_name
                if not target_dir.exists():
                    target_dir.mkdir()
                
                target = target_dir / item.name
                
                if self.dry_run:
                    print(f"[模拟] 移动: {item.name} → {dir_name}/")
                else:
                    shutil.move(str(item), str(target))
                    print(f"✅ {item.name} → {dir_name}/")
                moved += 1
        
        print(f"\n📊 整理了 {moved} 个文件")

def main():
    parser = argparse.ArgumentParser(description="文件管理工具")
    parser.add_argument("command", choices=["ls", "find", "cp", "mv", "rm", "info", "organize"],
                       help="命令")
    parser.add_argument("paths", nargs="*", help="路径参数")
    parser.add_argument("--name", help="文件名匹配")
    parser.add_argument("--ext", help="扩展名匹配")
    parser.add_argument("-r", "--recursive", action="store_true", help="递归")
    parser.add_argument("-f", "--force", action="store_true", help="强制")
    parser.add_argument("--dry-run", action="store_true", help="模拟运行")
    
    args = parser.parse_args()
    
    fm = FileManager(dry_run=args.dry_run)
    
    if args.command == "ls":
        fm.ls(args.paths[0] if args.paths else ".", args.recursive)
    elif args.command == "find":
        fm.find(args.paths[0] if args.paths else ".", args.name, args.ext)
    elif args.command == "cp":
        if len(args.paths) < 2:
            print("用法: cp <源> <目标>")
            return
        fm.cp(args.paths[0], args.paths[1])
    elif args.command == "mv":
        if len(args.paths) < 2:
            print("用法: mv <源> <目标>")
            return
        fm.mv(args.paths[0], args.paths[1])
    elif args.command == "rm":
        if not args.paths:
            print("用法: rm <路径>")
            return
        fm.rm(args.paths[0], args.force)
    elif args.command == "info":
        if not args.paths:
            print("用法: info <路径>")
            return
        fm.info(args.paths[0])
    elif args.command == "organize":
        fm.organize(args.paths[0] if args.paths else ".")

if __name__ == "__main__":
    main()
