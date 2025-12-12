#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool Macro Tự Động Hái Chè GTV
Thao tác: W -> Space -> Kéo chuột xuống -> Alt -> Click nút "HÁI TRÀ"
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
        'pyautogui': 'pyautogui',
        'keyboard': 'keyboard',
        'mouse': 'mouse'
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

from PIL import Image
import pyautogui
import keyboard
import mouse
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, scrolledtext
except ImportError:
    print("❌ Lỗi: Không tìm thấy tkinter!")
    input("\nNhấn Enter để thoát...")
    sys.exit(1)

pyautogui.FAILSAFE = False


class HaiCheMacro:
    """Lớp quản lý macro hái chè"""
    
    def __init__(self):
        self.playing = False
        self.template_path = None
        self.template_folder = "templates"
        
        # Tạo thư mục templates nếu chưa có
        if not os.path.exists(self.template_folder):
            os.makedirs(self.template_folder)
        
        # Tìm file ảnh template nếu có
        self.load_template()
    
    def load_template(self):
        """Tìm và load template từ file ảnh"""
        # Tìm file ảnh trong thư mục hiện tại
        image_files = [f for f in os.listdir('.') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Tìm file có tên liên quan đến "hai" hoặc "tra" hoặc "che"
        for img_file in image_files:
            name_lower = img_file.lower()
            if 'hai' in name_lower or 'tra' in name_lower or 'che' in name_lower or '7320685051676' in name_lower:
                self.template_path = img_file
                return True
        
        # Nếu không tìm thấy, tìm bất kỳ file ảnh nào
        if image_files:
            self.template_path = image_files[0]
            return True
        
        return False
    
    def capture_template(self):
        """Chụp ảnh nút HÁI TRÀ"""
        try:
            messagebox.showinfo(
                "Chụp ảnh nút HÁI TRÀ",
                "Chuẩn bị chụp ảnh nút 'HÁI TRÀ':\n\n"
                "1. Đảm bảo nút 'HÁI TRÀ' đang hiển thị trên màn hình\n"
                "2. Nhấn OK để bắt đầu\n"
                "3. Bạn có 3 giây để chuẩn bị\n"
                "4. Tool sẽ chụp màn hình, sau đó bạn chọn vùng nút"
            )
            
            time.sleep(3)
            
            # Chụp màn hình
            screenshot = pyautogui.screenshot()
            screenshot_path = f"{self.template_folder}/temp_screenshot.png"
            screenshot.save(screenshot_path)
            
            # Mở cửa sổ chọn vùng
            return self.select_region(screenshot_path)
            
        except Exception as e:
            return False, f"Lỗi: {e}"
    
    def select_region(self, image_path):
        """Chọn vùng nút từ ảnh"""
        try:
            from PIL import ImageTk
            
            root = tk.Tk()
            root.title("Chọn vùng nút HÁI TRÀ")
            
            img = Image.open(image_path)
            img.thumbnail((1200, 800))
            
            photo = ImageTk.PhotoImage(img)
            root.photo = photo  # Giữ reference
            
            canvas = tk.Canvas(root, width=img.width, height=img.height)
            canvas.pack()
            canvas.create_image(0, 0, anchor="nw", image=photo)
            
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
                        outline="red", width=3
                    )
            
            def on_release(event):
                nonlocal end_x, end_y
                end_x, end_y = event.x, event.y
            
            def save_region():
                if start_x is not None and start_y is not None and end_x is not None and end_y is not None:
                    x1, y1 = min(start_x, end_x), min(start_y, end_y)
                    x2, y2 = max(start_x, end_x), max(start_y, end_y)
                    
                    full_img = Image.open(image_path)
                    full_width, full_height = full_img.size
                    display_width, display_height = img.size
                    
                    scale_x = full_width / display_width
                    scale_y = full_height / display_height
                    
                    crop_box = (
                        int(x1 * scale_x),
                        int(y1 * scale_y),
                        int(x2 * scale_x),
                        int(y2 * scale_y)
                    )
                    
                    cropped = full_img.crop(crop_box)
                    template_path = f"{self.template_folder}/nut_hai_tra.png"
                    cropped.save(template_path)
                    
                    self.template_path = template_path
                    root.destroy()
                    return True, "Đã lưu template nút HÁI TRÀ!"
                else:
                    messagebox.showwarning("Cảnh báo", "Chưa chọn vùng!")
                    return False, "Chưa chọn vùng"
            
            canvas.bind("<Button-1>", on_click)
            canvas.bind("<B1-Motion>", on_drag)
            canvas.bind("<ButtonRelease-1>", on_release)
            
            tk.Button(root, text="Lưu vùng này", command=save_region, bg="#4a9eff", fg="white", font=("Arial", 12, "bold"), padx=20, pady=10).pack(pady=10)
            tk.Button(root, text="Hủy", command=root.destroy, bg="#666666", fg="white", padx=15, pady=5).pack()
            
            root.mainloop()
            
            if self.template_path and os.path.exists(self.template_path):
                return True, f"Đã lưu template: {self.template_path}"
            else:
                return False, "Đã hủy"
                
        except Exception as e:
            return False, f"Lỗi: {e}"
    
    def find_and_click_button(self, confidence=0.8, timeout=3):
        """Tìm và click vào nút HÁI TRÀ"""
        if not self.template_path or not os.path.exists(self.template_path):
            return False, "Chưa có template nút HÁI TRÀ!"
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            try:
                location = pyautogui.locateOnScreen(
                    self.template_path,
                    confidence=confidence
                )
                
                if location:
                    center = pyautogui.center(location)
                    pyautogui.click(center.x, center.y)
                    return True, f"Đã click nút HÁI TRÀ tại ({center.x}, {center.y})"
                
                time.sleep(0.1)
                
            except Exception as e:
                error_msg = str(e).lower()
                if "not found" in error_msg or "could not locate" in error_msg:
                    continue
                else:
                    return False, f"Lỗi: {e}"
        
        return False, f"Không tìm thấy nút HÁI TRÀ sau {timeout} giây"
    
    def perform_hai_che_action(self, mouse_down_duration=0.3):
        """Thực hiện thao tác hái chè"""
        try:
            # 1. Nhấn W
            keyboard.press('w')
            time.sleep(0.1)
            keyboard.release('w')
            time.sleep(0.2)
            
            # 2. Nhấn Space
            keyboard.press('space')
            time.sleep(0.1)
            keyboard.release('space')
            time.sleep(0.3)
            
            # 3. Kéo chuột nhìn xuống
            current_x, current_y = pyautogui.position()
            # Nhấn và giữ chuột trái
            pyautogui.mouseDown(button='left')
            time.sleep(mouse_down_duration)
            # Di chuyển chuột xuống (200 pixels)
            pyautogui.moveRel(0, 200, duration=0.2)
            # Thả chuột
            pyautogui.mouseUp(button='left')
            time.sleep(0.3)
            
            # 4. Nhấn Alt
            keyboard.press('alt')
            time.sleep(0.1)
            keyboard.release('alt')
            time.sleep(0.5)  # Đợi menu hiện ra
            
            # 5. Tìm và click nút HÁI TRÀ
            success, message = self.find_and_click_button(confidence=0.8, timeout=3)
            if not success:
                return False, message
            
            time.sleep(0.5)  # Đợi animation
            
            return True, "Đã hoàn thành thao tác hái chè!"
            
        except Exception as e:
            return False, f"Lỗi: {e}"
    
    def play_auto(self, repeat=1, delay_between=1.0, mouse_duration=0.3):
        """Phát tự động nhiều lần"""
        if self.playing:
            return False, "Đang phát rồi!"
        
        self.playing = True
        
        try:
            for i in range(repeat):
                if not self.playing:
                    break
                
                success, message = self.perform_hai_che_action(mouse_duration)
                if not success:
                    self.playing = False
                    return False, message
                
                if i < repeat - 1:
                    time.sleep(delay_between)
            
            self.playing = False
            return True, f"Đã hái chè {repeat} lần!"
            
        except Exception as e:
            self.playing = False
            return False, f"Lỗi: {e}"
    
    def stop_playing(self):
        """Dừng phát"""
        if self.playing:
            self.playing = False
            return True, "Đã dừng!"
        return False, "Không đang phát!"


class HaiCheGUI:
    """Giao diện GUI cho tool hái chè"""
    
    def __init__(self):
        self.macro = HaiCheMacro()
        self.root = tk.Tk()
        self.root.title("Tool Tự Động Hái Chè GTV")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        self.bg_color = "#1e3a5f"
        self.fg_color = "#ffffff"
        self.button_color = "#4a9eff"
        
        self.root.configure(bg=self.bg_color)
        self.setup_ui()
        self.setup_hotkeys()
        self.update_status()
        
    def setup_hotkeys(self):
        """Thiết lập phím tắt"""
        self.root.bind('<Escape>', lambda e: self.emergency_stop())
        self.root.bind('<F9>', lambda e: self.capture_template())
        self.root.bind('<F11>', lambda e: self.start_auto())
        self.root.bind('<F12>', lambda e: self.emergency_stop())
        
        try:
            keyboard.add_hotkey('f11', lambda: self.root.after(0, self.start_auto))
        except:
            pass
    
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Header
        header = tk.Label(
            self.root,
            text="🍃 TOOL TỰ ĐỘNG HÁI CHÈ GTV",
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
        
        self.template_label = tk.Label(
            self.root,
            text="Template: Chưa có",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#cccccc"
        )
        self.template_label.pack()
        
        # Buttons frame
        btn_frame = tk.Frame(self.root, bg=self.bg_color)
        btn_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Capture template button
        tk.Button(
            btn_frame,
            text="📸 Chụp Ảnh Nút HÁI TRÀ (F9)",
            font=("Arial", 12, "bold"),
            bg="#44ff44",
            fg="white",
            padx=20,
            pady=12,
            command=self.capture_template
        ).pack(fill="x", pady=5)
        
        # Test button
        tk.Button(
            btn_frame,
            text="🧪 Test 1 Lần",
            font=("Arial", 11),
            bg=self.button_color,
            fg="white",
            padx=15,
            pady=10,
            command=self.test_once
        ).pack(fill="x", pady=5)
        
        # Auto play section
        auto_frame = tk.LabelFrame(
            btn_frame,
            text="⚙️ Tự Động Hái Chè",
            font=("Arial", 11, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        auto_frame.pack(fill="x", pady=10)
        
        # Số lần lặp
        tk.Label(
            auto_frame,
            text="Số lần hái chè:",
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor="w", padx=10, pady=5)
        
        self.repeat_var = tk.StringVar(value="100")
        tk.Entry(auto_frame, textvariable=self.repeat_var, width=20, font=("Arial", 11)).pack(padx=10, pady=5, fill="x")
        
        # Delay giữa các lần
        tk.Label(
            auto_frame,
            text="Delay giữa các lần (giây):",
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor="w", padx=10, pady=5)
        
        self.delay_var = tk.StringVar(value="1.0")
        tk.Entry(auto_frame, textvariable=self.delay_var, width=20, font=("Arial", 11)).pack(padx=10, pady=5, fill="x")
        
        # Thời gian kéo chuột
        tk.Label(
            auto_frame,
            text="Thời gian kéo chuột (giây):",
            bg=self.bg_color,
            fg=self.fg_color
        ).pack(anchor="w", padx=10, pady=5)
        
        self.mouse_duration_var = tk.StringVar(value="0.3")
        tk.Entry(auto_frame, textvariable=self.mouse_duration_var, width=20, font=("Arial", 11)).pack(padx=10, pady=5, fill="x")
        
        # Auto play button
        self.auto_btn = tk.Button(
            auto_frame,
            text="▶️ Bắt Đầu Tự Động (F11)",
            font=("Arial", 12, "bold"),
            bg="#44ff44",
            fg="white",
            padx=20,
            pady=12,
            command=self.start_auto
        )
        self.auto_btn.pack(fill="x", padx=10, pady=10)
        
        # Stop button
        tk.Button(
            auto_frame,
            text="⏸️ Dừng",
            font=("Arial", 11),
            bg="#ff6666",
            fg="white",
            padx=15,
            pady=8,
            command=self.stop_play
        ).pack(fill="x", padx=10, pady=5)
        
        # Emergency stop
        tk.Button(
            btn_frame,
            text="🛑 TẮT KHẨN CẤP (ESC/F12)",
            font=("Arial", 12, "bold"),
            bg="#ff0000",
            fg="white",
            padx=20,
            pady=12,
            command=self.emergency_stop
        ).pack(fill="x", pady=10)
        
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
            height=5,
            font=("Consolas", 9),
            bg="#0a0a0a",
            fg="#00ff00",
            relief="flat"
        )
        self.log_text.pack(padx=20, pady=(0, 20), fill="both", expand=True)
        self.log("Tool đã sẵn sàng!")
        self.log("💡 F9: Chụp ảnh nút | F11: Tự động | ESC/F12: Tắt khẩn cấp")
        
        # Kiểm tra template
        if self.macro.template_path:
            self.log(f"✅ Đã tìm thấy template: {self.macro.template_path}")
            self.template_label.config(text=f"Template: {os.path.basename(self.macro.template_path)}")
        
    def log(self, msg):
        """Ghi log"""
        self.log_text.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see("end")
        
    def update_status(self):
        """Cập nhật trạng thái"""
        status = "Sẵn sàng"
        color = "#00ff00"
        
        if self.macro.playing:
            status = "▶️ ĐANG HÁI CHÈ"
            color = "#44ff44"
            
        self.status_label.config(text=f"Trạng thái: {status}", fg=color)
        self.root.after(500, self.update_status)
        
    def capture_template(self):
        """Chụp ảnh template"""
        self.log("📸 Bắt đầu chụp ảnh nút HÁI TRÀ...")
        success, msg = self.macro.capture_template()
        
        if success:
            self.log(f"✅ {msg}")
            self.template_label.config(text=f"Template: {os.path.basename(self.macro.template_path)}")
            messagebox.showinfo("Thành công", msg)
        else:
            self.log(f"❌ {msg}")
            messagebox.showerror("Lỗi", msg)
            
    def test_once(self):
        """Test 1 lần"""
        if not self.macro.template_path:
            messagebox.showwarning("Cảnh báo", "Chưa có template nút HÁI TRÀ!\nHãy chụp ảnh nút trước.")
            return
            
        self.log("🧪 Test 1 lần hái chè...")
        try:
            mouse_duration = float(self.mouse_duration_var.get() or "0.3")
        except:
            mouse_duration = 0.3
            
        success, msg = self.macro.perform_hai_che_action(mouse_duration)
        
        if success:
            self.log(f"✅ {msg}")
            messagebox.showinfo("Thành công", msg)
        else:
            self.log(f"❌ {msg}")
            messagebox.showerror("Lỗi", msg)
            
    def start_auto(self):
        """Bắt đầu tự động"""
        if not self.macro.template_path:
            messagebox.showwarning("Cảnh báo", "Chưa có template nút HÁI TRÀ!\nHãy chụp ảnh nút trước (F9).")
            return
            
        try:
            repeat = int(self.repeat_var.get() or "100")
            delay = float(self.delay_var.get() or "1.0")
        except ValueError:
            messagebox.showerror("Lỗi", "Giá trị không hợp lệ!")
            return
            
        self.auto_btn.config(state="disabled")
        self.log(f"▶️ Bắt đầu tự động hái chè ({repeat} lần)")
        
        def play_thread():
            try:
                mouse_duration = float(self.mouse_duration_var.get() or "0.3")
            except:
                mouse_duration = 0.3
                
            success, msg = self.macro.play_auto(repeat=repeat, delay_between=delay, mouse_duration=mouse_duration)
            self.root.after(0, lambda: self.auto_btn.config(state="normal"))
            
            if success:
                self.log(f"✅ {msg}")
                messagebox.showinfo("Thành công", msg)
            else:
                self.log(f"❌ {msg}")
                messagebox.showerror("Lỗi", msg)
                
        threading.Thread(target=play_thread, daemon=True).start()
        
    def stop_play(self):
        """Dừng phát"""
        self.macro.stop_playing()
        self.auto_btn.config(state="normal")
        self.log("⏸️ Đã dừng")
        
    def emergency_stop(self):
        """Tắt khẩn cấp"""
        self.macro.stop_playing()
        self.auto_btn.config(state="normal")
        self.log("🛑 TẮT KHẨN CẤP!")
        messagebox.showwarning("Tắt khẩn cấp", "Đã dừng tất cả!")
        
    def run(self):
        """Chạy ứng dụng"""
        try:
            self.root.mainloop()
        finally:
            try:
                keyboard.unhook_all()
            except:
                pass


def main():
    """Hàm chính"""
    try:
        app = HaiCheGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

