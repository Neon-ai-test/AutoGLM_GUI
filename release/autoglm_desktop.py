#!/usr/bin/env python3
"""
AutoGLM桌面应用程序 - 轻量级GUI界面
提供API配置、任务输入、设备状态显示等功能
"""

import os
import json
import subprocess
import threading
import time
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

class AutoGLMDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AutoGLM桌面应用程序")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # 配置文件路径
        self.config_file = "autoglm_config.json"
        self.config = self.load_config()
        
        # 执行状态
        self.is_running = False
        self.current_process = None
        
        # 创建界面
        self.create_widgets()
        
        # 启动时检查ADB状态
        self.check_adb_status()
        
    def load_config(self):
        """加载配置文件"""
        default_config = {
            "base_url": "https://open.bigmodel.cn/api/paas/v4",
            "model": "autoglm-phone",
            "api_key": "",
            "max_steps": "100",
            "lang": "cn"
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)
                    # 合并默认配置和加载的配置
                    for key, value in default_config.items():
                        if key not in loaded_config:
                            loaded_config[key] = value
                    return loaded_config
            except Exception as e:
                messagebox.showerror("配置错误", f"加载配置文件失败: {str(e)}")
                return default_config
        else:
            return default_config
    
    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("配置错误", f"保存配置文件失败: {str(e)}")
            return False
    
    def create_widgets(self):
        """创建界面组件"""
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建选项卡
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 主界面选项卡
        self.main_tab = ttk.Frame(notebook)
        notebook.add(self.main_tab, text="主界面")
        self.create_main_tab()
        
        # 设置选项卡
        self.settings_tab = ttk.Frame(notebook)
        notebook.add(self.settings_tab, text="设置")
        self.create_settings_tab()
        
        # 教程选项卡
        self.tutorial_tab = ttk.Frame(notebook)
        notebook.add(self.tutorial_tab, text="教程")
        self.create_tutorial_tab()
        
    def create_main_tab(self):
        """创建主界面"""
        # 设备状态框架
        status_frame = ttk.LabelFrame(self.main_tab, text="设备状态", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # ADB状态
        self.adb_status_var = tk.StringVar(value="检查中...")
        ttk.Label(status_frame, text="ADB状态:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.adb_status_label = ttk.Label(status_frame, textvariable=self.adb_status_var)
        self.adb_status_label.grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # 设备连接状态
        self.device_status_var = tk.StringVar(value="检查中...")
        ttk.Label(status_frame, text="设备连接:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.device_status_label = ttk.Label(status_frame, textvariable=self.device_status_var)
        self.device_status_label.grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # 刷新按钮
        refresh_btn = ttk.Button(status_frame, text="刷新状态", command=self.check_adb_status)
        refresh_btn.grid(row=0, column=2, rowspan=2, padx=(10, 0), pady=2)
        
        # 任务输入框架
        task_frame = ttk.LabelFrame(self.main_tab, text="任务输入", padding="10")
        task_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(task_frame, text="请输入任务指令:").pack(anchor=tk.W)
        self.task_entry = tk.Text(task_frame, height=4)
        self.task_entry.pack(fill=tk.X, pady=5)
        
        # 示例任务
        example_frame = ttk.Frame(task_frame)
        example_frame.pack(fill=tk.X, pady=5)
        ttk.Label(example_frame, text="示例任务:").pack(side=tk.LEFT)
        
        examples = [
            "打开美团搜索附近的火锅店",
            "打开小红书搜索美食攻略",
            "打开淘宝搜索无线耳机"
        ]
        
        for example in examples:
            btn = ttk.Button(example_frame, text=example, 
                           command=lambda e=example: self.set_example_task(e))
            btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # 执行按钮
        self.execute_btn = ttk.Button(task_frame, text="执行任务", command=self.execute_task)
        self.execute_btn.pack(pady=5)
        
        # 执行状态
        self.status_var = tk.StringVar(value="就绪")
        status_label = ttk.Label(task_frame, textvariable=self.status_var)
        status_label.pack(anchor=tk.W)
        
        # 进度条
        self.progress = ttk.Progressbar(task_frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)
        
        # 输出框架
        output_frame = ttk.LabelFrame(self.main_tab, text="执行输出", padding="10")
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = ScrolledText(output_frame, height=10, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
    def create_settings_tab(self):
        """创建设置界面"""
        # API配置框架
        api_frame = ttk.LabelFrame(self.settings_tab, text="API配置", padding="10")
        api_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Base URL
        ttk.Label(api_frame, text="Base URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.base_url_var = tk.StringVar(value=self.config["base_url"])
        base_url_entry = ttk.Entry(api_frame, textvariable=self.base_url_var, width=50)
        base_url_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 模型名称
        ttk.Label(api_frame, text="模型名称:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.model_var = tk.StringVar(value=self.config["model"])
        model_entry = ttk.Entry(api_frame, textvariable=self.model_var, width=50)
        model_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # API密钥
        ttk.Label(api_frame, text="API密钥:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.api_key_var = tk.StringVar(value=self.config["api_key"])
        api_key_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, width=50, show="*")
        api_key_entry.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # 显示/隐藏密钥
        self.show_api_key = tk.BooleanVar(value=False)
        show_key_cb = ttk.Checkbutton(api_frame, text="显示密钥", 
                                     variable=self.show_api_key, 
                                     command=self.toggle_api_key_visibility)
        show_key_cb.grid(row=2, column=2, padx=(5, 0), pady=5)
        
        # 最大步数
        ttk.Label(api_frame, text="最大步数:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.max_steps_var = tk.StringVar(value=self.config["max_steps"])
        max_steps_entry = ttk.Entry(api_frame, textvariable=self.max_steps_var, width=50)
        max_steps_entry.grid(row=3, column=1, sticky=tk.W, pady=5)
        
        # 语言选择
        ttk.Label(api_frame, text="语言:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.lang_var = tk.StringVar(value=self.config["lang"])
        lang_combo = ttk.Combobox(api_frame, textvariable=self.lang_var, 
                                 values=["cn", "en"], state="readonly", width=47)
        lang_combo.grid(row=4, column=1, sticky=tk.W, pady=5)
        
        # 保存按钮
        save_btn = ttk.Button(api_frame, text="保存配置", command=self.save_settings)
        save_btn.grid(row=5, column=0, columnspan=2, pady=10)
        
        # ADB配置框架
        adb_frame = ttk.LabelFrame(self.settings_tab, text="ADB配置", padding="10")
        adb_frame.pack(fill=tk.X)
        
        # ADB路径
        ttk.Label(adb_frame, text="ADB路径:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.adb_path_var = tk.StringVar(value="")
        adb_path_entry = ttk.Entry(adb_frame, textvariable=self.adb_path_var, width=50)
        adb_path_entry.grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # 浏览按钮
        browse_btn = ttk.Button(adb_frame, text="浏览...", command=self.browse_adb_path)
        browse_btn.grid(row=0, column=2, padx=(5, 0), pady=5)
        
        # 启动ADB服务按钮
        start_adb_btn = ttk.Button(adb_frame, text="启动ADB服务", command=self.start_adb_service)
        start_adb_btn.grid(row=1, column=0, columnspan=2, pady=10)
        
    def create_tutorial_tab(self):
        """创建教程界面"""
        # 创建滚动文本框
        tutorial_text = ScrolledText(self.tutorial_tab, state=tk.DISABLED, wrap=tk.WORD)
        tutorial_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 教程内容
        tutorial_content = """
AutoGLM 桌面应用程序使用教程

欢迎使用AutoGLM桌面应用程序！本教程将指导您完成所有必要的设置，以便使用AutoGLM手机自动化功能。

1. ADB (Android Debug Bridge) 安装和配置

ADB是Android调试桥，用于连接和控制Android设备。

1.1 下载ADB:
- 访问官方下载页面: https://developer.android.com/tools/releases/platform-tools?hl=zh-cn
- 下载适合您操作系统的版本
- 解压到自定义路径，例如: C:\\platform-tools

1.2 配置环境变量:
- 在Windows搜索中搜索"环境变量"
- 点击"编辑系统环境变量"
- 点击"环境变量"按钮
- 在"系统变量"中找到"Path"，点击"编辑"
- 点击"新建"，添加ADB解压路径，例如: C:\\platform-tools
- 点击"确定"保存所有更改

1.3 验证安装:
- 打开命令提示符或PowerShell
- 输入: adb version
- 如果显示版本信息，则安装成功

2. Android设备配置

2.1 启用开发者模式:
- 打开手机的"设置"
- 进入"关于手机"
- 连续快速点击"版本号"10次左右
- 直到弹出"开发者模式已启用"的提示

2.2 启用USB调试:
- 返回"设置"主界面
- 进入"开发者选项"(可能在"系统"或"关于手机"中)
- 启用"USB调试"选项
- 部分手机还需要启用"USB调试(安全设置)"

2.3 连接设备:
- 使用USB数据线连接手机和电脑
- 确保数据线支持数据传输(不仅是充电)
- 在手机上授权USB调试连接
- 在命令提示符中输入: adb devices
- 应该显示您的设备信息

2.4 无线连接(可选):
- 确保手机和电脑在同一WiFi网络中
- 在手机上启用"无线调试"
- 记录显示的IP地址和端口
- 使用命令: adb connect <IP地址>:<端口>

3. ADB Keyboard安装和配置

ADB Keyboard用于文本输入，是AutoGLM正常工作所必需的。

3.1 下载ADB Keyboard:
- 访问下载页面: https://github.com/senzhk/ADBKeyBoard/blob/master/ADBKeyboard.apk
- 下载ADBKeyboard.apk文件

3.2 安装ADB Keyboard:
- 将APK文件传输到手机
- 在手机上安装APK文件
- 或者使用ADB命令安装: adb install ADBKeyboard.apk

3.3 启用ADB Keyboard:
- 打开手机"设置"
- 进入"系统" > "语言和输入法" > "虚拟键盘"
- 启用"ADB Keyboard"
- 或者使用ADB命令: adb shell ime enable com.android.adbkeyboard/.AdbIME

4. API配置

AutoGLM支持多种模型服务提供商。

4.1 智谱BigModel:
- Base URL: https://open.bigmodel.cn/api/paas/v4
- 模型名称: autoglm-phone
- API密钥: 在智谱平台申请

4.2 ModelScope(魔搭社区):
- Base URL: https://api-inference.modelscope.cn/v1
- 模型名称: ZhipuAI/AutoGLM-Phone-9B
- API密钥: 在ModelScope平台申请

4.3 本地部署模型:
- Base URL: http://localhost:8000/v1
- 模型名称: autoglm-phone-9b
- API密钥: EMPTY(通常不需要)

5. 使用AutoGLM桌面应用

5.1 配置API:
- 在"设置"选项卡中输入API配置信息
- 点击"保存配置"按钮

5.2 检查设备状态:
- 在"主界面"选项卡中查看ADB和设备连接状态
- 如果ADB未启动，点击"启动ADB服务"按钮
- 如果设备未连接，检查USB连接或无线连接设置

5.3 执行任务:
- 在任务输入框中输入要执行的任务
- 例如: "打开美团搜索附近的火锅店"
- 点击"执行任务"按钮
- 查看执行输出和结果

6. 常见问题解决

6.1 ADB未找到:
- 确保ADB已正确安装并添加到PATH环境变量
- 在"设置"选项卡中手动指定ADB路径

6.2 设备未连接:
- 确保USB调试已启用
- 尝试更换USB端口或数据线
- 检查手机上是否授权了USB调试

6.3 文本输入不工作:
- 确保ADB Keyboard已安装并启用
- 检查手机输入法设置

6.4 截图失败(黑屏):
- 这通常是因为应用显示敏感页面
- AutoGLM会自动检测并请求人工接管

7. 支持的应用

AutoGLM支持50+款主流中文应用，包括:
- 社交通讯: 微信、QQ、微博
- 电商购物: 淘宝、京东、拼多多
- 美食外卖: 美团、饿了么、肯德基
- 出行旅游: 携程、12306、滴滴出行
- 视频娱乐: bilibili、抖音、爱奇艺
- 音乐音频: 网易云音乐、QQ音乐、喜马拉雅
- 生活服务: 大众点评、高德地图、百度地图
- 内容社区: 小红书、知乎、豆瓣

8. 可用操作

Agent可以执行以下操作:
- Launch: 启动应用
- Tap: 点击指定坐标
- Type: 输入文本
- Swipe: 滑动屏幕
- Back: 返回上一页
- Home: 返回桌面
- Long Press: 长按
- Double Tap: 双击
- Wait: 等待页面加载
- Take_over: 请求人工接管(登录/验证码等)

如有其他问题，请参考项目README文档或提交Issue。
        """
        
        # 更新文本框内容
        tutorial_text.config(state=tk.NORMAL)
        tutorial_text.delete(1.0, tk.END)
        tutorial_text.insert(1.0, tutorial_content)
        tutorial_text.config(state=tk.DISABLED)
    
    def toggle_api_key_visibility(self):
        """切换API密钥可见性"""
        if self.show_api_key.get():
            # 显示密钥
            for widget in self.settings_tab.winfo_children():
                if isinstance(widget, ttk.LabelFrame) and widget.cget("text") == "API配置":
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Entry) and child.get() == self.api_key_var.get():
                            child.config(show="")
                            break
                    break
        else:
            # 隐藏密钥
            for widget in self.settings_tab.winfo_children():
                if isinstance(widget, ttk.LabelFrame) and widget.cget("text") == "API配置":
                    for child in widget.winfo_children():
                        if isinstance(child, ttk.Entry) and child.get() == self.api_key_var.get():
                            child.config(show="*")
                            break
                    break
    
    def browse_adb_path(self):
        """浏览ADB路径"""
        filename = filedialog.askopenfilename(
            title="选择ADB可执行文件",
            filetypes=[("可执行文件", "*.exe"), ("所有文件", "*.*")]
        )
        if filename:
            self.adb_path_var.set(filename)
    
    def set_example_task(self, example):
        """设置示例任务"""
        self.task_entry.delete(1.0, tk.END)
        self.task_entry.insert(1.0, example)
    
    def save_settings(self):
        """保存设置"""
        self.config["base_url"] = self.base_url_var.get()
        self.config["model"] = self.model_var.get()
        self.config["api_key"] = self.api_key_var.get()
        self.config["max_steps"] = self.max_steps_var.get()
        self.config["lang"] = self.lang_var.get()
        
        if self.save_config():
            messagebox.showinfo("成功", "配置已保存")
    
    def check_adb_status(self):
        """检查ADB状态"""
        self.adb_status_var.set("检查中...")
        self.device_status_var.set("检查中...")
        
        # 在后台线程中检查ADB状态
        threading.Thread(target=self._check_adb_status_thread, daemon=True).start()
    
    def _check_adb_status_thread(self):
        """在后台线程中检查ADB状态"""
        try:
            # 检查ADB是否安装
            adb_path = self.adb_path_var.get() if self.adb_path_var.get() else "adb"
            result = subprocess.run([adb_path, "version"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.root.after(0, lambda: self.adb_status_var.set("✅ 已安装"))
                
                # 检查设备连接状态
                try:
                    result = subprocess.run([adb_path, "devices"], 
                                          capture_output=True, text=True, timeout=10)
                    lines = result.stdout.strip().split("\n")
                    devices = [line for line in lines[1:] if line.strip() and "\tdevice" in line]
                    
                    if devices:
                        device_ids = [d.split("\t")[0] for d in devices]
                        self.root.after(0, lambda: self.device_status_var.set(f"✅ 已连接 ({len(devices)} 台设备: {', '.join(device_ids)})"))
                    else:
                        self.root.after(0, lambda: self.device_status_var.set("❌ 未连接设备"))
                except Exception as e:
                    self.root.after(0, lambda: self.device_status_var.set(f"❌ 检查失败: {str(e)}"))
            else:
                self.root.after(0, lambda: self.adb_status_var.set("❌ 未安装"))
                self.root.after(0, lambda: self.device_status_var.set("❌ ADB未安装"))
        except FileNotFoundError:
            self.root.after(0, lambda: self.adb_status_var.set("❌ 未找到"))
            self.root.after(0, lambda: self.device_status_var.set("❌ ADB未找到"))
        except Exception as e:
            self.root.after(0, lambda: self.adb_status_var.set(f"❌ 检查失败: {str(e)}"))
            self.root.after(0, lambda: self.device_status_var.set("❌ 无法检查"))
    
    def start_adb_service(self):
        """启动ADB服务"""
        self.status_var.set("正在启动ADB服务...")
        threading.Thread(target=self._start_adb_service_thread, daemon=True).start()
    
    def _start_adb_service_thread(self):
        """在后台线程中启动ADB服务"""
        try:
            adb_path = self.adb_path_var.get() if self.adb_path_var.get() else "adb"
            result = subprocess.run([adb_path, "start-server"], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                self.root.after(0, lambda: self.status_var.set("ADB服务启动成功"))
                # 重新检查状态
                self.root.after(1000, self.check_adb_status)
            else:
                error_msg = result.stderr.strip() if result.stderr else "未知错误"
                self.root.after(0, lambda: self.status_var.set(f"ADB服务启动失败: {error_msg}"))
        except FileNotFoundError:
            self.root.after(0, lambda: self.status_var.set("ADB未找到，请检查安装路径"))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"启动失败: {str(e)}"))
    
    def execute_task(self):
        """执行任务"""
        task = self.task_entry.get(1.0, tk.END).strip()
        if not task:
            messagebox.showwarning("警告", "请输入任务指令")
            return
        
        if self.is_running:
            messagebox.showwarning("警告", "任务正在执行中，请等待完成")
            return
        
        # 检查API配置
        if not self.config["api_key"]:
            messagebox.showwarning("警告", "请先在设置中配置API密钥")
            return
        
        # 检查设备连接状态
        if "未连接" in self.device_status_var.get() or "未找到" in self.device_status_var.get():
            messagebox.showwarning("警告", "设备未连接，请检查ADB和设备连接")
            return
        
        # 开始执行任务
        self.is_running = True
        self.execute_btn.config(state=tk.DISABLED)
        self.status_var.set("正在执行任务...")
        self.progress.start()
        
        # 清空输出
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)
        
        # 在后台线程中执行任务
        threading.Thread(target=self._execute_task_thread, args=(task,), daemon=True).start()
    
    def _execute_task_thread(self, task):
        """在后台线程中执行任务"""
        try:
            # 构建命令
            adb_path = self.adb_path_var.get() if self.adb_path_var.get() else "adb"
            python_cmd = f"python main.py --base-url {self.config['base_url']} --model \"{self.config['model']}\" --apikey \"{self.config['api_key']}\" --max-steps {self.config['max_steps']} --lang {self.config['lang']} \"{task}\""
            
            # 在Windows上使用PowerShell执行
            if os.name == 'nt':
                # 使用PowerShell执行命令，设置UTF-8编码
                ps_cmd = f'powershell -Command "$env:PYTHONIOENCODING=\'utf-8\'; & {python_cmd}"'
                process = subprocess.Popen(ps_cmd, shell=True, stdout=subprocess.PIPE, 
                                         stderr=subprocess.STDOUT, text=True, 
                                         universal_newlines=True, bufsize=1,
                                         encoding='utf-8', errors='replace')
            else:
                process = subprocess.Popen(python_cmd, shell=True, stdout=subprocess.PIPE, 
                                         stderr=subprocess.STDOUT, text=True, 
                                         universal_newlines=True, bufsize=1)
            
            self.current_process = process
            
            # 实时读取输出
            for line in iter(process.stdout.readline, ''):
                if line:
                    self.root.after(0, lambda l=line: self._update_output(l))
            
            # 等待进程完成
            process.wait()
            
            if process.returncode == 0:
                self.root.after(0, lambda: self.status_var.set("任务执行完成"))
            else:
                self.root.after(0, lambda: self.status_var.set(f"任务执行失败，退出码: {process.returncode}"))
                
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"执行错误: {str(e)}"))
        finally:
            self.current_process = None
            self.is_running = False
            self.root.after(0, self._task_finished)
    
    def _update_output(self, line):
        """更新输出文本框"""
        self.output_text.config(state=tk.NORMAL)
        self.output_text.insert(tk.END, line)
        self.output_text.see(tk.END)
        self.output_text.config(state=tk.DISABLED)
    
    def _task_finished(self):
        """任务完成后的清理工作"""
        self.execute_btn.config(state=tk.NORMAL)
        self.progress.stop()


def main():
    """主函数"""
    root = tk.Tk()
    app = AutoGLMDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()