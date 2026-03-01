#!/bin/bash
# 国产化记忆系统安装脚本

set -e

echo "🦞 龙虾国产化记忆系统安装"
echo "============================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo ""
echo "📋 安装步骤："

# 1. 检查Python版本
echo ""
echo "[1/5] 检查Python版本..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python版本: $python_version"

# 2. 安装Python依赖
echo ""
echo "[2/5] 安装Python依赖..."
echo "   安装: sentence-transformers lancedb pyarrow requests"
pip install -q sentence-transformers lancedb pyarrow requests numpy || {
    echo -e "${RED}❌ 依赖安装失败${NC}"
    echo "   请手动运行: pip install sentence-transformers lancedb pyarrow requests numpy"
    exit 1
}
echo -e "${GREEN}✅ 依赖安装完成${NC}"

# 3. 创建配置目录
echo ""
echo "[3/5] 创建配置目录..."
mkdir -p ~/.openclaw/memory/vectors
echo -e "${GREEN}✅ 目录创建完成${NC}"

# 4. 检查配置文件
echo ""
echo "[4/5] 检查配置文件..."
config_file="$HOME/.openclaw/config.json"
if [ -f "$config_file" ]; then
    echo -e "${YELLOW}⚠️ 配置文件已存在: $config_file${NC}"
    echo "   请手动添加 chinese-memory 配置"
else
    echo "   创建默认配置..."
    cat > "$config_file" << 'EOF'
{
  "chinese-memory": {
    "embedding_model": "BAAI/bge-large-zh-v1.5",
    "vector_db_path": "~/.openclaw/memory/vectors",
    "use_local_model": true,
    "bitable_app_token": "",
    "bitable_table_id": "",
    "feishu_app_id": "",
    "feishu_app_secret": ""
  }
}
EOF
    echo -e "${GREEN}✅ 配置文件创建: $config_file${NC}"
fi

# 5. 测试导入
echo ""
echo "[5/5] 测试模块导入..."
cd "$(dirname "$0")"
python3 -c "from memory_store import ChineseMemory; print('✅ memory_store 导入成功')" 2>/dev/null || echo -e "${YELLOW}⚠️ 首次使用时会自动下载BGE模型（约1.5GB）${NC}"

echo ""
echo "============================"
echo -e "${GREEN}🎉 安装完成！${NC}"
echo ""
echo "📖 快速开始:"
echo ""
echo "1. 配置飞书Bitable（可选）:"
echo "   python3 init_bitable.py --app-id YOUR_APP_ID --app-secret YOUR_APP_SECRET"
echo ""
echo "2. 存储向量记忆:"
echo "   python3 memory_store.py '老板喜欢吃川菜' --category preference"
echo ""
echo "3. 搜索记忆:"
echo "   python3 memory_search.py '老板的饮食偏好'"
echo ""
echo "4. 存储知识图谱:"
echo "   python3 knowledge_graph.py store 老板 喜欢吃 川菜"
echo ""
echo "5. 查询知识图谱:"
echo "   python3 knowledge_graph.py query --subject 老板"
echo ""
