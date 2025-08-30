SMB挂载管理Web应用
这是一个跨平台的SMB挂载管理Web应用，使用Python Flask作为后端，TailwindCSS和DaisyUI作为前端框架，JSON文件存储配置。

跨平台兼容性处理(macOS/Linux/Windows)
系统命令封装用于挂载操作

项目结构

smb-web-manager/
├── app.py                 # Flask主应用
├── config.json           # 配置文件
├── smb_manager.py        # SMB管理核心逻辑
├── static/
│   ├── css/
│   │   └── style.css     # 自定义样式
│   └── js/
│       └── script.js     # 前端交互逻辑
├── templates/
│   ├── base.html         # 基础模板
│   ├── index.html        # 主界面
│   ├── config.html       # 配置管理
│   └── logs.html         # 日志查看
└── requirements.txt      # Python依赖

使用说明
安装依赖:
pip install -r requirements.txt

运行应用:
python app.py

访问应用:
打开浏览器访问 http://localhost:5555

功能特点
跨平台支持: 兼容 macOS、Linux 和 Windows 系统
响应式设计: 使用 TailwindCSS 和 DaisyUI，适配桌面和移动设备
挂载管理: 添加、删除、挂载和卸载 SMB 共享
状态监控: 实时查看挂载状态和系统信息
配置管理: 通过 Web 界面管理 SMB 挂载配置
日志查看: 查看操作日志和系统日志
