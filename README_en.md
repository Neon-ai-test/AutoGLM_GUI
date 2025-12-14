# AutoGLM Desktop Application

[中文文档](README.md)

<!-- <div align="center">
<img src="resources/logo.svg" width="20%"/>
</div>
<p align="center">
    👋 Join our <a href="resources/WECHAT.md" target="_blank">WeChat</a> or <a href="https://discord.gg/QR7SARHRxK" target="_blank">Discord</a> communities
</p>
<p align="center">
    🎤 Experience "voice commands" with our product <a href="https://autoglm.zhipuai.cn/autotyper/" target="_blank">Zhipu AI Input Method</a>
</p> -->

## Project Introduction

AutoGLM Desktop Application is a lightweight desktop application that provides a graphical interface for the AutoGLM phone automation tool. It encapsulates command-line functionality, allowing users to configure APIs, input task commands, check device status, and more through an intuitive GUI interface, greatly simplifying the usage process.

Phone Agent is a mobile intelligent assistant framework built on AutoGLM. It understands phone screen content in a multimodal manner and helps users complete tasks through automated operations. The system controls devices via ADB (Android Debug Bridge), perceives screens using vision-language models, and generates and executes operation workflows through intelligent planning. Users simply describe their needs in natural language, such as "Open Xiaohongshu and search for food," and Phone Agent will automatically parse the intent, understand the current interface, plan the next action, and complete the entire workflow. The system also includes a sensitive operation confirmation mechanism and supports manual takeover during login or verification code scenarios. Additionally, it provides remote ADB debugging capabilities, allowing device connection via WiFi or network for flexible remote control and development.

## Features

- **Easy-to-use GUI Interface**: Provides an intuitive graphical interface, eliminating the need to memorize complex command-line parameters
- **API Configuration Management**: Easily configure Zhipu BigModel API settings through the interface
- **Device Status Monitoring**: Real-time display of ADB service status and device connection
- **Task Execution**: Support natural language task input with real-time execution output
- **Built-in Tutorial**: Provides detailed installation and configuration guides, including ADB and ADB Keyboard setup
- **Configuration Persistence**: Automatically saves user configuration for next startup
- **Multi-platform Startup Scripts**: Provides batch and PowerShell startup scripts to resolve Windows encoding issues

## Quick Start

### Method 1: Using Batch Script (Windows)

1. Double-click `start_autoglm_desktop_enhanced.bat`
2. The application will start automatically

### Method 2: Using PowerShell Script (Windows)

1. Open PowerShell in the project directory
2. Run `.\start_autoglm_desktop_enhanced.ps1`
3. The application will start automatically

### Method 3: Direct Python Execution

1. Open terminal in the project directory
2. Run `python autoglm_desktop_enhanced.py`

## System Requirements

- Python 3.10 or higher
- ADB (Android Debug Bridge) installed and added to PATH
- Android device with USB debugging enabled
- ADB Keyboard installed on Android device

## Usage Guide

### API Configuration

1. Click the "Settings" tab
2. Enter your API configuration:
   - **Base URL**: Model API endpoint (e.g., `https://open.bigmodel.cn/api/paas/v4`)
   - **Model Name**: Model name (e.g., `autoglm-phone`)
   - **API Key**: Your API key
   - **Max Steps**: Maximum steps per task (default: 20)
   - **Language**: System prompt language (Chinese/English)
3. Click "Save Configuration"

### ADB Configuration

1. In the "Settings" tab, specify custom ADB path if needed
2. Click "Start ADB Service" to manually start ADB service
3. Check device connection status on the main interface

### Usage

1. **Check Device Status**: Confirm ADB is running and device is connected
2. **Input Task**: Enter your task in the input box (e.g., "Open Meituan and search for nearby hotpot restaurants")
3. **Execute**: Click "Execute Task" to run automation
4. **Monitor**: View real-time output in the output area

## Tutorial

The "Tutorial" tab provides detailed guides, including:
- ADB installation and configuration
- Android device setup
- ADB Keyboard installation and configuration
- API configuration
- Troubleshooting common issues

## Supported Applications

AutoGLM supports 50+ popular Chinese applications, including:
- Social Communication: WeChat, QQ, Weibo
- E-commerce Shopping: Taobao, JD, Pinduoduo
- Food Delivery: Meituan, Ele.me, KFC
- Travel Tourism: Ctrip, 12306, Didi Chuxing
- Video Entertainment: bilibili, Douyin, iQIYI
- Music Audio: NetEase Cloud Music, QQ Music, Ximalaya
- Life Services: Dianping, Gaode Maps, Baidu Maps
- Content Communities: Xiaohongshu, Zhihu, Douban

## Detailed Usage Guide

### Quick Start

#### 1. Launch the Application

Double-click any of the following files to start the application:
- `start_autoglm_desktop_enhanced.bat` (Windows batch file)
- `start_autoglm_desktop_enhanced.ps1` (PowerShell script)

Or run in command line:
```
python autoglm_desktop_enhanced.py
```

#### 2. First-time Setup

1. **Configure API Information**:
   - Click the "Settings" tab
   - Enter Base URL, model name, and API key
   - Click the "Save Configuration" button

2. **Check Device Status**:
   - View ADB and device connection status in the "Main Interface" tab
   - If ADB is not started, click the "Start ADB Service" button
   - If device is not connected, check USB connection or wireless connection settings

3. **Execute Task**:
   - Enter the task to execute in the task input box
   - For example: "Open Meituan and search for nearby hotpot restaurants"
   - Click the "Execute Task" button
   - View execution output and results

### Feature Description

#### Main Interface

- **Device Status**: Shows ADB service and device connection status
- **Task Input**: Enter task commands to execute
- **Example Tasks**: Provides common task examples, click to quickly fill in
- **Execution Output**: Displays output information during task execution

#### Settings

- **API Configuration**:
  - Base URL: Address of the model API
  - Model Name: Name of the model to use
  - API Key: Key for API authentication
  - Max Steps: Maximum steps for task execution
  - Language: System prompt language (cn/en)

- **ADB Configuration**:
  - ADB Path: Specify the path to the ADB executable (optional)
  - Start ADB Service: Manually start ADB service

#### Tutorial

Provides detailed usage tutorials, including:
- ADB installation and configuration
- Android device configuration
- ADB Keyboard installation and configuration
- API configuration instructions
- Troubleshooting common issues

### Common Issues

#### Q: ADB not found or not installed
A: 
1. Download Android SDK Platform Tools: https://developer.android.com/tools/releases/platform-tools
2. Extract to custom path, such as C:\platform-tools
3. Add the path to system environment variable PATH
4. Or manually specify ADB path in the "Settings" tab

#### Q: Device not connected
A:
1. Ensure Android device has USB debugging enabled
2. Connect device with USB cable and authorize debugging
3. Check if device is displayed in "Device Connection" status
4. Try clicking the "Refresh Status" button

#### Q: Task execution failed
A:
1. Check if API configuration is correct
2. Ensure device is connected and authorized
3. View error information in execution output
4. Ensure ADB Keyboard is installed

#### Q: Text input not working
A:
1. Ensure device has ADB Keyboard installed
2. Enable ADB Keyboard in phone settings
3. Try using command: adb shell ime enable com.android.adbkeyboard/.AdbIME

## Troubleshooting

### ADB Not Found
1. Download Android SDK Platform Tools: https://developer.android.com/tools/releases/platform-tools
2. Extract to custom path (e.g., C:\platform-tools)
3. Add path to system PATH environment variable
4. Or manually specify ADB path in the "Settings" tab

### Device Not Connected
1. Ensure Android device has USB debugging enabled
2. Connect device with USB cable and authorize debugging
3. Check if device is displayed in "Device Connection" status
4. Try clicking the "Refresh Status" button

### Task Execution Failed
1. Check if API configuration is correct
2. Ensure device is connected and authorized
3. View error information in execution output
4. Ensure ADB Keyboard is installed

## File Structure

```
AutoGLM Desktop Application/
├── autoglm_desktop_enhanced.py  # Main desktop application (enhanced version)
├── main.py                      # Command-line version
├── tutorial.md                  # Tutorial documentation (Markdown format)
├── start_autoglm_desktop_enhanced.bat    # Batch startup script (enhanced version)
├── start_autoglm_desktop_enhanced.ps1    # PowerShell startup script (enhanced version)
├── autoglm_config.json          # Configuration file (auto-generated)
├── DESKTOP_APP_GUIDE.md         # Detailed user guide
├── DESKTOP_APP_README.md        # Project overview and quick start
└── DESKTOP_APP_SUMMARY.md       # Development summary and technical details
```

## Technical Details

The desktop application is built using the following technologies:
- **GUI Framework**: CustomTkinter (modern Tkinter alternative)
- **Configuration Storage**: JSON file
- **Background Processing**: Multithreading for non-blocking operations
- **Command Execution**: Subprocess with proper encoding handling
- **Tutorial Rendering**: Markdown parsing and styled display

## Technical Implementation Details

### Architecture Design

The desktop application adopts the following architecture design:
- **Single-file GUI Application**: Easy to distribute and use
- **Configuration Persistence**: Use JSON file to store configuration, simple and reliable
- **Multithreading Processing**: Ensure interface responsiveness, avoid operation blocking
- **Modular Design**: Clear functional separation for easy maintenance and expansion

### Key Feature Implementation

#### 1. ADB Service Detection and Device Management
- Real-time detection of ADB service status
- Automatic ADB service startup functionality
- Real-time display of device connection status
- Support for custom ADB path configuration

#### 2. Task Execution and Output Processing
- Encapsulate command-line parameters into simple GUI operations
- Real-time display of task execution output
- Support for non-blocking handling of long-running tasks
- Friendly display of error messages

#### 3. Configuration Management
- JSON format configuration file storage
- Merge default configuration with user configuration
- Configuration validation and error prompts
- Configuration hot reload functionality

#### 4. Tutorial System
- Built-in Markdown rendering engine
- Styled display with beautification
- Categorized tutorial content
- Real-time updated tutorial documentation

### Key Technical Issues Resolved

#### Windows Encoding Issues
- Resolve Unicode character display issues by setting PYTHONIOENCODING environment variable
- Specify correct encoding parameters in subprocess
- Ensure all output can correctly display Chinese characters

#### Cross-platform Compatibility
- Provide both batch and PowerShell startup scripts
- Automatically detect operating system environment
- Adapt path separators and command formats for different systems

#### User Experience Optimization
- Modern UI design (CustomTkinter framework)
- Intuitive operation flow
- Rich visual feedback and status prompts
- Responsive layout adapting to different screen sizes

### Future Optimization Directions

1. **Multi-device Support**: Allow users to select specific devices for task execution
2. **Task History**: Save execution history for convenient repetition of similar tasks
3. **Log Viewer**: Provide more detailed execution logs and debugging information
4. **Multi-model Support**: Support preset configurations for more model service providers
5. **Auto-update Functionality**: Keep the application at the latest version

## Official Project Links

- **GitHub Repository**: https://github.com/zai-org/Open-AutoGLM
- **Project Homepage**: https://github.com/zai-org/Open-AutoGLM
- **Zhipu AI Input Method**: https://autoglm.zhipuai.cn/autotyper/

## Acknowledgments

This desktop application is developed based on the Open-AutoGLM project. Thanks to the following organizations and individuals for their contributions:

- **Zhipu AI**: Providing AutoGLM model and technical support
- **Open-AutoGLM Development Team**: Building a powerful mobile automation framework
- **All Contributors**: Providing code, documentation, and feedback for the project

## License

This project is licensed under the Apache License 2.0. For details, please see the [LICENSE](LICENSE) file.

Copyright 2025 Zhipu AI

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Support

For questions and issues:
1. Check the "Tutorial" tab for detailed guides
2. Review the "Detailed Usage Guide" section of this README document
3. Submit issues to the project repository

## Changelog

### v1.1.0
- Upgraded GUI framework to CustomTkinter, providing modern interface
- Optimized tutorial document styles with Markdown rendering support
- Beautified interface elements, enhancing user experience
- Added more visual prompts and decorative elements
- Improved code block and quote styles