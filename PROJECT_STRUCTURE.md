# 📁 项目结构说明

```
sci-listen/
├── README.md                    # 主项目说明文档
├── sci-listen.md                # 项目详细设计文档
├── requirements.txt             # Python依赖列表
├── .gitignore                   # Git忽略文件配置
│
├── 📂 sci_listen_app/           # Flutter移动端应用
│   ├── lib/                     # Dart源代码
│   ├── android/                 # Android平台配置
│   ├── ios/                     # iOS平台配置
│   ├── web/                     # Flutter Web平台配置
│   ├── pubspec.yaml            # Flutter依赖配置
│   └── README.md               # Flutter应用说明
│
├── 📂 web/                      # Web前端应用
│   └── simple_sci_listen.html   # 主要的Web应用界面
│
├── 📂 api/                      # 后端API服务
│   ├── api_server.py           # 基础API服务器（需外部API key）
│   └── working_api.py          # 简化API服务器（本地备用方案）
│
├── 📂 tests/                    # 测试文件
│   ├── test_api.py             # API功能测试
│   └── simple_test.py          # 简单测试脚本
│
└── 📂 docs/                     # 文档目录
    └── api_call_explanation.md  # API调用详细说明
```

## 🎯 各目录功能说明

### sci_listen_app/ - Flutter移动端
- 跨平台移动应用，支持Android、iOS、Desktop
- 基于Flutter框架，提供原生的移动端体验
- 支持离线语音识别和本地数据存储

### web/ - Web应用
- 基于HTML/CSS/JavaScript的单页应用
- 使用Web Speech API进行实时语音识别
- 通过API调用后端AI服务生成学术问题

### api/ - 后端服务
- 基于Flask的RESTful API服务器
- 提供语音转文本后的AI问题生成服务
- 支持DashScope API和本地备用方案

### tests/ - 测试脚本
- API功能验证和性能测试
- 前后端集成测试

### docs/ - 项目文档
- API调用流程说明
- 技术实现细节文档

## 🚀 快速启动

1. **Web端使用**：
   ```bash
   cd api && python working_api.py &
   cd ../web && python -m http.server 8082 &
   # 访问 http://localhost:8082/simple_sci_listen.html
   ```

2. **Flutter端开发**：
   ```bash
   cd sci_listen_app
   flutter pub get
   flutter run
   ```

## 📦 部署说明

- **Web端**：可部署到任何静态文件服务器
- **API服务**：需要Python 3.6+环境，建议使用Docker容器化部署
- **Flutter应用**：可打包为APK、IPA或桌面应用