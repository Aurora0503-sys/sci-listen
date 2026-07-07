#!/bin/bash

# 🎓 学术会议陪听助手 - 桌面版安装脚本

echo "🚀 开始安装学术会议陪听助手桌面版..."

# 检查Node.js环境
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到Node.js，请先安装Node.js 16+"
    echo "📥 下载地址: https://nodejs.org/"
    exit 1
fi

# 检查npm
if ! command -v npm &> /dev/null; then
    echo "❌ 错误: 未找到npm，请确保Node.js安装正确"
    exit 1
fi

# 进入桌面版目录
cd desktop

# 安装依赖
echo "📦 安装依赖包..."
npm install

if [ $? -ne 0 ]; then
    echo "❌ 依赖安装失败"
    exit 1
fi

# 安装Electron构建工具
echo "🔧 安装构建工具..."
npm install --save-dev electron-builder

# 创建启动脚本
echo "📝 创建启动脚本..."
cat > start.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
npm start
EOF

chmod +x start.sh

echo ""
echo "✅ 安装完成！"
echo ""
echo "🎯 使用方法："
echo "   ./start.sh        # 启动桌面应用"
echo "   npm run dev       # 开发模式启动"
echo "   npm run build     # 打包应用"
echo ""
echo "🎨 功能特性："
echo "   ✅ 原生系统音频捕获"
echo "   ✅ 无需浏览器权限"
echo "   ✅ 跨平台支持 (Windows/macOS/Linux)"
echo ""
echo "🚀 让AI助力学术交流，让每个问题都更有深度！"