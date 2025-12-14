#!/usr/bin/env python3
#
# Copyright 2025 Zhipu AI
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
AutoGLM桌面应用程序 - 美化版
使用CustomTkinter提供现代化的UI界面
提供API配置、任务输入、设备状态显示等功能
"""

import os
import json
import subprocess
import threading
import time
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import markdown2
import customtkinter as ctk

# 设置CustomTkinter外观
ctk.set_appearance_mode("light")  # 可选: "light", "dark", "system"
ctk.set_default_color_theme("blue")  # 可选: "blue", "green", "dark-blue"

# 自定义颜色方案
COLORS = {
    "primary": "#1E6BA8",      # 主色调 - 深蓝色
    "primary_light": "#E8F4FD",  # 主色调浅色背景
    "secondary": "#F0F0F0",    # 次要背景色
    "accent": "#FF6B6B",       # 强调色 - 珊瑚红
    "success": "#4CAF50",      # 成功状态 - 绿色
    "warning": "#FF9800",      # 警告状态 - 橙色
    "warning_light": "#FFF3E0", # 警告状态浅色背景
    "error": "#F44336",        # 错误状态 - 红色
    "text_primary": "#212121",  # 主要文本色
    "text_secondary": "#757575", # 次要文本色
    "border": "#E0E0E0",       # 边框颜色
    "card_bg": "#FFFFFF",      # 卡片背景色
    "status_ok": "#4CAF50",    # 状态正常 - 绿色
    "status_warning": "#FF9800", # 状态警告 - 橙色
    "status_error": "#F44336",  # 状态错误 - 红色
    "status_checking": "#2196F3", # 状态检查中 - 蓝色
}

class ToolTip:
    """工具提示类，用于显示悬停提示"""
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.widget.bind("<Enter>", self.show_tip)
        self.widget.bind("<Leave>", self.hide_tip)
    
    def show_tip(self, event=None):
        """显示提示"""
        if self.tip_window or not self.text:
            return
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        self.tip_window = tk.Toplevel(self.widget)
        self.tip_window.wm_overrideredirect(True)
        self.tip_window.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tip_window, text=self.text, 
                        background="#FFFFDD", relief="solid", borderwidth=1,
                        font=("Arial", "10", "normal"))
        label.pack()
    
    def hide_tip(self, event=None):
        """隐藏提示"""
        tip_window = self.tip_window
        self.tip_window = None
        if tip_window:
            tip_window.destroy()

class StatusIndicator:
    """状态指示器类，用于显示状态和动画"""
    def __init__(self, parent, width=20, height=20):
        self.parent = parent
        self.width = width
        self.height = height
        self.canvas = tk.Canvas(parent, width=width, height=height, 
                               bg=COLORS["card_bg"], highlightthickness=0)
        self.status = "unknown"
        self.animation_id = None
        self.pulse_count = 0
        
    def set_status(self, status, animate=False):
        """设置状态"""
        self.status = status
        self.canvas.delete("all")
        
        # 根据状态选择颜色
        if status == "ok" or status == "success":
            color = COLORS["status_ok"]
        elif status == "warning":
            color = COLORS["status_warning"]
        elif status == "error":
            color = COLORS["status_error"]
        elif status == "checking" or status == "loading":
            color = COLORS["status_checking"]
            if animate:
                self._animate_checking()
        else:
            color = COLORS["text_secondary"]
        
        # 绘制状态圆圈
        self.canvas.create_oval(2, 2, self.width-2, self.height-2, 
                               fill=color, outline="")
        
        # 如果是成功状态，添加勾选标记
        if status == "ok" or status == "success":
            self.canvas.create_line(5, self.height//2, self.width//2-2, self.height-5, 
                                   fill="white", width=2)
            self.canvas.create_line(self.width//2-2, self.height-5, self.width-5, 5, 
                                   fill="white", width=2)
        # 如果是错误状态，添加X标记
        elif status == "error":
            self.canvas.create_line(5, 5, self.width-5, self.height-5, 
                                   fill="white", width=2)
            self.canvas.create_line(self.width-5, 5, 5, self.height-5, 
                                   fill="white", width=2)
        # 如果是警告状态，添加感叹号
        elif status == "warning":
            self.canvas.create_text(self.width//2, self.height//2-2, 
                                   text="!", fill="white", 
                                   font=("Arial", 12, "bold"))
    
    def _animate_checking(self):
        """动画效果：检查中状态"""
        if self.status != "checking" and self.status != "loading":
            return
            
        self.canvas.delete("all")
        
        # 计算动画阶段
        phase = self.pulse_count % 6
        
        # 绘制不同阶段的圆圈
        if phase < 3:
            # 扩大阶段
            size = 2 + phase * 2
            alpha = 255 - phase * 50
        else:
            # 缩小阶段
            size = 8 - (phase - 3) * 2
            alpha = 100 + (phase - 3) * 50
            
        # 绘制圆圈
        self.canvas.create_oval(
            self.width//2 - size, self.height//2 - size,
            self.width//2 + size, self.height//2 + size,
            fill=COLORS["status_checking"], outline=""
        )
        
        self.pulse_count += 1
        self.animation_id = self.parent.after(200, self._animate_checking)
    
    def stop_animation(self):
        """停止动画"""
        if self.animation_id:
            self.parent.after_cancel(self.animation_id)
            self.animation_id = None
        self.pulse_count = 0

class AutoGLMDesktopApp:
    def __init__(self):
        # 创建主窗口
        self.root = ctk.CTk()
        self.root.title("AutoGLM桌面应用程序 - 美化版")
        self.root.geometry("1200x750")
        self.root.resizable(True, True)
        
        # 设置窗口最小尺寸
        self.root.minsize(1000, 650)
        
        # 配置文件路径
        self.config_file = "autoglm_config.json"
        self.config = self.load_config()
        
        # 执行状态
        self.is_running = False
        self.current_process = None
        
        # 创建界面
        self.create_widgets()
        
        # 设置窗口关闭事件处理
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # 启动时检查ADB状态
        self.check_adb_status()
        
        # 初始化任务状态指示器
        self.task_indicator.set_status("ok")
        
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
        # 创建选项卡
        self.tabview = ctk.CTkTabview(self.root)
        # 将选项卡控件填充到父容器，使其随窗口大小自动扩展，四周留 10 像素边距
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # 创建选项卡
        self.tab_main = self.tabview.add("主界面")
        self.tab_settings = self.tabview.add("设置")
        self.tab_tutorial = self.tabview.add("教程")
        
        # 创建各选项卡内容
        self.create_main_tab()
        self.create_settings_tab()
        self.create_tutorial_tab()
        
    def create_main_tab(self):
        """创建主界面"""
        # 主框架 - 添加背景色
        self.main_frame = ctk.CTkFrame(self.tab_main)
        self.main_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # 创建三栏固定宽度布局
        self.create_three_column_layout()
        
    def create_three_column_layout(self):
        """创建三栏固定宽度布局：左侧状态，中间操作，右侧输出"""
        # 左侧状态栏 - 固定宽度250px
        left_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS["card_bg"], corner_radius=12, width=250)
        left_frame.pack(side="left", fill="y", padx=(15, 8), pady=15)
        left_frame.pack_propagate(False)  # 防止框架被内容撑大
        
        # 中间操作区 - 固定宽度450px
        middle_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS["card_bg"], corner_radius=12, width=450)
        middle_frame.pack(side="left", fill="y", padx=8, pady=15)
        middle_frame.pack_propagate(False)  # 防止框架被内容撑大
        
        # 右侧输出区 - 剩余空间
        right_frame = ctk.CTkFrame(self.main_frame, fg_color=COLORS["card_bg"], corner_radius=12)
        right_frame.pack(side="right", fill="both", expand=True, padx=(8, 15), pady=15)
        
        # 创建各栏内容
        self.create_status_panel(left_frame)
        self.create_operation_panel(middle_frame)
        self.create_output_panel(right_frame)
        
    def create_status_panel(self, parent):
        """创建左侧状态面板"""
        # 标题 - 使用主色调
        title_container = ctk.CTkFrame(parent, fg_color=COLORS["primary"], corner_radius=8)
        title_container.pack(fill="x", padx=15, pady=(15, 10))
        
        title_label = ctk.CTkLabel(title_container, text="系统状态", 
                                  font=ctk.CTkFont(size=18, weight="bold"),
                                  text_color="white")
        title_label.pack(pady=10)
        
        # ADB状态框架
        adb_frame = ctk.CTkFrame(parent, fg_color=COLORS["primary_light"], 
                                corner_radius=8, border_width=1, 
                                border_color=COLORS["primary"])
        adb_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # ADB状态标题
        adb_title = ctk.CTkLabel(adb_frame, text="ADB状态", 
                                font=ctk.CTkFont(size=14, weight="bold"),
                                text_color=COLORS["primary"])
        adb_title.pack(anchor="w", padx=10, pady=(10, 5))
        
        # ADB状态指示器和文本
        adb_status_frame = ctk.CTkFrame(adb_frame, fg_color="transparent")
        adb_status_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.adb_indicator = StatusIndicator(adb_status_frame, width=20, height=20)
        self.adb_indicator.canvas.pack(side="left", padx=(0, 8))
        
        self.adb_status_var = tk.StringVar(value="检查中...")
        self.adb_status_label = ctk.CTkLabel(adb_status_frame, textvariable=self.adb_status_var, 
                                           font=ctk.CTkFont(size=12))
        self.adb_status_label.pack(side="left")
        
        # 设备状态框架
        device_frame = ctk.CTkFrame(parent, fg_color=COLORS["primary_light"], 
                                   corner_radius=8, border_width=1, 
                                   border_color=COLORS["primary"])
        device_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # 设备状态标题
        device_title = ctk.CTkLabel(device_frame, text="设备状态", 
                                   font=ctk.CTkFont(size=14, weight="bold"),
                                   text_color=COLORS["primary"])
        device_title.pack(anchor="w", padx=10, pady=(10, 5))
        
        # 设备状态指示器和文本
        device_status_frame = ctk.CTkFrame(device_frame, fg_color="transparent")
        device_status_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.device_indicator = StatusIndicator(device_status_frame, width=20, height=20)
        self.device_indicator.canvas.pack(side="left", padx=(0, 8))
        
        self.device_status_var = tk.StringVar(value="检查中...")
        self.device_status_label = ctk.CTkLabel(device_status_frame, textvariable=self.device_status_var, 
                                              font=ctk.CTkFont(size=12))
        self.device_status_label.pack(side="left")
        
        # 任务状态框架
        task_frame = ctk.CTkFrame(parent, fg_color=COLORS["primary_light"], 
                                 corner_radius=8, border_width=1, 
                                 border_color=COLORS["primary"])
        task_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # 任务状态标题
        task_title = ctk.CTkLabel(task_frame, text="任务状态", 
                                 font=ctk.CTkFont(size=14, weight="bold"),
                                 text_color=COLORS["primary"])
        task_title.pack(anchor="w", padx=10, pady=(10, 5))
        
        # 任务状态指示器和文本
        task_status_frame = ctk.CTkFrame(task_frame, fg_color="transparent")
        task_status_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.task_indicator = StatusIndicator(task_status_frame, width=20, height=20)
        self.task_indicator.canvas.pack(side="left", padx=(0, 8))
        
        self.status_var = tk.StringVar(value="就绪")
        self.task_status_label = ctk.CTkLabel(task_status_frame, textvariable=self.status_var, 
                                            font=ctk.CTkFont(size=12))
        self.task_status_label.pack(side="left")
        
        # 进度条框架
        progress_frame = ctk.CTkFrame(parent, fg_color=COLORS["primary_light"], 
                                     corner_radius=8, border_width=1, 
                                     border_color=COLORS["primary"])
        progress_frame.pack(fill="x", padx=15, pady=(0, 10))
        
        # 进度条标题
        progress_title = ctk.CTkLabel(progress_frame, text="任务进度", 
                                     font=ctk.CTkFont(size=14, weight="bold"),
                                     text_color=COLORS["primary"])
        progress_title.pack(anchor="w", padx=10, pady=(10, 5))
        
        # 进度条
        self.progress = ctk.CTkProgressBar(progress_frame, progress_color=COLORS["primary"])
        self.progress.pack(fill="x", padx=10, pady=(0, 10))
        self.progress.set(0)
        
        # 刷新按钮
        refresh_btn = ctk.CTkButton(parent, text="🔄 刷新状态", 
                                  command=self.check_adb_status,
                                  fg_color=COLORS["accent"], hover_color="#E55A5A",
                                  height=32, corner_radius=6)
        refresh_btn.pack(pady=10, padx=15, fill="x")
        # 添加工具提示
        ToolTip(refresh_btn, "检查ADB服务和设备连接状态")
    
    def create_operation_panel(self, parent):
        """创建中间操作面板"""
        # 任务输入框架
        task_frame = ctk.CTkFrame(parent, fg_color="transparent")
        task_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        # 标题 - 使用主色调
        task_title_container = ctk.CTkFrame(task_frame, fg_color=COLORS["primary"], corner_radius=8)
        task_title_container.pack(fill="x", padx=15, pady=(0, 15))
        
        task_title = ctk.CTkLabel(task_title_container, text="任务操作", 
                                font=ctk.CTkFont(size=18, weight="bold"),
                                text_color="white")
        task_title.pack(pady=10)
        
        # 任务输入说明
        task_desc = ctk.CTkLabel(task_frame, text="请输入任务指令:", 
                                font=ctk.CTkFont(size=14, weight="normal"),
                                text_color=COLORS["text_primary"])
        task_desc.pack(anchor="w", padx=15, pady=(0, 5))
        
        # 任务输入框 - 固定高度
        self.task_entry = ctk.CTkTextbox(task_frame, height=100, 
                                        border_width=1, border_color=COLORS["border"],
                                        corner_radius=8, fg_color=COLORS["card_bg"])
        self.task_entry.pack(fill="x", padx=15, pady=(5, 10))
        
        # 示例任务框架
        example_frame = ctk.CTkFrame(task_frame, fg_color=COLORS["primary_light"], 
                                    corner_radius=8, border_width=1, 
                                    border_color=COLORS["primary"])
        example_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        example_label = ctk.CTkLabel(example_frame, text="示例任务:", 
                                    font=ctk.CTkFont(size=14, weight="bold"),
                                    text_color=COLORS["primary"])
        example_label.pack(anchor="w", padx=(15, 10), pady=(10, 5))
        
        # 示例任务按钮 - 两列排列，改进样式
        examples_container = ctk.CTkFrame(example_frame, fg_color="transparent")
        examples_container.pack(fill="x", padx=15, pady=(0, 10))
        
        examples = [
            "打开美团搜索附近的火锅店",
            "打开小红书搜索美食攻略",
            "打开淘宝搜索无线耳机",    
            "打开高德地图导航到公司",
            "打开哔哩哔哩观看科技视频"
        ]
        
        # 创建两列布局
        left_column = ctk.CTkFrame(examples_container, fg_color="transparent")
        left_column.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        right_column = ctk.CTkFrame(examples_container, fg_color="transparent")
        right_column.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # 分配示例到两列
        for i, example in enumerate(examples):
            column = left_column if i % 2 == 0 else right_column
            btn = ctk.CTkButton(column, text=f"{example}", 
                             command=lambda e=example: self.set_example_task(e),
                             fg_color="transparent", text_color=COLORS["text_primary"],
                             border_width=1, border_color=COLORS["border"],
                             hover_color=COLORS["primary_light"],
                             height=30, corner_radius=6, anchor="w")
            btn.pack(fill="x", pady=3)
            # 添加工具提示
            ToolTip(btn, f"点击使用示例: {example}")
        
        # 执行按钮 - 使用主色调，增加尺寸
        self.execute_btn = ctk.CTkButton(task_frame, text="🚀 执行任务", 
                                       command=self.execute_task,
                                       height=45, font=ctk.CTkFont(size=16, weight="bold"),
                                       fg_color=COLORS["primary"], hover_color="#155A8E",
                                       corner_radius=8)
        self.execute_btn.pack(pady=(15, 10), padx=15, fill="x")
    
    def create_output_panel(self, parent):
        """创建右侧输出面板"""
        # 标题 - 使用主色调
        title_container = ctk.CTkFrame(parent, fg_color=COLORS["primary"], corner_radius=8)
        title_container.pack(fill="x", padx=15, pady=(15, 10))
        
        output_title = ctk.CTkLabel(title_container, text="执行输出", 
                                   font=ctk.CTkFont(size=18, weight="bold"),
                                   text_color="white")
        output_title.pack(pady=10)
        
        # 输出文本框 - 固定字体大小
        self.output_text = ctk.CTkTextbox(parent, 
                                        border_width=1, border_color=COLORS["border"],
                                        corner_radius=8, fg_color=COLORS["card_bg"],
                                        font=ctk.CTkFont(family="Consolas", size=12))
        self.output_text.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # 设置文本框为只读模式
        self.output_text.configure(state="disabled")
        
        # 添加输出控制按钮区域
        controls_frame = ctk.CTkFrame(parent, fg_color="transparent")
        controls_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # 清空输出按钮
        clear_btn = ctk.CTkButton(controls_frame, text="🗑️ 清空输出", 
                                command=self.clear_output,
                                fg_color=COLORS["warning"], hover_color="#E68900",
                                height=32, width=120, corner_radius=6)
        clear_btn.pack(side="left", padx=(0, 10))
        
        # 复制输出按钮
        copy_btn = ctk.CTkButton(controls_frame, text="📋 复制输出", 
                               command=self.copy_output,
                               fg_color=COLORS["success"], hover_color="#45A049",
                               height=32, width=120, corner_radius=6)
        copy_btn.pack(side="left", padx=(0, 10))
        
        # 保存输出按钮
        save_btn = ctk.CTkButton(controls_frame, text="💾 保存输出", 
                               command=self.save_output,
                               fg_color=COLORS["primary"], hover_color="#155A8E",
                               height=32, width=120, corner_radius=6)
        save_btn.pack(side="left")
        
    def create_settings_tab(self):
        """创建设置界面"""
        # 主框架
        settings_frame = ctk.CTkFrame(self.tab_settings)
        settings_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # 创建左右两栏布局
        left_column = ctk.CTkFrame(settings_frame, fg_color="transparent")
        left_column.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        right_column = ctk.CTkFrame(settings_frame, fg_color="transparent")
        right_column.pack(side="right", fill="both", expand=True, padx=(0, 10), pady=10)
        
        # 左侧：API配置区域
        self.create_api_config_section(left_column)
        
        # 右侧：ADB使用说明区域
        self.create_adb_info_section(right_column)
    
    def create_api_config_section(self, parent):
        """创建API配置区域"""
        # 配置容器框架
        config_container = ctk.CTkFrame(parent, corner_radius=15, fg_color=COLORS["card_bg"])
        config_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # 标题区域
        title_frame = ctk.CTkFrame(config_container, corner_radius=12, fg_color=COLORS["primary"])
        title_frame.pack(fill="x", padx=15, pady=(15, 0))
        
        api_title = ctk.CTkLabel(title_frame, text="API配置", 
                                font=ctk.CTkFont(size=20, weight="bold"),
                                text_color="white")
        api_title.pack(pady=15)
        
        # 配置项容器
        config_items = ctk.CTkScrollableFrame(config_container, fg_color="transparent")
        config_items.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Base URL
        self.create_config_item(config_items, "Base URL:", "base_url", 
                               "API服务地址，例如：https://open.bigmodel.cn/api/paas/v4")
        
        # 模型名称
        self.create_config_item(config_items, "模型名称:", "model", 
                               "模型名称，例如：autoglm-phone")
        
        # API密钥
        self.create_config_item(config_items, "API密钥:", "api_key", 
                               "API访问密钥", password=True)
        
        # 最大步数
        self.create_config_item(config_items, "最大步数:", "max_steps", 
                               "任务执行的最大步数，建议10-20")
        
        # 语言选择
        self.create_config_item(config_items, "语言:", "lang", 
                               "界面语言", options=["cn", "en"])
        
        # 保存按钮区域
        button_frame = ctk.CTkFrame(config_container, fg_color="transparent")
        button_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        save_btn = ctk.CTkButton(button_frame, text="💾 保存配置", 
                               command=self.save_settings,
                               height=45, font=ctk.CTkFont(size=16, weight="bold"),
                               fg_color=COLORS["success"], hover_color="#28a745",
                               corner_radius=10)
        save_btn.pack(fill="x")
    
    def create_config_item(self, parent, label_text, var_name, hint_text, password=False, options=None):
        """创建单个配置项"""
        # 配置项框架
        item_frame = ctk.CTkFrame(parent, fg_color=COLORS["primary_light"], 
                                 corner_radius=10, border_width=1, 
                                 border_color=COLORS["border"])
        item_frame.pack(fill="x", pady=(0, 10))
        
        # 标签
        label = ctk.CTkLabel(item_frame, text=label_text, 
                           font=ctk.CTkFont(size=14, weight="bold"),
                           text_color=COLORS["text_primary"])
        label.pack(anchor="w", padx=15, pady=(12, 5))
        
        # 输入控件容器
        input_container = ctk.CTkFrame(item_frame, fg_color="transparent")
        input_container.pack(fill="x", padx=15, pady=(0, 5))
        
        # 创建变量
        var = tk.StringVar(value=self.config[var_name])
        setattr(self, f"{var_name}_var", var)
        
        # 根据类型创建不同的输入控件
        if options:
            # 下拉框
            input_widget = ctk.CTkComboBox(input_container, variable=var, 
                                         values=options, width=300, height=32)
            input_widget.pack(side="left", fill="x", expand=True)
        else:
            # 文本框
            show_var = None
            if password:
                # 密码框和显示/隐藏选项
                input_widget = ctk.CTkEntry(input_container, textvariable=var, 
                                         width=300, height=32, show="*")
                input_widget.pack(side="left", fill="x", expand=True, padx=(0, 10))
                
                # 显示/隐藏复选框
                show_var = tk.BooleanVar(value=False)
                show_cb = ctk.CTkCheckBox(input_container, text="显示", 
                                        variable=show_var, 
                                        command=lambda: self.toggle_password_visibility(var_name, var, show_var))
                show_cb.pack(side="right")
                
                # 保存引用以便后续使用
                setattr(self, f"show_{var_name}", show_var)
                setattr(self, f"{var_name}_entry", input_widget)
            else:
                # 普通文本框
                input_widget = ctk.CTkEntry(input_container, textvariable=var, 
                                         width=300, height=32)
                input_widget.pack(side="left", fill="x", expand=True)
        
        # 提示文本
        hint = ctk.CTkLabel(item_frame, text=hint_text, 
                          font=ctk.CTkFont(size=11),
                          text_color=COLORS["text_secondary"])
        hint.pack(anchor="w", padx=15, pady=(0, 10))
        
        return var
    
    def toggle_password_visibility(self, var_name, var, show_var):
        """切换密码可见性"""
        entry_widget = getattr(self, f"{var_name}_entry")
        if show_var.get():
            entry_widget.configure(show="")
        else:
            entry_widget.configure(show="*")
    
    def create_adb_info_section(self, parent):
        """创建ADB使用说明区域"""
        # 说明容器框架
        info_container = ctk.CTkFrame(parent, corner_radius=15, fg_color=COLORS["card_bg"])
        info_container.pack(fill="both", expand=True, padx=0, pady=0)
        
        # 标题区域
        title_frame = ctk.CTkFrame(info_container, corner_radius=12, fg_color=COLORS["accent"])
        title_frame.pack(fill="x", padx=15, pady=(15, 0))
        
        adb_title = ctk.CTkLabel(title_frame, text="ADB使用说明", 
                                font=ctk.CTkFont(size=20, weight="bold"),
                                text_color="white")
        adb_title.pack(pady=15)
        
        # 说明内容区域
        info_content = ctk.CTkScrollableFrame(info_container, fg_color="transparent")
        info_content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # 重要提示
        warning_frame = ctk.CTkFrame(info_content, fg_color=COLORS["warning_light"], 
                                    corner_radius=10, border_width=1, 
                                    border_color=COLORS["warning"])
        warning_frame.pack(fill="x", pady=(0, 15))
        
        warning_icon = ctk.CTkLabel(warning_frame, text="⚠️", 
                                  font=ctk.CTkFont(size=20))
        warning_icon.pack(side="left", padx=15, pady=15)
        
        warning_text = ctk.CTkLabel(warning_frame, 
                                  text="本应用程序要求ADB必须添加到系统环境变量中，不支持手动指定ADB路径。",
                                  font=ctk.CTkFont(size=13, weight="bold"),
                                  text_color=COLORS["warning"])
        warning_text.pack(side="left", padx=(0, 15), pady=15)
        
        # 步骤说明
        steps_frame = ctk.CTkFrame(info_content, fg_color=COLORS["primary_light"], 
                                 corner_radius=10, border_width=1, 
                                 border_color=COLORS["border"])
        steps_frame.pack(fill="x", pady=(0, 15))
        
        steps_title = ctk.CTkLabel(steps_frame, text="配置步骤:", 
                                  font=ctk.CTkFont(size=15, weight="bold"),
                                  text_color=COLORS["text_primary"])
        steps_title.pack(anchor="w", padx=15, pady=(12, 8))
        
        steps = [
            "1. 下载并安装Android SDK Platform-Tools",
            "2. 将ADB路径添加到系统PATH环境变量中",
            "3. 在命令提示符中输入\"adb version\"验证安装是否成功"
        ]
        
        for step in steps:
            step_label = ctk.CTkLabel(steps_frame, text=step, 
                                    font=ctk.CTkFont(size=13),
                                    text_color=COLORS["text_primary"])
            step_label.pack(anchor="w", padx=15, pady=(0, 5))
        
        # 详细方法
        method_frame = ctk.CTkFrame(info_content, fg_color=COLORS["primary_light"], 
                                  corner_radius=10, border_width=1, 
                                  border_color=COLORS["border"])
        method_frame.pack(fill="both", expand=True)
        
        method_title = ctk.CTkLabel(method_frame, text="添加到环境变量的方法:", 
                                  font=ctk.CTkFont(size=15, weight="bold"),
                                  text_color=COLORS["text_primary"])
        method_title.pack(anchor="w", padx=15, pady=(12, 8))
        
        method_steps = [
            "1. 右键点击\"此电脑\" → \"属性\" → \"高级系统设置\" → \"环境变量\"",
            "2. 在\"系统变量\"中找到或创建\"Path\"变量",
            "3. 点击\"编辑\" → \"新建\" → 添加ADB所在路径（例如：C:\\platform-tools）",
            "4. 点击\"确定\"保存所有更改"
        ]
        
        for step in method_steps:
            step_label = ctk.CTkLabel(method_frame, text=step, 
                                    font=ctk.CTkFont(size=13),
                                    text_color=COLORS["text_primary"])
            step_label.pack(anchor="w", padx=15, pady=(0, 5))
        
    def create_tutorial_tab(self):
        """创建教程界面"""
        # 主框架
        tutorial_frame = ctk.CTkFrame(self.tab_tutorial)
        tutorial_frame.pack(fill="both", expand=True, padx=0, pady=0)
        
        # 创建顶部标题区域
        header_frame = ctk.CTkFrame(tutorial_frame, fg_color=COLORS["primary_light"], 
                                   corner_radius=0, height=80)
        header_frame.pack(fill="x", padx=0, pady=(0, 10))
        header_frame.pack_propagate(False)
        
        # 标题图标和文本
        title_container = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_container.pack(expand=True)
        
        title_label = ctk.CTkLabel(title_container, 
                                  text="📚 AutoGLM 使用教程",
                                  font=ctk.CTkFont(size=24, weight="bold"),
                                  text_color=COLORS["primary"])
        title_label.pack(pady=(20, 5))
        
        # subtitle_label = ctk.CTkLabel(title_container, 
        #                              text="完整指南，助您快速上手",
        #                              font=ctk.CTkFont(size=10),
        #                              text_color=COLORS["text_secondary"])
        # subtitle_label.pack(pady=(0,0))
        
        # 创建主要内容区域
        content_frame = ctk.CTkFrame(tutorial_frame)
        content_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        # 创建滚动文本框
        tutorial_text = ctk.CTkTextbox(content_frame, 
                                     font=ctk.CTkFont(size=14),
                                     wrap="word",
                                     border_width=0,
                                     fg_color="transparent",
                                     corner_radius=0)
        tutorial_text.pack(fill="both", expand=True)
        
        # 配置文本标签样式 - 美化版本
        tutorial_text.tag_config("title", 
                                foreground=COLORS["primary"], 
                                spacing1=20, spacing3=15,
                                lmargin1=0, lmargin2=0)
        tutorial_text.tag_config("title_underline", 
                                foreground=COLORS["primary"], 
                                spacing1=0, spacing3=15)
        tutorial_text.tag_config("heading", 
                                foreground=COLORS["text_primary"], 
                                spacing1=15, spacing3=10,
                                lmargin1=0, lmargin2=0)
        tutorial_text.tag_config("heading_underline", 
                                foreground=COLORS["accent"], 
                                spacing1=0, spacing3=10)
        tutorial_text.tag_config("subheading", 
                                foreground=COLORS["text_primary"], 
                                spacing1=10, spacing3=8,
                                lmargin1=0, lmargin2=0)
        tutorial_text.tag_config("content", 
                                foreground=COLORS["text_primary"],
                                spacing1=3, spacing3=3,
                                lmargin1=20, lmargin2=20)
        tutorial_text.tag_config("list_item", 
                                foreground=COLORS["text_primary"],
                                spacing1=2, spacing3=2,
                                lmargin1=30, lmargin2=30)
        tutorial_text.tag_config("warning", 
                                foreground=COLORS["warning"],
                                spacing1=10, spacing3=10,
                                lmargin1=15, lmargin2=15,
                                background=COLORS["warning_light"])
        tutorial_text.tag_config("warning_icon", 
                                foreground=COLORS["warning"],
                                spacing1=10, spacing3=0)
        tutorial_text.tag_config("link", 
                                foreground=COLORS["primary"],
                                spacing1=3, spacing3=3,
                                lmargin1=20, lmargin2=20)
        tutorial_text.tag_config("code_inline", 
                                foreground=COLORS["text_primary"], 
                                background=COLORS["secondary"],
                                spacing1=0, spacing3=0)
        tutorial_text.tag_config("code_block", 
                                foreground=COLORS["text_primary"], 
                                background="#2D2D2D",
                                spacing1=10, spacing3=10,
                                lmargin1=20, lmargin2=20)
        tutorial_text.tag_config("code_block_content", 
                                foreground="#F8F8F2", 
                                spacing1=0, spacing3=0,
                                lmargin1=25, lmargin2=25)
        tutorial_text.tag_config("separator", 
                                foreground=COLORS["border"],
                                spacing1=5, spacing3=5)
        
        try:
            # 直接读取Markdown文件
            with open("tutorial.md", "r", encoding="utf-8") as f:
                md_content = f.read()
            
            # 解析Markdown内容并应用美化样式
            lines = md_content.split('\n')
            in_code_block = False
            
            for line in lines:
                if not line.strip():
                    # 空行
                    tutorial_text.insert("end", "\n")
                elif line.startswith("```"):
                    # 代码块开始或结束
                    if not in_code_block:
                        # 代码块开始
                        tutorial_text.insert("end", "▶ 代码块\n", "code_block")
                        in_code_block = True
                    else:
                        # 代码块结束
                        tutorial_text.insert("end", "◀ 代码块结束\n", "code_block")
                        in_code_block = False
                elif in_code_block:
                    # 代码块内容
                    tutorial_text.insert("end", line + "\n", "code_block_content")
                elif line.startswith("# "):
                    # 主标题 - 美化版本
                    tutorial_text.insert("end", "\n", "title")
                    tutorial_text.insert("end", line[2:] + "\n", "title")
                    tutorial_text.insert("end", "═" * 60 + "\n", "title_underline")
                elif line.startswith("## "):
                    # 二级标题 - 美化版本
                    tutorial_text.insert("end", "\n", "heading")
                    tutorial_text.insert("end", "▌ " + line[3:] + "\n", "heading")
                    tutorial_text.insert("end", "─" * 40 + "\n", "heading_underline")
                elif line.startswith("### "):
                    # 三级标题 - 美化版本
                    tutorial_text.insert("end", "\n", "subheading")
                    tutorial_text.insert("end", "▸ " + line[4:] + "\n", "subheading")
                elif line.startswith("> "):
                    # 引用/警告 - 美化版本
                    tutorial_text.insert("end", "\n", "warning_icon")
                    tutorial_text.insert("end", "⚠️  重要提示\n", "warning_icon")
                    tutorial_text.insert("end", line[2:] + "\n", "warning")
                elif line.startswith("- ") or line.startswith("* "):
                    # 无序列表 - 美化版本
                    tutorial_text.insert("end", "• " + line[2:] + "\n", "list_item")
                elif line.startswith("1. ") or line.startswith("2. ") or line.startswith("3. ") or line.startswith("4. ") or line.startswith("5. "):
                    # 有序列表 - 美化版本
                    tutorial_text.insert("end", "  " + line + "\n", "list_item")
                elif "`" in line and not in_code_block:
                    # 包含行内代码的行
                    parts = line.split("`")
                    for i, part in enumerate(parts):
                        if i % 2 == 0:
                            # 普通文本
                            tutorial_text.insert("end", part, "content")
                        else:
                            # 代码
                            tutorial_text.insert("end", "'" + part + "'", "code_inline")
                    tutorial_text.insert("end", "\n", "content")
                elif "[" in line and "](" in line:
                    # 包含链接的行 - 美化版本
                    import re
                    # 简单处理链接文本
                    def replace_link(match):
                        text = match.group(1)
                        url = match.group(2)
                        return f"🔗 {text} (访问: {url})"
                    
                    processed_line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace_link, line)
                    tutorial_text.insert("end", processed_line + "\n", "link")
                else:
                    # 普通内容
                    tutorial_text.insert("end", line + "\n", "content")
            
        except FileNotFoundError:
            # 如果找不到文件，显示错误信息
            tutorial_text.insert("0.0", "教程文件未找到，请确保tutorial.md文件存在于应用程序目录中。")
        except Exception as e:
            # 其他错误
            tutorial_text.insert("0.0", f"读取教程文件时出错: {str(e)}")
        
        # 设置文本框为只读
        tutorial_text.configure(state="disabled")
    
    def _html_to_ctk_text(self, html_content):
        """将HTML内容转换为适合CTkTextbox的文本格式"""
        # 简单的HTML标签处理
        import re
        
        # 移除HTML标签，但保留格式信息
        text = html_content
        
        # 处理标题
        text = re.sub(r'<h1[^>]*>(.*?)</h1>', r'\1\n' + '='*50 + '\n', text)
        text = re.sub(r'<h2[^>]*>(.*?)</h2>', r'\n\1\n' + '-'*30 + '\n', text)
        text = re.sub(r'<h3[^>]*>(.*?)</h3>', r'\n### \1\n', text)
        
        # 处理粗体
        text = re.sub(r'<strong[^>]*>(.*?)</strong>', r'**\1**', text)
        text = re.sub(r'<b[^>]*>(.*?)</b>', r'**\1**', text)
        
        # 处理斜体
        text = re.sub(r'<em[^>]*>(.*?)</em>', r'*\1*', text)
        text = re.sub(r'<i[^>]*>(.*?)</i>', r'*\1*', text)
        
        # 处理代码块
        text = re.sub(r'<pre[^>]*><code[^>]*>(.*?)</code></pre>', 
                     r'\n```\n\1\n```\n', text, flags=re.DOTALL)
        text = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', text)
        
        # 处理引用
        text = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', 
                     r'> \1', text, flags=re.DOTALL)
        
        # 处理链接
        text = re.sub(r'<a[^>]*href="([^"]*)"[^>]*>(.*?)</a>', r'\2 (链接: \1)', text)
        
        # 处理列表
        text = re.sub(r'<ul[^>]*>(.*?)</ul>', r'\1', text, flags=re.DOTALL)
        text = re.sub(r'<ol[^>]*>(.*?)</ol>', r'\1', text, flags=re.DOTALL)
        text = re.sub(r'<li[^>]*>(.*?)</li>', r'• \1\n', text)
        
        # 处理段落
        text = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', text, flags=re.DOTALL)
        
        # 处理换行
        text = re.sub(r'<br[^>]*>', '\n', text)
        
        # 移除剩余的HTML标签
        text = re.sub(r'<[^>]+>', '', text)
        
        # 清理多余的空行
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()
    
    def clear_output(self):
        """清空输出文本框"""
        self.output_text.configure(state="normal")
        self.output_text.delete("0.0", "end")
        self.output_text.configure(state="disabled")
        
        # 显示清空成功状态
        self.task_indicator.set_status("success")
        self.status_var.set("输出已清空")
        # 2秒后恢复原状态
        self.root.after(2000, lambda: self.task_indicator.set_status("ok"))
        self.root.after(2000, lambda: self.status_var.set("就绪"))
    
    def copy_output(self):
        """复制输出内容到剪贴板"""
        try:
            content = self.output_text.get("0.0", "end").strip()
            if content:
                self.root.clipboard_clear()
                self.root.clipboard_append(content)
                # 显示复制成功状态
                self.task_indicator.set_status("success")
                self.status_var.set("输出内容已复制到剪贴板")
                # 2秒后恢复原状态
                self.root.after(2000, lambda: self.task_indicator.set_status("ok"))
                self.root.after(2000, lambda: self.status_var.set("就绪"))
            else:
                self.task_indicator.set_status("warning")
                self.status_var.set("没有内容可复制")
                self.root.after(2000, lambda: self.task_indicator.set_status("ok"))
                self.root.after(2000, lambda: self.status_var.set("就绪"))
        except Exception as e:
            self.task_indicator.set_status("error")
            self.status_var.set(f"复制失败: {str(e)}")
            self.root.after(3000, lambda: self.task_indicator.set_status("ok"))
            self.root.after(3000, lambda: self.status_var.set("就绪"))
    
    def save_output(self):
        """保存输出内容到文件"""
        try:
            content = self.output_text.get("0.0", "end").strip()
            if not content:
                self.task_indicator.set_status("warning")
                self.status_var.set("没有内容可保存")
                self.root.after(2000, lambda: self.task_indicator.set_status("ok"))
                self.root.after(2000, lambda: self.status_var.set("就绪"))
                return
                
            # 打开文件保存对话框
            from tkinter import filedialog
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")],
                title="保存输出内容"
            )
            
            if file_path:  # 用户选择了文件路径
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(content)
                
                # 显示保存成功状态
                self.task_indicator.set_status("success")
                self.status_var.set(f"输出内容已保存到: {os.path.basename(file_path)}")
                # 3秒后恢复原状态
                self.root.after(3000, lambda: self.task_indicator.set_status("ok"))
                self.root.after(3000, lambda: self.status_var.set("就绪"))
        except Exception as e:
            self.task_indicator.set_status("error")
            self.status_var.set(f"保存失败: {str(e)}")
            self.root.after(3000, lambda: self.task_indicator.set_status("ok"))
            self.root.after(3000, lambda: self.status_var.set("就绪"))
    
    def toggle_api_key_visibility(self):
        """切换API密钥可见性"""
        if self.show_api_key.get():
            # 显示密钥
            self.api_key_entry.configure(show="")
        else:
            # 隐藏密钥
            self.api_key_entry.configure(show="*")
    
    def set_example_task(self, example):
        """设置示例任务"""
        self.task_entry.delete("0.0", "end")
        self.task_entry.insert("0.0", example)
    
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
        
        # 设置状态指示器为检查中状态
        self.adb_indicator.set_status("checking", animate=True)
        self.device_indicator.set_status("checking", animate=True)
        
        # 在后台线程中检查ADB状态
        threading.Thread(target=self._check_adb_status_thread, daemon=True).start()
    
    def _check_adb_status_thread(self):
        """在后台线程中检查ADB状态"""
        try:
            # 检查ADB是否安装
            adb_path = "adb"  # 直接使用adb命令，假设已添加到环境变量
            result = subprocess.run([adb_path, "version"], 
                                  capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.root.after(0, lambda: self.adb_status_var.set("✅ 已安装"))
                self.root.after(0, lambda: self.adb_indicator.set_status("ok"))
                
                # 检查设备连接状态
                try:
                    result = subprocess.run([adb_path, "devices"], 
                                          capture_output=True, text=True, timeout=10)
                    lines = result.stdout.strip().split("\n")
                    devices = [line for line in lines[1:] if line.strip() and "\tdevice" in line]
                    
                    if devices:
                        device_ids = [d.split("\t")[0] for d in devices]
                        self.root.after(0, lambda: self.device_status_var.set(f"✅ 已连接 ({len(devices)} 台设备: {', '.join(device_ids)})"))
                        self.root.after(0, lambda: self.device_indicator.set_status("ok"))
                    else:
                        self.root.after(0, lambda: self.device_status_var.set("❌ 未连接设备"))
                        self.root.after(0, lambda: self.device_indicator.set_status("error"))
                except Exception as e:
                    self.root.after(0, lambda: self.device_status_var.set(f"❌ 检查失败: {str(e)}"))
                    self.root.after(0, lambda: self.device_indicator.set_status("error"))
            else:
                self.root.after(0, lambda: self.adb_status_var.set("❌ 未安装"))
                self.root.after(0, lambda: self.adb_indicator.set_status("error"))
                self.root.after(0, lambda: self.device_status_var.set("❌ ADB未安装"))
                self.root.after(0, lambda: self.device_indicator.set_status("error"))
        except FileNotFoundError:
            self.root.after(0, lambda: self.adb_status_var.set("❌ 未找到"))
            self.root.after(0, lambda: self.adb_indicator.set_status("error"))
            self.root.after(0, lambda: self.device_status_var.set("❌ ADB未找到"))
            self.root.after(0, lambda: self.device_indicator.set_status("error"))
        except Exception as e:
            self.root.after(0, lambda: self.adb_status_var.set(f"❌ 检查失败: {str(e)}"))
            self.root.after(0, lambda: self.adb_indicator.set_status("error"))
            self.root.after(0, lambda: self.device_status_var.set("❌ 无法检查"))
            self.root.after(0, lambda: self.device_indicator.set_status("error"))
    
    def execute_task(self):
        """执行任务"""
        task = self.task_entry.get("0.0", "end").strip()
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
        self.execute_btn.configure(state="disabled")
        self.status_var.set("正在执行任务...")
        self.task_indicator.set_status("loading", animate=True)
        self.progress.start()
        
        # 清空输出
        self.output_text.configure(state="normal")
        self.output_text.delete("0.0", "end")
        self.output_text.configure(state="disabled")
        
        # 在后台线程中执行任务
        threading.Thread(target=self._execute_task_thread, args=(task,), daemon=True).start()
    
    def _execute_task_thread(self, task):
        """在后台线程中执行任务"""
        try:
            # 构建命令
            adb_path = "adb"  # 直接使用adb命令，假设已添加到环境变量
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
                self.root.after(0, lambda: self.task_indicator.set_status("success"))
            else:
                self.root.after(0, lambda: self.status_var.set(f"任务执行失败，退出码: {process.returncode}"))
                self.root.after(0, lambda: self.task_indicator.set_status("error"))
                
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"执行错误: {str(e)}"))
            self.root.after(0, lambda: self.task_indicator.set_status("error"))
        finally:
            self.current_process = None
            self.is_running = False
            self.root.after(0, self._task_finished)
    
    def _update_output(self, line):
        """更新输出文本框"""
        # 临时启用编辑模式
        self.output_text.configure(state="normal")
        self.output_text.insert("end", line)
        self.output_text.see("end")
        # 恢复只读模式
        self.output_text.configure(state="disabled")
    
    def _task_finished(self):
        """任务完成后的清理工作"""
        self.execute_btn.configure(state="normal")
        self.progress.stop()
        self.progress.set(0)
    

    
    def on_closing(self):
        """窗口关闭事件处理"""
        # 如果有任务正在执行，询问用户是否确定要关闭
        if self.is_running:
            if messagebox.askokcancel("确认", "任务正在执行中，确定要关闭应用程序吗？"):
                # 尝试停止当前进程
                if self.current_process:
                    try:
                        self.current_process.terminate()
                        self.current_process.wait(timeout=5)
                    except Exception:
                        try:
                            self.current_process.kill()
                        except Exception:
                            pass
            else:
                return
        
        # 关闭窗口
        self.root.destroy()


def main():
    """主函数"""
    app = AutoGLMDesktopApp()
    app.root.mainloop()


if __name__ == "__main__":
    main()