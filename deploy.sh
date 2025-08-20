#!/bin/bash

# TokenData Cloudflare部署脚本

echo "🚀 开始部署TokenData到Cloudflare Pages..."

# 检查是否安装了wrangler
if ! command -v wrangler &> /dev/null; then
    echo "❌ 未找到wrangler，正在安装..."
    npm install -g wrangler
fi

# 检查是否已登录
if ! wrangler whoami &> /dev/null; then
    echo "🔐 请先登录Cloudflare..."
    wrangler login
fi

# 检查必要文件
echo "📁 检查项目文件..."
if [ ! -f "app.py" ]; then
    echo "❌ 未找到app.py文件"
    exit 1
fi

if [ ! -f "requirements-cloudflare.txt" ]; then
    echo "❌ 未找到requirements-cloudflare.txt文件"
    exit 1
fi

if [ ! -f "wrangler.toml" ]; then
    echo "❌ 未找到wrangler.toml文件"
    exit 1
fi

echo "✅ 所有必要文件已找到"

# 部署到Cloudflare Pages
echo "🌐 开始部署..."
wrangler pages deploy . --project-name=tokendata

if [ $? -eq 0 ]; then
    echo "✅ 部署成功！"
    echo "🌍 你的应用现在可以通过以下URL访问："
    echo "   https://tokendata.pages.dev"
else
    echo "❌ 部署失败，请检查错误信息"
    exit 1
fi
