#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool Macro với Nhận Diện Hình Ảnh
Tự động tìm và click vào các nút dựa trên ảnh mẫu
"""

import os
import sys
import time
import json
import subprocess
import threading
from datetime import datetime

# Tự động cài đặt thư viện
def install_requirements():
    """Tự động cài đặt các thư viện cần thiết"""
    required_packages = {
        'PIL': 'Pillow',
        'cv2': 'opencv-python',
        'numpy': 'numpy',
        'pyautogui': 'pyautogui'
    }
    missing_packages = []
    
    for module, package in required_packages.items():
        try:
            if module == 'PIL':
                __import__('PIL')
            elif module == 'cv2':
                __import__('cv2')
            else:
                __import__(module)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("=" * 60)
        print("ĐANG CÀI ĐẶT THƯ VIỆN CẦN THIẾT...")
        print("=" * 60)
        print(f"Cần cài đặt: {', '.join(missing_packages)}")
        print("Vui lòng đợi...")
        print("-" * 60)
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package, "--quiet"])
                print(f"✅ Đã cài đặt: {package}")
            except Exception as e:
                print(f"❌ Lỗi khi cài {package}: {e}")
                print("\nVui lòng chạy với quyền Administrator!")
                input("\nNhấn Enter để thoát...")
                sys.exit(1)
        
        print("-" * 60)
        print("✅ Đã cài đặt xong!")
        time.sleep(1)

install_requirements()

from PIL import Image, ImageGrab
import cv2
import numpy as np
import pyautogui
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, scrolledtext
except ImportError:
    print("❌ Lỗi: Không tìm thấy tkinter!")
    input("\nNhấn Enter để thoát...")
    sys.exit(1)

# Tắt fail-safe của pyautogui (để tránh dừng khi di chuột ra góc)
pyautogui.FAILSAFE = False


class ImageMacro:
    """Lớp quản lý macro với nhận diện hình ảnh"""
    
    def __init__(self):
        self.templates = {}  # Lưu các ảnh mẫu
        self.actions = []  # Lưu chuỗi hành động
        self.playing = False
        self.template_folder = "templates"  # Thư mục chứa ảnh mẫu
        
        # Tạo thư mục templates nếu chưa có
        if not os.path.exists(self.template_folder):
            os.makedirs(self.template_folder)
    
    def capture_template(self, name):
        """Chụp ảnh màn hình và lưu làm template"""
        try:
            # Hiển thị hướng dẫn
            messagebox.showinfo(
                "Chụp ảnh mẫu",
                f"Chuẩn bị chụp ảnh cho: {name}\n\n"
                "1. Đảm bảo nút/bộ phận cần chụp đang hiển thị trên màn hình\n"
                "2. Nhấn OK để bắt đầu\n"
                "3. Bạn có 3 giây để chuẩn bị\n"
                "4. Tool sẽ chụp toàn màn hình, sau đó bạn chọn vùng cần lưu"
            )
            
            time.sleep(3)
            
            # Chụp toàn màn hình
            screenshot = pyautogui.screenshot()
            screenshot_path = f"{self.template_folder}/temp_screenshot.png"
            screenshot.save(screenshot_path)
            
            # Mở cửa sổ để chọn vùng
            return self.select_region(screenshot_path, name)
            
        except Exception as e:
            return False, f"Lỗi: {e}"
    
    def select_region(self, image_path, name):
        """Chọn vùng từ ảnh để lưu làm template"""
        try:
            from PIL import Image, ImageTk
            
            # Tạo cửa sổ chọn vùng
            root = tk.Tk()
            root.title(f"Chọn vùng cho: {name}")
            
            # Load ảnh
            img = Image.open(image_path)
            img.thumbnail((1200, 800))  # Resize để vừa màn hình
            
            photo = ImageTk.PhotoImage(img)
            
            canvas = tk.Canvas(root, width=img.width, height=img.height)
            canvas.pack()
            canvas.create_image(0, 0, anchor="nw", image=photo)
            
            # Biến để lưu vùng chọn
            start_x = start_y = end_x = end_y = None
            rect_id = None
            
            def on_click(event):
                nonlocal start_x, start_y, rect_id
                start_x, start_y = event.x, event.y
                if rect_id:
                    canvas.delete(rect_id)
            
            def on_drag(event):
                nonlocal end_x, end_y, rect_id
                end_x, end_y = event.x, event.y
                if rect_id:
                    canvas.delete(rect_id)
                if start_x and start_y:
                    rect_id = canvas.create_rectangle(
                        start_x, start_y, end_x, end_y,
                        outline="red", width=2
                    )
            
            def on_release(event):
                nonlocal end_x, end_y
                end_x, end_y = event.x, event.y
            
            def save_region():
                if start_x is not None and start_y is not None and end_x is not None and end_y is not None:
                    # Tính toán vùng chọn
                    x1, y1 = min(start_x, end_x), min(start_y, end_y)
                    x2, y2 = max(start_x, end_x), max(start_y, end_y)
                    
                    # Load ảnh gốc (full size)
                    full_img = Image.open(image_path)
                    full_width, full_height = full_img.size
                    
                    # Tính scale (ảnh đã được resize trong canvas)
                    display_width, display_height = img.size
                    scale_x = full_width / display_width
                    scale_y = full_height / display_height
                    
                    # Tính vùng crop trên ảnh gốc
                    crop_box = (
                        int(x1 * scale_x),
                        int(y1 * scale_y),
                        int(x2 * scale_x),
                        int(y2 * scale_y)
                    )
                    
                    cropped = full_img.crop(crop_box)
                    template_path = f"{self.template_folder}/{name}.png"
                    cropped.save(template_path)
                    
                    self.templates[name] = template_path
                    root.destroy()
                    return True, f"Đã lưu template: {name}"
                else:
                    messagebox.showwarning("Cảnh báo", "Chưa chọn vùng!")
                    return False, "Chưa chọn vùng"
            
            canvas.bind("<Button-1>", on_click)
            canvas.bind("<B1-Motion>", on_drag)
            canvas.bind("<ButtonRelease-1>", on_release)
            
            tk.Button(root, text="Lưu vùng này", command=save_region, bg="#4a9eff", fg="white").pack(pady=10)
            tk.Button(root, text="Hủy", command=root.destroy, bg="#666666", fg="white").pack()
            
            # Lưu reference để tránh garbage collection
            root.photo = photo
            
            root.mainloop()
            
            # Kiểm tra kết quả
            if name in self.templates:
                return True, f"Đã lưu template: {name}"
            else:
                return False, "Đã hủy"
                
        except Exception as e:
            return False, f"Lỗi: {e}"
    
    def find_and_click(self, template_name, confidence=0.8, timeout=5):
        """Tìm và click vào template"""
        if template_name not in self.templates:
            return False, f"Không tìm thấy template: {template_name}"
        
        template_path = self.templates[template_name]
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                # Tìm kiếm trên màn hình
                location = pyautogui.locateOnScreen(
                    template_path,
                    confidence=confidence
                )
                
                if location:
                    # Click vào center của vùng tìm thấy
                    center = pyautogui.center(location)
                    pyautogui.click(center.x, center.y)
                    return True, f"Đã click vào {template_name} tại ({center.x}, {center.y})"
                
                time.sleep(0.1)  # Đợi một chút trước khi tìm lại
                
            except Exception as e:
                # Kiểm tra nếu là lỗi không tìm thấy ảnh (tiếp tục tìm)
                error_msg = str(e).lower()
                if "not found" in error_msg or "could not locate" in error_msg:
                    continue
                else:
                    # Lỗi khác, trả về
                    return False, f"Lỗi: {e}"
        
        return False, f"Không tìm thấy {template_name} sau {timeout} giây"
    
    def add_action(self, template_name, delay=1.0, confidence=0.8, timeout=5):
        """Thêm hành động vào danh sách"""
        self.actions.append({
            'type': 'click_template',
            'template': template_name,
            'delay': delay,
            'confidence': confidence,
            'timeout': timeout
        })
    
    def play_actions(self, repeat=1):
        """Phát lại các hành động"""
        if not self.actions:
            return False, "Không có hành động nào!"
        
        self.playing = True
        
        try:
            for iteration in range(repeat):
                if not self.playing:
                    break
                
                for action in self.actions:
                    if not self.playing:
                        break
                    
                    if action['type'] == 'click_template':
                        success, message = self.find_and_click(
                            action['template'],
                            action['confidence'],
                            action['timeout']
                        )
                        if not success:
                            return False, message
                        
                        time.sleep(action['delay'])
            
            self.playing = False
            return True, f"Đã phát xong ({repeat} lần)!"
            
        except Exception as e:
            self.playing = False
            return False, f"Lỗi: {e}"
    
    def stop_playing(self):
        """Dừng phát"""
        self.playing = False
        return True, "Đã dừng!"
    
    def save_config(self, filename):
        """Lưu cấu hình"""
        config = {
            'templates': self.templates,
            'actions': self.actions,
            'created': datetime.now().isoformat()
        }
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True, f"Đã lưu vào {filename}"
        except Exception as e:
            return False, f"Lỗi: {e}"
    
    def load_config(self, filename):
        """Tải cấu hình"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.templates = config.get('templates', {})
                self.actions = config.get('actions', [])
            return True, f"Đã tải từ {filename}"
        except Exception as e:
            return False, f"Lỗi: {e}"


class ImageMacroGUI:
    """Giao diện GUI cho tool nhận diện hình ảnh"""
    
    def __init__(self):
        self.macro = ImageMacro()
        self.root = tk.Tk()
        self.root.title("Tool Macro Nhận Diện Hình Ảnh - Hái Chè GTV")
        self.root.geometry("700x750")
        self.root.resizable(False, False)
        
        self.bg_color = "#1e3a5f"
        self.fg_color = "#ffffff"
        self.button_color = "#4a9eff"
        
        self.root.configure(bg=self.bg_color)
        self.setup_ui()
        self.update_status()
        
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Header
        header = tk.Label(
            self.root,
            text="🖼️ TOOL MACRO NHẬN DIỆN HÌNH ẢNH",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg="#ffd700"
        )
        header.pack(pady=15)
        
        # Status
        self.status_label = tk.Label(
            self.root,
            text="Trạng thái: Sẵn sàng",
            font=("Arial", 11),
            bg=self.bg_color,
            fg="#00ff00"
        )
        self.status_label.pack(pady=5)
        
        # Notebook (tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Tab 1: Quản lý Templates
        template_frame = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(template_frame, text="📸 Templates")
        self.setup_template_tab(template_frame)
        
        # Tab 2: Tạo Hành Động
        action_frame = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(action_frame, text="⚙️ Hành Động")
        self.setup_action_tab(action_frame)
        
        # Tab 3: Chạy Macro
        play_frame = tk.Frame(notebook, bg=self.bg_color)
        notebook.add(play_frame, text="▶️ Chạy Macro")
        self.setup_play_tab(play_frame)
        
        # Log
        log_label = tk.Label(
            self.root,
            text="Nhật ký:",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color,
            anchor="w"
        )
        log_label.pack(pady=(10, 5), padx=20, anchor="w")
        
        self.log_text = scrolledtext.ScrolledText(
            self.root,
            height=6,
            font=("Consolas", 9),
            bg="#0a0a0a",
            fg="#00ff00",
            relief="flat"
        )
        self.log_text.pack(padx=20, pady=(0, 20), fill="both", expand=True)
        self.log("Tool đã sẵn sàng!")
        
    def setup_template_tab(self, parent):
        """Thiết lập tab Templates"""
        tk.Label(
            parent,
            text="Quản lý Ảnh Mẫu (Templates)",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(pady=10)
        
        # Frame chứa danh sách templates
        list_frame = tk.Frame(parent, bg=self.bg_color)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(
            list_frame,
            text="Danh sách Templates:",
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor="w")
        
        self.template_listbox = tk.Listbox(
            list_frame,
            height=8,
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Arial", 10)
        )
        self.template_listbox.pack(fill="both", expand=True, pady=5)
        
        # Buttons
        btn_frame = tk.Frame(list_frame, bg=self.bg_color)
        btn_frame.pack(fill="x", pady=5)
        
        tk.Button(
            btn_frame,
            text="➕ Chụp Template Mới",
            font=("Arial", 11),
            bg="#44ff44",
            fg="white",
            padx=15,
            pady=8,
            command=self.capture_template
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        tk.Button(
            btn_frame,
            text="🗑️ Xóa",
            font=("Arial", 11),
            bg="#ff6666",
            fg="white",
            padx=15,
            pady=8,
            command=self.delete_template
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        # Input để đặt tên template
        input_frame = tk.Frame(parent, bg=self.bg_color)
        input_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(
            input_frame,
            text="Tên template:",
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(side="left", padx=5)
        
        self.template_name_var = tk.StringVar()
        tk.Entry(
            input_frame,
            textvariable=self.template_name_var,
            width=30,
            font=("Arial", 10)
        ).pack(side="left", padx=5, fill="x", expand=True)
        
    def setup_action_tab(self, parent):
        """Thiết lập tab Hành Động"""
        tk.Label(
            parent,
            text="Tạo Chuỗi Hành Động",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(pady=10)
        
        # Danh sách hành động
        list_frame = tk.Frame(parent, bg=self.bg_color)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(
            list_frame,
            text="Chuỗi hành động:",
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor="w")
        
        self.action_listbox = tk.Listbox(
            list_frame,
            height=10,
            bg="#2b2b2b",
            fg="#ffffff",
            font=("Arial", 10)
        )
        self.action_listbox.pack(fill="both", expand=True, pady=5)
        
        # Form thêm hành động
        form_frame = tk.LabelFrame(
            parent,
            text="Thêm Hành Động",
            font=("Arial", 10, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        form_frame.pack(pady=10, padx=20, fill="x")
        
        # Template
        tk.Label(form_frame, text="Template:", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.action_template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(form_frame, textvariable=self.action_template_var, width=25)
        self.template_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        form_frame.columnconfigure(1, weight=1)
        
        # Delay
        tk.Label(form_frame, text="Delay (giây):", bg=self.bg_color, fg=self.fg_color).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.action_delay_var = tk.StringVar(value="1.0")
        tk.Entry(form_frame, textvariable=self.action_delay_var, width=25).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Confidence
        tk.Label(form_frame, text="Độ chính xác (0.7-0.9):", bg=self.bg_color, fg=self.fg_color).grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.action_confidence_var = tk.StringVar(value="0.8")
        tk.Entry(form_frame, textvariable=self.action_confidence_var, width=25).grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        
        # Buttons
        btn_frame = tk.Frame(form_frame, bg=self.bg_color)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        tk.Button(
            btn_frame,
            text="➕ Thêm Hành Động",
            font=("Arial", 10),
            bg=self.button_color,
            fg="white",
            padx=15,
            pady=5,
            command=self.add_action
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="🗑️ Xóa Hành Động",
            font=("Arial", 10),
            bg="#ff6666",
            fg="white",
            padx=15,
            pady=5,
            command=self.remove_action
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame,
            text="🗑️ Xóa Tất Cả",
            font=("Arial", 10),
            bg="#cc0000",
            fg="white",
            padx=15,
            pady=5,
            command=self.clear_actions
        ).pack(side="left", padx=5)
        
        # Cập nhật danh sách templates khi thay đổi
        self.update_template_list()
        self.update_template_combo()
        
    def setup_play_tab(self, parent):
        """Thiết lập tab Chạy Macro"""
        tk.Label(
            parent,
            text="Chạy Macro Tự Động",
            font=("Arial", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(pady=10)
        
        # Settings
        settings_frame = tk.LabelFrame(
            parent,
            text="Cài Đặt",
            font=("Arial", 10, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        settings_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(settings_frame, text="Số lần lặp:", bg=self.bg_color, fg=self.fg_color).grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.repeat_var = tk.StringVar(value="100")
        tk.Entry(settings_frame, textvariable=self.repeat_var, width=20).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        settings_frame.columnconfigure(1, weight=1)
        
        tk.Label(settings_frame, text="Delay giữa các lần (giây):", bg=self.bg_color, fg=self.fg_color).grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.play_delay_var = tk.StringVar(value="0.5")
        tk.Entry(settings_frame, textvariable=self.play_delay_var, width=20).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Buttons
        btn_frame = tk.Frame(parent, bg=self.bg_color)
        btn_frame.pack(pady=20, padx=20, fill="x")
        
        self.play_btn = tk.Button(
            btn_frame,
            text="▶️ Bắt Đầu Tự Động",
            font=("Arial", 14, "bold"),
            bg="#44ff44",
            fg="white",
            padx=30,
            pady=15,
            command=self.start_auto_play
        )
        self.play_btn.pack(fill="x", pady=5)
        
        tk.Button(
            btn_frame,
            text="⏸️ Dừng",
            font=("Arial", 12, "bold"),
            bg="#ff6666",
            fg="white",
            padx=20,
            pady=10,
            command=self.stop_play
        ).pack(fill="x", pady=5)
        
        tk.Button(
            btn_frame,
            text="🛑 TẮT KHẨN CẤP",
            font=("Arial", 12, "bold"),
            bg="#ff0000",
            fg="white",
            padx=20,
            pady=10,
            command=self.emergency_stop
        ).pack(fill="x", pady=5)
        
        # File operations
        file_frame = tk.Frame(parent, bg=self.bg_color)
        file_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Button(
            file_frame,
            text="💾 Lưu Cấu Hình",
            font=("Arial", 10),
            bg=self.button_color,
            fg="white",
            padx=15,
            pady=8,
            command=self.save_config
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        tk.Button(
            file_frame,
            text="📂 Tải Cấu Hình",
            font=("Arial", 10),
            bg=self.button_color,
            fg="white",
            padx=15,
            pady=8,
            command=self.load_config
        ).pack(side="left", padx=5, fill="x", expand=True)
        
    def log(self, msg):
        """Ghi log"""
        self.log_text.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see("end")
        
    def update_status(self):
        """Cập nhật trạng thái"""
        status = "Sẵn sàng"
        color = "#00ff00"
        
        if self.macro.playing:
            status = "▶️ ĐANG CHẠY"
            color = "#44ff44"
            
        self.status_label.config(text=f"Trạng thái: {status}", fg=color)
        self.root.after(500, self.update_status)
        
    def update_template_list(self):
        """Cập nhật danh sách templates"""
        self.template_listbox.delete(0, tk.END)
        for name in self.macro.templates.keys():
            self.template_listbox.insert(tk.END, name)
            
    def update_template_combo(self):
        """Cập nhật combo box templates"""
        if hasattr(self, 'template_combo'):
            self.template_combo['values'] = list(self.macro.templates.keys())
                                    
    def capture_template(self):
        """Chụp template mới"""
        name = self.template_name_var.get().strip()
        if not name:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập tên template!")
            return
            
        if name in self.macro.templates:
            if not messagebox.askyesno("Xác nhận", f"Template '{name}' đã tồn tại. Ghi đè?"):
                return
        
        self.log(f"📸 Đang chụp template: {name}")
        success, msg = self.macro.capture_template(name)
        
        if success:
            self.log(f"✅ {msg}")
            self.update_template_list()
            self.update_template_combo()
            messagebox.showinfo("Thành công", msg)
        else:
            self.log(f"❌ {msg}")
            messagebox.showerror("Lỗi", msg)
            
    def delete_template(self):
        """Xóa template"""
        selection = self.template_listbox.curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Chọn template để xóa!")
            return
            
        name = self.template_listbox.get(selection[0])
        if messagebox.askyesno("Xác nhận", f"Xóa template '{name}'?"):
            if name in self.macro.templates:
                try:
                    os.remove(self.macro.templates[name])
                    del self.macro.templates[name]
                    self.log(f"🗑️ Đã xóa template: {name}")
                    self.update_template_list()
                    self.update_template_combo()
                except Exception as e:
                    self.log(f"❌ Lỗi: {e}")
                    
    def add_action(self):
        """Thêm hành động"""
        template = self.action_template_var.get()
        if not template or template not in self.macro.templates:
            messagebox.showwarning("Cảnh báo", "Chọn template hợp lệ!")
            return
            
        try:
            delay = float(self.action_delay_var.get() or "1.0")
            confidence = float(self.action_confidence_var.get() or "0.8")
        except ValueError:
            messagebox.showerror("Lỗi", "Giá trị không hợp lệ!")
            return
            
        self.macro.add_action(template, delay, confidence)
        self.log(f"➕ Đã thêm: Click {template} (delay: {delay}s)")
        self.update_action_list()
        
    def remove_action(self):
        """Xóa hành động"""
        selection = self.action_listbox.curselection()
        if not selection:
            messagebox.showwarning("Cảnh báo", "Chọn hành động để xóa!")
            return
            
        index = selection[0]
        self.macro.actions.pop(index)
        self.log(f"🗑️ Đã xóa hành động #{index + 1}")
        self.update_action_list()
        
    def clear_actions(self):
        """Xóa tất cả hành động"""
        if messagebox.askyesno("Xác nhận", "Xóa tất cả hành động?"):
            self.macro.actions = []
            self.log("🗑️ Đã xóa tất cả hành động")
            self.update_action_list()
            
    def update_action_list(self):
        """Cập nhật danh sách hành động"""
        self.action_listbox.delete(0, tk.END)
        for i, action in enumerate(self.macro.actions, 1):
            if action['type'] == 'click_template':
                self.action_listbox.insert(
                    tk.END,
                    f"{i}. Click '{action['template']}' (delay: {action['delay']}s)"
                )
                
    def start_auto_play(self):
        """Bắt đầu tự động phát"""
        if not self.macro.actions:
            messagebox.showwarning("Cảnh báo", "Chưa có hành động nào!")
            return
            
        try:
            repeat = int(self.repeat_var.get() or "100")
            play_delay = float(self.play_delay_var.get() or "0.5")
        except ValueError:
            messagebox.showerror("Lỗi", "Giá trị không hợp lệ!")
            return
            
        self.play_btn.config(state="disabled")
        self.log(f"▶️ Bắt đầu tự động phát ({repeat} lần)")
        
        def play_thread():
            for i in range(repeat):
                if not self.macro.playing:
                    break
                    
                success, msg = self.macro.play_actions(repeat=1)
                if not success:
                    self.log(f"❌ {msg}")
                    break
                    
                if i < repeat - 1:
                    time.sleep(play_delay)
                    
            self.root.after(0, lambda: self.play_btn.config(state="normal"))
            self.log(f"✅ Hoàn thành!")
            
        threading.Thread(target=play_thread, daemon=True).start()
        
    def stop_play(self):
        """Dừng phát"""
        self.macro.stop_playing()
        self.play_btn.config(state="normal")
        self.log("⏸️ Đã dừng")
        
    def emergency_stop(self):
        """Tắt khẩn cấp"""
        self.macro.stop_playing()
        self.play_btn.config(state="normal")
        self.log("🛑 TẮT KHẨN CẤP!")
        messagebox.showwarning("Tắt khẩn cấp", "Đã dừng tất cả!")
        
    def save_config(self):
        """Lưu cấu hình"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON", "*.json")]
        )
        if filename:
            success, msg = self.macro.save_config(filename)
            if success:
                self.log(f"✅ {msg}")
                messagebox.showinfo("Thành công", msg)
            else:
                self.log(f"❌ {msg}")
                
    def load_config(self):
        """Tải cấu hình"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON", "*.json")]
        )
        if filename:
            success, msg = self.macro.load_config(filename)
            if success:
                self.log(f"✅ {msg}")
                self.update_template_list()
                self.update_template_combo()
                self.update_action_list()
                messagebox.showinfo("Thành công", msg)
            else:
                self.log(f"❌ {msg}")
                
    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()


def main():
    """Hàm chính"""
    try:
        app = ImageMacroGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

