#!/bin/bash

# 修仙游戏助手 - Docker 快速部署脚本
# 用法：bash deploy.sh

set -e

echo "🚀 修仙游戏助手 - Docker 部署脚本"
echo "=================================="
echo ""

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装！请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装！请先安装 Docker Compose"
    exit 1
fi

echo "✅ Docker 环境检查通过"
echo ""

# 检查配置文件
if [ ! -f "config/config.yaml" ]; then
    echo "⚠️  配置文件不存在，正在创建..."
    cp config/config.example.yaml config/config.yaml
    echo "📝 请编辑 config/config.yaml 填入："
    echo "   - bot_token: 你的 Bot Token"
    echo "   - user_id: 你的 User ID"
    echo "   - game_bot_username: 游戏机器人用户名"
    echo ""
    read -p "按 Enter 继续（确保已编辑 config/config.yaml）..."
fi

# 检查 Bot Token 是否已配置
if grep -q "YOUR_BOT_TOKEN_HERE" config/config.yaml; then
    echo "❌ Bot Token 未配置！请编辑 config/config.yaml"
    exit 1
fi

echo "✅ 配置文件检查通过"
echo ""

# 停止旧容器
echo "🛑 停止旧容器..."
docker-compose down 2>/dev/null || true

# 清理（可选）
read -p "是否清理旧的 Docker 镜像？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🧹 清理旧镜像..."
    docker system prune -a --volumes --force
fi

# 构建
echo ""
echo "🔨 构建 Docker 镜像..."
docker-compose build --no-cache

# 启动
echo ""
echo "🚀 启动服务..."
docker-compose up -d

# 等待初始化
echo ""
echo "⏳ 等待服务初始化 (10秒)..."
sleep 10

# 检查状态
echo ""
echo "📊 检查服务状态..."
docker-compose ps

# 显示日志
echo ""
echo "📋 最近的日志："
docker-compose logs --tail=20 bot

echo ""
echo "✅ 部署完成！"
echo ""
echo "🎮 接下来："
echo "1. 在 Telegram 中找到你的 Bot"
echo "2. 发送 /start 命令"
echo "3. 应该看到菜单界面"
echo ""
echo "📖 更多信息查看："
echo "   - cat QUICKSTART.md"
echo "   - cat README.md"
echo ""
echo "📝 查看实时日志："
echo "   docker-compose logs -f bot"
echo ""
