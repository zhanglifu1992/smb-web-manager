# SMB挂载管理Web应用

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-2.2.19-38B2AC)
![DaisyUI](https://img.shields.io/badge/DaisyUI-2.6.0-FF7AC1)
![License](https://img.shields.io/badge/License-MIT-yellow)

一个现代化的跨平台SMB挂载管理Web应用，使用Python Flask作为后端，TailwindCSS和DaisyUI作为前端框架，JSON文件存储配置。

## ✨ 特性

- 🌐 **跨平台支持**: 全面兼容 macOS、Linux 和 Windows 系统
- 📱 **响应式设计**: 基于TailwindCSS和DaisyUI，完美适配桌面和移动设备
- 🔧 **挂载管理**: 完整的SMB共享添加、删除、挂载和卸载功能
- 📊 **状态监控**: 实时查看挂载状态和系统信息
- ⚙️ **配置管理**: 直观的Web界面管理SMB挂载配置
- 📝 **日志系统**: 完整的操作日志和系统日志查看功能
- 🛡️ **安全可靠**: 自动处理配置文件损坏，提供备份机制

## 🗂️ 项目结构

```
smb-web-manager/
├── app.py                 # Flask主应用
├── config.json           # 配置文件 (自动生成)
├── smb_web_manager.log   # 日志文件 (自动生成)
├── static/
│   ├── css/
│   │   └── style.css     # 自定义样式
│   └── js/
│       └── script.js     # 前端交互逻辑
├── templates/
│   ├── base.html         # 基础模板
│   ├── index.html        # 主界面
│   ├── config.html       # 配置管理页面
│   └── logs.html         # 日志查看页面
└── requirements.txt      # Python依赖
```

## 🚀 快速开始

### 前置要求

- Python 3.8+
- pip (Python包管理器)

### 安装步骤

1. 克隆或下载项目文件
2. 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行应用：
   ```bash
   python app.py
   ```

4. 打开浏览器访问：
   ```
   http://localhost:5555
   ```

## 🎯 核心功能

### 仪表盘
- 实时系统信息展示（操作系统、主机名、版本等）
- 挂载点统计（总数/已挂载数）
- 一键挂载/卸载所有共享
- 状态实时刷新

### 配置管理
- 直观的表单添加新SMB共享配置
- 配置项列表展示与管理
- 支持服务器地址、共享名称、挂载点路径等完整参数
- 安全的密码输入字段

### 日志系统
- 操作日志实时查看
- 日志自动滚动显示
- 一键清空日志功能
- 错误信息高亮显示

## 🔧 技术架构

### 后端
- **Flask**: 轻量级Python Web框架，提供RESTful API
- **跨平台命令封装**: 自动适配macOS/Linux/Windows系统命令
- **JSON配置存储**: 简单可靠的数据持久化方案
- **异常处理**: 完善的错误处理和日志记录

### 前端
- **TailwindCSS**: 实用优先的CSS框架
- **DaisyUI**: 基于Tailwind的UI组件库
- **响应式设计**: 移动端优先的适配方案
- **现代JavaScript**: 使用Fetch API实现前后端交互

## 🌍 跨平台支持

| 操作系统 | 挂载命令 | 卸载命令 |
|----------|----------|----------|
| macOS | `mount -t smbfs` | `umount` |
| Linux | `mount -t cifs` | `umount` |
| Windows | `net use` | `net use /delete` |

## ⚠️ 注意事项

1. **权限要求**:
   - Windows系统可能需要管理员权限运行
   - macOS/Linux系统可能需要sudo权限执行挂载操作

2. **安全性**:
   - 密码以明文形式存储于配置文件中，请确保文件安全
   - 建议在生产环境中使用加密存储方案

3. **系统依赖**:
   - 确保系统已安装相应的SMB/CIFS客户端工具
   - macOS: 默认支持SMB
   - Linux: 需要安装cifs-utils包
   - Windows: 默认支持SMB

## 📝 更新日志

### v1.0.0
- 初始版本发布
- 基础SMB挂载管理功能
- 跨平台支持
- 响应式Web界面

## 🤝 贡献指南

欢迎提交Issue和Pull Request来帮助改进这个项目。

## 📄 许可证

本项目采用MIT许可证 - 查看[LICENSE](LICENSE)文件了解详情。

## 🙏 致谢

- [Flask](https://flask.palletsprojects.com/) - Python微框架
- [TailwindCSS](https://tailwindcss.com/) - 实用优先的CSS框架
- [DaisyUI](https://daisyui.com/) - Tailwind CSS组件库

---

如有问题或建议，请通过GitHub Issues提交反馈。
