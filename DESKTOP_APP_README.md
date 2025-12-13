# AutoGLM Desktop Application

A lightweight desktop application that provides a graphical interface for the AutoGLM phone automation tool.

## Features

- **Easy Configuration**: Configure API settings through a user-friendly interface
- **Device Management**: Check ADB service status and device connection
- **Task Execution**: Execute automation tasks with real-time output
- **Built-in Tutorial**: Step-by-step guide for setup and configuration
- **Cross-platform**: Works on Windows with both batch and PowerShell startup scripts

## Quick Start

### Method 1: Using Batch Script (Windows)

1. Double-click `start_autoglm_desktop.bat`
2. The application will start automatically

### Method 2: Using PowerShell Script (Windows)

1. Open PowerShell in the project directory
2. Run `.\start_autoglm_desktop.ps1`
3. The application will start automatically

### Method 3: Direct Python Execution

1. Open a terminal in the project directory
2. Run `python autoglm_desktop.py`

## Requirements

- Python 3.10 or higher
- ADB (Android Debug Bridge) installed and in PATH
- Android device with USB debugging enabled
- ADB Keyboard installed on the Android device

## Configuration

### API Settings

1. Click on the "Settings" tab
2. Enter your API configuration:
   - **Base URL**: Model API endpoint (e.g., `https://open.bigmodel.cn/api/paas/v4`)
   - **Model Name**: Model name (e.g., `autoglm-phone`)
   - **API Key**: Your API key
   - **Max Steps**: Maximum steps per task (default: 20)
   - **Language**: System prompt language (cn/en)
3. Click "Save Configuration"

### ADB Configuration

1. In the "Settings" tab, you can specify a custom ADB path if needed
2. Click "Start ADB Service" to manually start the ADB service
3. Check the main interface for device connection status

## Usage

1. **Check Device Status**: Verify that ADB is running and a device is connected
2. **Enter Task**: Type your task in the input field (e.g., "Open Meituan and search for nearby hotpot restaurants")
3. **Execute**: Click "Execute Task" to run the automation
4. **Monitor**: Watch the real-time output in the output area

## Tutorial

The "Tutorial" tab provides detailed guides for:
- ADB installation and configuration
- Android device setup
- ADB Keyboard installation and configuration
- API configuration
- Troubleshooting common issues

## Supported Applications

AutoGLM supports 50+ popular Chinese applications including:
- Social: WeChat, QQ, Weibo
- E-commerce: Taobao, JD.com, Pinduoduo
- Food Delivery: Meituan, Ele.me
- Travel: Ctrip, 12306, Didi
- Entertainment: Bilibili, Douyin, iQiyi
- And many more...

## Troubleshooting

### ADB Not Found
1. Download Android SDK Platform Tools: https://developer.android.com/tools/releases/platform-tools
2. Extract to a custom path (e.g., C:\platform-tools)
3. Add the path to your system PATH environment variable
4. Or specify the ADB path in the "Settings" tab

### Device Not Connected
1. Ensure USB debugging is enabled on your Android device
2. Connect the device with a USB cable and authorize debugging
3. Check the device connection status in the main interface
4. Try clicking "Refresh Status" button

### Task Execution Fails
1. Check your API configuration
2. Ensure the device is connected and authorized
3. Review the execution output for error messages
4. Make sure ADB Keyboard is installed and enabled

## File Structure

```
AutoGLM Desktop Application/
├── autoglm_desktop.py          # Main desktop application
├── start_autoglm_desktop.bat    # Batch startup script
├── start_autoglm_desktop.ps1    # PowerShell startup script
├── autoglm_config.json          # Configuration file (auto-generated)
└── DESKTOP_APP_GUIDE.md         # Detailed user guide
```

## Technical Details

The desktop application is built with:
- **GUI Framework**: Tkinter
- **Configuration Storage**: JSON files
- **Background Processing**: Threading for non-blocking operations
- **Command Execution**: Subprocess with proper encoding handling

## License

This project is part of the AutoGLM phone automation tool. Please refer to the main project license for more information.

## Support

For issues and questions:
1. Check the "Tutorial" tab for detailed guides
2. Review the DESKTOP_APP_GUIDE.md file
3. Submit issues to the project repository