#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chương trình Macro cho Windows - Giao diện GUI
Tự động cài đặt thư viện và chạy với menu đồ họa
"""

import os
import sys
import time
import json
import subprocess
import threading
from datetime import datetime

# Tự động cài đặt thư viện nếu chưa có
def install_requirements():
    """Tự động cài đặt các thư viện cần thiết"""
    required_packages = {
        'keyboard': 'keyboard',
        'mouse': 'mouse',
        'tkinter': None  # tkinter có sẵn trong Python
    }
    missing_packages = []
    
    # Kiểm tra keyboard và mouse
    for package, pip_name in required_packages.items():
        if pip_name:  # Chỉ kiểm tra packages cần cài từ pip
            try:
                __import__(package)
            except ImportError:
                missing_packages.append(pip_name)
    
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
        print("✅ Đã cài đặt xong tất cả thư viện!")
        print("Đang khởi động chương trình...")
        time.sleep(1)

# Cài đặt thư viện trước khi import
install_requirements()

# Import sau khi đã cài đặt
import keyboard
import mouse
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, scrolledtext
except ImportError:
    print("❌ Lỗi: Không tìm thấy tkinter!")
    print("Vui lòng cài lại Python và chọn 'tcl/tk' trong options.")
    input("\nNhấn Enter để thoát...")
    sys.exit(1)


class MacroRecorder:
    """Lớp quản lý ghi và phát macro"""
    
    def __init__(self):
        self.recording = False
        self.events = []
        self.start_time = None
        self.playing = False
        self.current_macro_file = None
        
    def start_recording(self):
        """Bắt đầu ghi macro"""
        if self.recording:
            return False, "Đang ghi rồi!"
            
        self.recording = True
        self.events = []
        self.start_time = time.time()
        
        keyboard.hook(self._on_keyboard_event)
        mouse.hook(self._on_mouse_event)
        
        return True, "Đã bắt đầu ghi macro!"
        
    def stop_recording(self):
        """Dừng ghi macro"""
        if not self.recording:
            return False, "Không đang ghi!"
            
        self.recording = False
        keyboard.unhook_all()
        mouse.unhook_all()
        event_count = len(self.events)
        return True, f"Đã dừng ghi. Tổng cộng {event_count} sự kiện."
        
    def _on_keyboard_event(self, event):
        """Xử lý sự kiện bàn phím"""
        if not self.recording:
            return
            
        if event.event_type in ['down', 'up']:
            delay = time.time() - self.start_time
            self.events.append({
                'type': 'keyboard',
                'event': event.event_type,
                'key': event.name,
                'time': delay
            })
    
    def _on_mouse_event(self, event):
        """Xử lý sự kiện chuột"""
        if not self.recording:
            return
            
        delay = time.time() - self.start_time
        
        if isinstance(event, mouse.ButtonEvent):
            self.events.append({
                'type': 'mouse_button',
                'event': event.event_type,
                'button': event.button,
                'time': delay
            })
        elif isinstance(event, mouse.MoveEvent):
            self.events.append({
                'type': 'mouse_move',
                'x': event.x,
                'y': event.y,
                'time': delay
            })
        elif isinstance(event, mouse.WheelEvent):
            self.events.append({
                'type': 'mouse_wheel',
                'delta': event.delta,
                'time': delay
            })
    
    def save_macro(self, filename):
        """Lưu macro vào file"""
        if not self.events:
            return False, "Không có sự kiện nào để lưu!"
            
        try:
            if not filename.endswith('.json'):
                filename += '.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'events': self.events,
                    'created': datetime.now().isoformat(),
                    'event_count': len(self.events)
                }, f, indent=2, ensure_ascii=False)
            self.current_macro_file = filename
            return True, f"Đã lưu macro vào {filename}"
        except Exception as e:
            return False, f"Lỗi khi lưu: {e}"
    
    def load_macro(self, filename):
        """Tải macro từ file"""
        try:
            if not filename.endswith('.json'):
                filename += '.json'
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, dict) and 'events' in data:
                    self.events = data['events']
                else:
                    self.events = data
            self.current_macro_file = filename
            return True, f"Đã tải macro từ {filename} ({len(self.events)} sự kiện)"
        except FileNotFoundError:
            return False, f"Không tìm thấy file {filename}!"
        except Exception as e:
            return False, f"Lỗi khi tải: {e}"
    
    def play_macro(self, repeat=1, speed=1.0):
        """Phát lại macro"""
        if not self.events:
            return False, "Không có macro để phát!"
            
        if self.playing:
            return False, "Đang phát macro rồi!"
        
        self.playing = True
        
        try:
            for iteration in range(repeat):
                if not self.playing:
                    break
                    
                last_time = 0
                
                for event in self.events:
                    if not self.playing:
                        break
                        
                    delay = (event['time'] - last_time) / speed
                    if delay > 0:
                        time.sleep(delay)
                    
                    last_time = event['time']
                    
                    if event['type'] == 'keyboard':
                        if event['event'] == 'down':
                            keyboard.press(event['key'])
                        elif event['event'] == 'up':
                            keyboard.release(event['key'])
                            
                    elif event['type'] == 'mouse_button':
                        if event['event'] == 'down':
                            mouse.press(event['button'])
                        elif event['event'] == 'up':
                            mouse.release(event['button'])
                            
                    elif event['type'] == 'mouse_move':
                        mouse.move(event['x'], event['y'])
                        
                    elif event['type'] == 'mouse_wheel':
                        mouse.wheel(event['delta'])
            
            self.playing = False
            return True, f"Đã phát xong macro ({repeat} lần)!"
        except Exception as e:
            self.playing = False
            return False, f"Lỗi khi phát: {e}"
    
    def stop_playing(self):
        """Dừng phát macro"""
        if self.playing:
            self.playing = False
            return True, "Đã dừng phát macro"
        return False, "Không đang phát macro"


class MacroGUI:
    """Giao diện GUI cho chương trình Macro"""
    
    def __init__(self):
        self.recorder = MacroRecorder()
        self.root = tk.Tk()
        self.root.title("Chương trình Macro cho Windows")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Màu sắc
        self.bg_color = "#2b2b2b"
        self.fg_color = "#ffffff"
        self.button_color = "#4a9eff"
        self.button_hover = "#357abd"
        self.record_color = "#ff4444"
        self.play_color = "#44ff44"
        
        self.root.configure(bg=self.bg_color)
        self.setup_ui()
        self.setup_hotkeys()
        self.update_status()
        
    def setup_hotkeys(self):
        """Thiết lập phím tắt"""
        # Phím ESC để tắt khẩn cấp
        self.root.bind('<Escape>', lambda e: self.emergency_stop())
        # Phím F12 để tắt khẩn cấp
        self.root.bind('<F12>', lambda e: self.emergency_stop())
        
    def setup_ui(self):
        """Thiết lập giao diện"""
        # Header
        header = tk.Label(
            self.root,
            text="🎯 CHƯƠNG TRÌNH MACRO CHO WINDOWS",
            font=("Arial", 16, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        header.pack(pady=20)
        
        # Status frame
        status_frame = tk.Frame(self.root, bg=self.bg_color)
        status_frame.pack(pady=10)
        
        self.status_label = tk.Label(
            status_frame,
            text="Trạng thái: Sẵn sàng",
            font=("Arial", 11),
            bg=self.bg_color,
            fg="#00ff00"
        )
        self.status_label.pack()
        
        self.info_label = tk.Label(
            status_frame,
            text="Sự kiện: 0 | File: Chưa có",
            font=("Arial", 10),
            bg=self.bg_color,
            fg="#cccccc"
        )
        self.info_label.pack()
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Row 1: Record buttons
        record_frame = tk.Frame(buttons_frame, bg=self.bg_color)
        record_frame.pack(fill="x", pady=5)
        
        self.record_btn = tk.Button(
            record_frame,
            text="📹 Ghi Macro",
            font=("Arial", 12, "bold"),
            bg=self.record_color,
            fg="white",
            activebackground="#cc0000",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.toggle_record
        )
        self.record_btn.pack(side="left", padx=5, fill="x", expand=True)
        
        self.stop_record_btn = tk.Button(
            record_frame,
            text="⏹️ Dừng Ghi",
            font=("Arial", 12, "bold"),
            bg="#666666",
            fg="white",
            activebackground="#555555",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.stop_record
        )
        self.stop_record_btn.pack(side="left", padx=5, fill="x", expand=True)
        
        # Row 2: Play buttons
        play_frame = tk.Frame(buttons_frame, bg=self.bg_color)
        play_frame.pack(fill="x", pady=5)
        
        self.play_btn = tk.Button(
            play_frame,
            text="▶️ Phát Macro",
            font=("Arial", 12, "bold"),
            bg=self.play_color,
            fg="white",
            activebackground="#00cc00",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.play_macro
        )
        self.play_btn.pack(side="left", padx=5, fill="x", expand=True)
        
        self.stop_play_btn = tk.Button(
            play_frame,
            text="⏸️ Dừng Phát",
            font=("Arial", 12, "bold"),
            bg="#666666",
            fg="white",
            activebackground="#555555",
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.stop_play
        )
        self.stop_play_btn.pack(side="left", padx=5, fill="x", expand=True)
        
        # Row 3: File operations
        file_frame = tk.Frame(buttons_frame, bg=self.bg_color)
        file_frame.pack(fill="x", pady=5)
        
        tk.Button(
            file_frame,
            text="💾 Lưu Macro",
            font=("Arial", 11),
            bg=self.button_color,
            fg="white",
            activebackground=self.button_hover,
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.save_macro
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        tk.Button(
            file_frame,
            text="📂 Tải Macro",
            font=("Arial", 11),
            bg=self.button_color,
            fg="white",
            activebackground=self.button_hover,
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.load_macro
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        # Row 4: Info and Clear
        info_frame = tk.Frame(buttons_frame, bg=self.bg_color)
        info_frame.pack(fill="x", pady=5)
        
        tk.Button(
            info_frame,
            text="📋 Thông Tin",
            font=("Arial", 11),
            bg=self.button_color,
            fg="white",
            activebackground=self.button_hover,
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.show_info
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        tk.Button(
            info_frame,
            text="🗑️ Xóa Macro",
            font=("Arial", 11),
            bg="#ff6666",
            fg="white",
            activebackground="#cc0000",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.clear_macro
        ).pack(side="left", padx=5, fill="x", expand=True)
        
        # Emergency stop button (nổi bật)
        self.emergency_btn = tk.Button(
            buttons_frame,
            text="🛑 TẮT KHẨN CẤP",
            font=("Arial", 14, "bold"),
            bg="#ff0000",
            fg="white",
            activebackground="#cc0000",
            activeforeground="white",
            relief="raised",
            padx=20,
            pady=15,
            cursor="hand2",
            command=self.emergency_stop
        )
        self.emergency_btn.pack(fill="x", pady=10)
        
        # Settings button
        tk.Button(
            buttons_frame,
            text="⚙️ Cài Đặt",
            font=("Arial", 11),
            bg="#888888",
            fg="white",
            activebackground="#666666",
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=8,
            cursor="hand2",
            command=self.show_settings
        ).pack(fill="x", pady=5)
        
        # Log area
        log_label = tk.Label(
            self.root,
            text="Nhật ký hoạt động:",
            font=("Arial", 10),
            bg=self.bg_color,
            fg=self.fg_color,
            anchor="w"
        )
        log_label.pack(pady=(10, 5), padx=20, anchor="w")
        
        self.log_text = scrolledtext.ScrolledText(
            self.root,
            height=8,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#00ff00",
            relief="flat",
            borderwidth=0
        )
        self.log_text.pack(padx=20, pady=(0, 20), fill="both", expand=True)
        self.log_text.insert("1.0", "Chương trình đã sẵn sàng!\n")
        self.log_text.config(state="disabled")
        
    def log(self, message):
        """Ghi log"""
        self.log_text.config(state="normal")
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert("end", f"[{timestamp}] {message}\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        
    def update_status(self):
        """Cập nhật trạng thái"""
        status_parts = []
        color = "#00ff00"
        
        if self.recorder.recording:
            status_parts.append("🔴 ĐANG GHI")
            color = "#ff4444"
        if self.recorder.playing:
            status_parts.append("▶️ ĐANG PHÁT")
            color = "#44ff44"
        if not status_parts:
            status_parts.append("Sẵn sàng")
            
        self.status_label.config(
            text=f"Trạng thái: {' | '.join(status_parts)}",
            fg=color
        )
        
        info_parts = [f"Sự kiện: {len(self.recorder.events)}"]
        if self.recorder.current_macro_file:
            info_parts.append(f"File: {self.recorder.current_macro_file}")
        else:
            info_parts.append("File: Chưa có")
            
        self.info_label.config(text=" | ".join(info_parts))
        
        # Cập nhật button states
        self.record_btn.config(state="normal" if not self.recorder.recording else "disabled")
        self.stop_record_btn.config(state="normal" if self.recorder.recording else "disabled")
        self.play_btn.config(state="normal" if (not self.recorder.playing and self.recorder.events) else "disabled")
        self.stop_play_btn.config(state="normal" if self.recorder.playing else "disabled")
        
        # Cập nhật nút tắt khẩn cấp - luôn bật, nhưng nổi bật hơn khi đang chạy
        if self.recorder.recording or self.recorder.playing:
            self.emergency_btn.config(
                bg="#ff0000",
                text="🛑 TẮT KHẨN CẤP (ESC/F12)",
                font=("Arial", 14, "bold")
            )
        else:
            self.emergency_btn.config(
                bg="#cc0000",
                text="🛑 TẮT KHẨN CẤP",
                font=("Arial", 12, "bold")
            )
        
        self.root.after(500, self.update_status)
        
    def toggle_record(self):
        """Bật/tắt ghi macro"""
        if not self.recorder.recording:
            success, message = self.recorder.start_recording()
            if success:
                self.log(f"✅ {message}")
                messagebox.showinfo("Thành công", message)
            else:
                self.log(f"❌ {message}")
                messagebox.showerror("Lỗi", message)
        else:
            self.stop_record()
            
    def stop_record(self):
        """Dừng ghi macro"""
        success, message = self.recorder.stop_recording()
        if success:
            self.log(f"✅ {message}")
            messagebox.showinfo("Thành công", message)
        else:
            self.log(f"⚠️ {message}")
            messagebox.showwarning("Cảnh báo", message)
            
    def play_macro(self):
        """Phát macro"""
        if not self.recorder.events:
            messagebox.showwarning("Cảnh báo", "Không có macro để phát!\nHãy ghi hoặc tải macro trước.")
            return
            
        # Dialog để nhập số lần lặp và tốc độ
        dialog = tk.Toplevel(self.root)
        dialog.title("Phát Macro")
        dialog.geometry("300x150")
        dialog.configure(bg=self.bg_color)
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="Số lần lặp:", bg=self.bg_color, fg=self.fg_color).pack(pady=5)
        repeat_entry = tk.Entry(dialog, width=20)
        repeat_entry.insert(0, "1")
        repeat_entry.pack(pady=5)
        
        tk.Label(dialog, text="Tốc độ (1.0 = bình thường):", bg=self.bg_color, fg=self.fg_color).pack(pady=5)
        speed_entry = tk.Entry(dialog, width=20)
        speed_entry.insert(0, "1.0")
        speed_entry.pack(pady=5)
        
        def start_play():
            try:
                repeat = int(repeat_entry.get() or "1")
                speed = float(speed_entry.get() or "1.0")
                dialog.destroy()
                
                self.log(f"▶️ Bắt đầu phát macro ({repeat} lần, tốc độ {speed}x)")
                threading.Thread(target=lambda: self._play_in_thread(repeat, speed), daemon=True).start()
            except ValueError:
                messagebox.showerror("Lỗi", "Giá trị không hợp lệ!")
                
        tk.Button(dialog, text="Phát", command=start_play, bg=self.button_color, fg="white").pack(pady=10)
        
    def _play_in_thread(self, repeat, speed):
        """Phát macro trong thread riêng"""
        success, message = self.recorder.play_macro(repeat=repeat, speed=speed)
        if success:
            self.log(f"✅ {message}")
            messagebox.showinfo("Thành công", message)
        else:
            self.log(f"❌ {message}")
            messagebox.showerror("Lỗi", message)
            
    def emergency_stop(self):
        """Tắt khẩn cấp - Dừng tất cả"""
        stopped_anything = False
        
        # Dừng ghi nếu đang ghi
        if self.recorder.recording:
            success, message = self.recorder.stop_recording()
            if success:
                self.log(f"🛑 TẮT KHẨN CẤP: {message}")
                stopped_anything = True
                
        # Dừng phát nếu đang phát
        if self.recorder.playing:
            success, message = self.recorder.stop_playing()
            if success:
                self.log(f"🛑 TẮT KHẨN CẤP: {message}")
                stopped_anything = True
                
        if stopped_anything:
            messagebox.showwarning("Tắt khẩn cấp", "Đã dừng tất cả hoạt động!")
        else:
            messagebox.showinfo("Thông báo", "Không có hoạt động nào đang chạy.")
            
    def stop_play(self):
        """Dừng phát macro"""
        success, message = self.recorder.stop_playing()
        if success:
            self.log(f"✅ {message}")
            messagebox.showinfo("Thành công", message)
        else:
            self.log(f"⚠️ {message}")
            
    def save_macro(self):
        """Lưu macro"""
        if not self.recorder.events:
            messagebox.showwarning("Cảnh báo", "Không có macro để lưu!")
            return
            
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Lưu Macro"
        )
        
        if filename:
            success, message = self.recorder.save_macro(filename)
            if success:
                self.log(f"✅ {message}")
                messagebox.showinfo("Thành công", message)
            else:
                self.log(f"❌ {message}")
                messagebox.showerror("Lỗi", message)
                
    def load_macro(self):
        """Tải macro"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Tải Macro"
        )
        
        if filename:
            success, message = self.recorder.load_macro(filename)
            if success:
                self.log(f"✅ {message}")
                messagebox.showinfo("Thành công", message)
            else:
                self.log(f"❌ {message}")
                messagebox.showerror("Lỗi", message)
                
    def show_info(self):
        """Hiển thị thông tin macro"""
        if not self.recorder.events:
            messagebox.showinfo("Thông tin", "Không có macro!")
            return
            
        keyboard_events = sum(1 for e in self.recorder.events if e['type'] == 'keyboard')
        mouse_events = sum(1 for e in self.recorder.events if e['type'].startswith('mouse'))
        total_time = max(e['time'] for e in self.recorder.events) if self.recorder.events else 0
        
        info = f"""Thông tin Macro:

📊 Tổng số sự kiện: {len(self.recorder.events)}
⌨️ Sự kiện bàn phím: {keyboard_events}
🖱️ Sự kiện chuột: {mouse_events}
⏱️ Thời lượng: {total_time:.2f} giây
💾 File: {self.recorder.current_macro_file or 'Chưa lưu'}
"""
        messagebox.showinfo("Thông tin Macro", info)
        self.log("📋 Đã xem thông tin macro")
        
    def clear_macro(self):
        """Xóa macro"""
        if not self.recorder.events:
            messagebox.showinfo("Thông báo", "Không có macro để xóa!")
            return
            
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa macro hiện tại?"):
            self.recorder.events = []
            self.recorder.current_macro_file = None
            self.log("🗑️ Đã xóa macro")
            messagebox.showinfo("Thành công", "Đã xóa macro!")
            
    def show_settings(self):
        """Hiển thị cài đặt"""
        settings_text = """HƯỚNG DẪN SỬ DỤNG:

1. Ghi Macro:
   - Click nút "Ghi Macro"
   - Thực hiện các hành động
   - Click "Dừng Ghi" khi xong

2. Phát Macro:
   - Click "Phát Macro"
   - Nhập số lần lặp và tốc độ
   - Click "Dừng Phát" nếu cần

3. Lưu/Tải:
   - Dùng nút "Lưu Macro" để lưu
   - Dùng nút "Tải Macro" để tải

4. TẮT KHẨN CẤP:
   - Click nút "TẮT KHẨN CẤP" (màu đỏ)
   - Hoặc nhấn phím ESC
   - Hoặc nhấn phím F12
   - Sẽ dừng tất cả hoạt động ngay lập tức

LƯU Ý:
- Có thể cần chạy với quyền Administrator
- Luôn lưu macro sau khi ghi
- Dùng nút TẮT KHẨN CẤP nếu macro chạy sai
"""
        messagebox.showinfo("Cài đặt & Hướng dẫn", settings_text)
        
    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()


def main():
    """Hàm chính"""
    try:
        app = MacroGUI()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 Tạm biệt!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()


