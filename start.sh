#!/bin/bash

# 🎯 学术会议陪听助手 - 快速启动脚本

echo "🚀 启动学术会议陪听助手..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到Python3，请先安装Python 3.6+"
    exit 1
fi

# 检查依赖
echo "📦 检查依赖..."
pip3 install flask flask-cors requests > /dev/null 2>&1

# 启动API服务器
echo "🔧 启动API服务器 (端口: 5002)..."
cd api
python3 working_api.py &
API_PID=$!
cd ..

# 等待API服务器启动
sleep 2

# 启动Web服务器
echo "🌐 启动Web服务器 (端口: 8082)..."
cd web
python3 -m http.server 8082 &
WEB_PID=$!
cd ..

echo ""
echo "✅ 服务启动成功！"
echo ""
echo "📱 Web应用地址: http://localhost:8082/simple_sci_listen.html"
echo "🔧 API服务地址: http://localhost:5002"
echo ""
echo "🛑 停止服务请按 Ctrl+C"
echo ""

# 等待中断信号
trap "echo ''; echo '🛑 正在停止服务...'; kill $API_PID $WEB_PID; exit 0" INT

# 保持脚本运行
wait