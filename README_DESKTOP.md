# AutoGLM Desktop Application

[官方项目文档](README.md) | [English Documentation](README_en.md)

<div align="center">
<img src="resources/logo.svg" width="20%"/>
</div>
<p align="center">
    👋 加入我们的 <a href="resources/WECHAT.md" target="_blank">微信</a> 社区
</p>
<p align="center">
    🎤 进一步在我们的产品 <a href="https://autoglm.zhipuai.cn/autotyper/" target="_blank">智谱 AI 输入法</a> 体验"用嘴发指令"
</p>

## 项目介绍

AutoGLM Desktop Application 是一个轻量级的桌面应用程序，为 AutoGLM 手机自动化工具提供图形化界面。它封装了命令行功能，使用户能够通过直观的GUI界面配置API、输入任务指令、查看设备状态等，大大简化了使用流程。

Phone Agent 是一个基于 AutoGLM 构建的手机端智能助理框架，它能够以多模态方式理解手机屏幕内容，并通过自动化操作帮助用户完成任务。系统通过 ADB(Android Debug Bridge)来控制设备，以视觉语言模型进行屏幕感知，再结合智能规划能力生成并执行操作流程。用户只需用自然语言描述需求，如"打开小红书搜索美食"，Phone Agent 即可自动解析意图、理解当前界面、规划下一步动作并完成整个流程。系统还内置敏感操作确认机制，并支持在登录或验证码场景下进行人工接管。同时，它提供远程 ADB 调试能力，可通过 WiFi 或网络连接设备，实现灵活的远程控制与开发。

## 特性

- **简单易用的GUI界面**：提供直观的图形界面，无需记忆复杂的命令行参数
- **API配置管理**：通过界面轻松配置API设置，支持多种模型服务提供商
- **设备状态监控**：实时显示ADB服务状态和设备连接情况
- **任务执行**：支持自然语言任务输入，实时显示执行输出
- **内置教程**：提供详细的安装和配置指南，包括ADB和ADB Keyboard设置
- **配置持久化**：自动保存用户配置，下次启动时自动加载
- **多平台启动脚本**：提供批处理和PowerShell启动脚本，解决Windows编码问题

## 快速开始

### 方法1：使用批处理脚本（Windows）

1. 双击 `start_autoglm_desktop.bat`
2. 应用程序将自动启动

### 方法2：使用PowerShell脚本（Windows）

1. 在项目目录中打开PowerShell
2. 运行 `.\start_autoglm_desktop.ps1`
3. 应用程序将自动启动

### 方法3：直接运行Python

1. 在项目目录中打开终端
2. 运行 `python autoglm_desktop.py`

## 系统要求

- Python 3.10或更高版本
- ADB（Android Debug Bridge）已安装并添加到PATH
- 已启用USB调试的Android设备
- Android设备上已安装ADB Keyboard

## 使用指南

### API配置

1. 点击"设置"选项卡
2. 输入您的API配置：
   - **Base URL**：模型API端点（例如：`https://open.bigmodel.cn/api/paas/v4`）
   - **模型名称**：模型名称（例如：`autoglm-phone`）
   - **API密钥**：您的API密钥
   - **最大步数**：每个任务的最大步数（默认：20）
   - **语言**：系统提示语言（中文/英文）
3. 点击"保存配置"

### ADB配置

1. 在"设置"选项卡中，如果需要可以指定自定义ADB路径
2. 点击"启动ADB服务"手动启动ADB服务
3. 在主界面检查设备连接状态

### 使用方法

1. **检查设备状态**：确认ADB正在运行且设备已连接
2. **输入任务**：在输入框中输入您的任务（例如："打开美团搜索附近的火锅店"）
3. **执行**：点击"执行任务"运行自动化
4. **监控**：在输出区域查看实时输出

## 教程

"教程"选项卡提供详细指南，包括：
- ADB安装和配置
- Android设备设置
- ADB Keyboard安装和配置
- API配置
- 常见问题解决

## 支持的应用

AutoGLM支持50+款热门中文应用，包括：
- 社交通讯：微信、QQ、微博
- 电商购物：淘宝、京东、拼多多
- 美食外卖：美团、饿了么、肯德基
- 出行旅游：携程、12306、滴滴出行
- 视频娱乐：bilibili、抖音、爱奇艺
- 音乐音频：网易云音乐、QQ音乐、喜马拉雅
- 生活服务：大众点评、高德地图、百度地图
- 内容社区：小红书、知乎、豆瓣

## 故障排除

### ADB未找到
1. 下载Android SDK Platform Tools：https://developer.android.com/tools/releases/platform-tools
2. 解压到自定义路径（例如：C:\platform-tools）
3. 将路径添加到系统PATH环境变量
4. 或在"设置"选项卡中手动指定ADB路径

### 设备未连接
1. 确保Android设备已启用USB调试
2. 使用USB数据线连接设备并授权调试
3. 检查设备是否显示在"设备连接"状态中
4. 尝试点击"刷新状态"按钮

### 任务执行失败
1. 检查API配置是否正确
2. 确保设备已连接并授权
3. 查看执行输出中的错误信息
4. 确保已安装ADB Keyboard

## 文件结构

```
AutoGLM Desktop Application/
├── autoglm_desktop.py          # 主桌面应用程序
├── start_autoglm_desktop.bat    # 批处理启动脚本
├── start_autoglm_desktop.ps1    # PowerShell启动脚本
├── create_shortcut.bat          # 创建桌面快捷方式脚本
├── autoglm_config.json          # 配置文件（自动生成）
├── DESKTOP_APP_GUIDE.md         # 详细用户指南
├── DESKTOP_APP_README.md        # 项目概述和快速入门
├── DESKTOP_APP_SUMMARY.md       # 开发总结和技术细节
└── release/                     # 发布版本目录
    ├── autoglm_desktop.py       # 桌面应用程序（发布版本）
    ├── AutoGLM桌面应用.bat       # 批处理启动脚本（发布版本）
    ├── AutoGLM桌面应用.ps1       # PowerShell启动脚本（发布版本）
    └── DESKTOP_APP_GUIDE.md      # 用户指南（发布版本）
```

## 技术细节

桌面应用程序使用以下技术构建：
- **GUI框架**：Tkinter
- **配置存储**：JSON文件
- **后台处理**：多线程用于非阻塞操作
- **命令执行**：Subprocess，正确处理编码

## 官方项目链接

- **GitHub仓库**：https://github.com/zai-org/Open-AutoGLM
- **项目主页**：https://github.com/zai-org/Open-AutoGLM
- **智谱AI输入法**：https://autoglm.zhipuai.cn/autotyper/

## 鸣谢

本桌面应用程序基于Open-AutoGLM项目开发，感谢以下组织和个人的贡献：

- **智谱AI（Zhipu AI）**：提供AutoGLM模型和技术支持
- **Open-AutoGLM开发团队**：构建了强大的手机自动化框架
- **所有贡献者**：为项目提供代码、文档和反馈

## 许可证

本项目是AutoGLM手机自动化工具的一部分。请参考主项目许可证获取更多信息。

## 支持

如有问题和疑问：
1. 查看"教程"选项卡获取详细指南
2. 阅读DESKTOP_APP_GUIDE.md文件
3. 向项目仓库提交问题

## 更新日志

### v1.0.0
- 初始版本发布
- 提供基本的GUI界面
- 支持API配置和任务执行
- 集成ADB状态检查和设备管理
- 包含详细的使用教程
- 解决Windows编码问题