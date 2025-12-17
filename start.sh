#!/bin/bash

# Mimo2API Python版本 - 快速启动脚本

echo "╔══════════════════════════════════════════════════════════╗"
echo "║                    Mimo2API Python                       ║"
echo "║          将小米 Mimo AI 转换为 OpenAI 兼容 API           ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python 3"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python 版本: $PYTHON_VERSION"

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
    echo "✓ 虚拟环境创建成功"
fi

# 激活虚拟环境
echo ""
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo ""
echo "📥 安装依赖..."
pip install -r requirements.txt -q

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

echo "✓ 依赖安装成功"

# 启动服务
echo ""
echo "🚀 启动服务..."
echo ""
python3 main.py
