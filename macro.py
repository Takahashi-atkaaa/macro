#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chương trình Macro cho Windows - Tất cả trong một
Hỗ trợ ghi và phát lại các hành động bàn phím và chuột
Với menu điều khiển đẹp và hotkeys tiện lợi
"""

import os
import time
import json
import sys
from datetime import datetime

try:
    import keyboard
    import mouse
except ImportError:
    print("Đang cài đặt thư viện cần thiết...")
    import subprocess
    subprocess.check_call(["pip", "install", "keyboard", "mouse"])
    import keyboard
    import mouse


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
        
        # Ghi sự kiện bàn phím
        keyboard.hook(self._on_keyboard_event)
        # Ghi sự kiện chuột
        mouse.hook(self._on_mouse_event)
        
        return True, "Đã bắt đầu ghi macro... (Quay lại menu và chọn [2] để dừng)"
        
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
                        
                    # Tính thời gian chờ
                    delay = (event['time'] - last_time) / speed
                    if delay > 0:
                        time.sleep(delay)
                    
                    last_time = event['time']
                    
                    # Thực hiện sự kiện
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


class MenuController:
    """Lớp quản lý menu điều khiển"""
    
    def __init__(self):
        self.recorder = MacroRecorder()
        self.running = True
        
    def clear_screen(self):
        """Xóa màn hình"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """In header menu"""
        print("=" * 60)
        print(" " * 15 + "CHƯƠNG TRÌNH MACRO CHO WINDOWS")
        print("=" * 60)
        print()
    
    def print_status(self):
        """In trạng thái hiện tại"""
        status = []
        if self.recorder.recording:
            status.append("🔴 ĐANG GHI")
        if self.recorder.playing:
            status.append("▶️ ĐANG PHÁT")
        if self.recorder.events:
            status.append(f"📝 {len(self.recorder.events)} sự kiện")
        if self.recorder.current_macro_file:
            status.append(f"💾 {self.recorder.current_macro_file}")
        
        if status:
            print("Trạng thái: " + " | ".join(status))
        else:
            print("Trạng thái: Sẵn sàng")
        print("-" * 60)
        print()
    
    def print_menu(self):
        """In menu chính"""
        print("MENU ĐIỀU KHIỂN:")
        print()
        print("  [1] 📹 Ghi macro mới")
        print("  [2] ⏹️  Dừng ghi macro")
        print("  [3] ▶️  Phát macro")
        print("  [4] ⏸️  Dừng phát macro")
        print("  [5] 💾 Lưu macro")
        print("  [6] 📂 Tải macro")
        print("  [7] 📋 Xem thông tin macro")
        print("  [8] 🗑️  Xóa macro hiện tại")
        print("  [9] ⚙️  Cài đặt & Hotkeys")
        print("  [0] ❌ Thoát")
        print()
        print("-" * 60)
    
    def handle_choice(self, choice):
        """Xử lý lựa chọn của người dùng"""
        if choice == '1':
            self.record_macro()
        elif choice == '2':
            self.stop_recording()
        elif choice == '3':
            self.play_macro()
        elif choice == '4':
            self.stop_playing()
        elif choice == '5':
            self.save_macro()
        elif choice == '6':
            self.load_macro()
        elif choice == '7':
            self.show_macro_info()
        elif choice == '8':
            self.clear_macro()
        elif choice == '9':
            self.settings()
        elif choice == '0':
            self.exit_program()
        else:
            print("❌ Lựa chọn không hợp lệ!")
            time.sleep(1)
    
    def record_macro(self):
        """Ghi macro"""
        if self.recorder.recording:
            print("⚠️  Đang ghi rồi! Nhấn [2] trong menu để dừng.")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        print("\n" + "=" * 60)
        print("GHI MACRO MỚI")
        print("=" * 60)
        print("\nHướng dẫn:")
        print("  - Chương trình sẽ bắt đầu ghi ngay sau khi bạn nhấn Enter")
        print("  - Thực hiện các hành động bạn muốn ghi lại")
        print("  - Sau khi xong, quay lại menu và chọn [2] để dừng ghi")
        print("\nNhấn Enter để bắt đầu ghi, hoặc bất kỳ phím nào khác để hủy...")
        
        try:
            event = keyboard.read_event()
            if event.name == 'enter' and event.event_type == 'down':
                success, message = self.recorder.start_recording()
                print(f"\n{message}")
                print("\nĐang ghi... Quay lại menu và chọn [2] để dừng ghi.")
                print("(Bạn có thể tiếp tục làm việc bình thường)")
                input("\nNhấn Enter để quay lại menu...")
            else:
                print("\nĐã hủy!")
                input("\nNhấn Enter để tiếp tục...")
        except Exception as e:
            print(f"\nLỗi: {e}")
            input("\nNhấn Enter để tiếp tục...")
    
    def stop_recording(self):
        """Dừng ghi macro"""
        success, message = self.recorder.stop_recording()
        if success:
            print(f"\n✅ {message}")
        else:
            print(f"\n⚠️  {message}")
        input("\nNhấn Enter để tiếp tục...")
    
    def play_macro(self):
        """Phát macro"""
        if not self.recorder.events:
            print("\n❌ Không có macro để phát!")
            print("Hãy ghi hoặc tải macro trước.")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        print("\n" + "=" * 60)
        print("PHÁT MACRO")
        print("=" * 60)
        print(f"\nMacro hiện tại: {len(self.recorder.events)} sự kiện")
        
        try:
            repeat = input("Số lần lặp lại (mặc định 1): ").strip() or "1"
            repeat = int(repeat)
            
            speed = input("Tốc độ phát (1.0 = bình thường, mặc định 1.0): ").strip() or "1.0"
            speed = float(speed)
            
            print(f"\nBắt đầu phát macro ({repeat} lần, tốc độ {speed}x)...")
            print("Quay lại menu và chọn [4] để dừng phát nếu cần")
            time.sleep(2)
            
            success, message = self.recorder.play_macro(repeat=repeat, speed=speed)
            if success:
                print(f"\n✅ {message}")
            else:
                print(f"\n❌ {message}")
        except ValueError:
            print("\n❌ Giá trị không hợp lệ!")
        except KeyboardInterrupt:
            self.recorder.stop_playing()
            print("\n\nĐã dừng phát!")
        
        input("\nNhấn Enter để tiếp tục...")
    
    def stop_playing(self):
        """Dừng phát macro"""
        success, message = self.recorder.stop_playing()
        if success:
            print(f"\n✅ {message}")
        else:
            print(f"\n⚠️  {message}")
        input("\nNhấn Enter để tiếp tục...")
    
    def save_macro(self):
        """Lưu macro"""
        if not self.recorder.events:
            print("\n❌ Không có macro để lưu!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        print("\n" + "=" * 60)
        print("LƯU MACRO")
        print("=" * 60)
        filename = input("\nTên file (mặc định: macro.json): ").strip() or "macro.json"
        
        success, message = self.recorder.save_macro(filename)
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
        
        input("\nNhấn Enter để tiếp tục...")
    
    def load_macro(self):
        """Tải macro"""
        print("\n" + "=" * 60)
        print("TẢI MACRO")
        print("=" * 60)
        
        # Liệt kê các file .json trong thư mục hiện tại
        json_files = [f for f in os.listdir('.') if f.endswith('.json')]
        if json_files:
            print("\nCác file macro có sẵn:")
            for i, f in enumerate(json_files, 1):
                print(f"  [{i}] {f}")
            print()
        
        filename = input("Tên file (mặc định: macro.json): ").strip() or "macro.json"
        
        success, message = self.recorder.load_macro(filename)
        if success:
            print(f"✅ {message}")
        else:
            print(f"❌ {message}")
        
        input("\nNhấn Enter để tiếp tục...")
    
    def show_macro_info(self):
        """Hiển thị thông tin macro"""
        print("\n" + "=" * 60)
        print("THÔNG TIN MACRO")
        print("=" * 60)
        
        if not self.recorder.events:
            print("\n❌ Không có macro!")
        else:
            print(f"\n📊 Tổng số sự kiện: {len(self.recorder.events)}")
            if self.recorder.current_macro_file:
                print(f"💾 File: {self.recorder.current_macro_file}")
            
            # Thống kê
            keyboard_events = sum(1 for e in self.recorder.events if e['type'] == 'keyboard')
            mouse_events = sum(1 for e in self.recorder.events if e['type'].startswith('mouse'))
            
            print(f"\n📈 Thống kê:")
            print(f"  - Sự kiện bàn phím: {keyboard_events}")
            print(f"  - Sự kiện chuột: {mouse_events}")
            
            if self.recorder.events:
                total_time = max(e['time'] for e in self.recorder.events)
                print(f"  - Thời lượng: {total_time:.2f} giây")
        
        input("\nNhấn Enter để tiếp tục...")
    
    def clear_macro(self):
        """Xóa macro hiện tại"""
        if not self.recorder.events:
            print("\n❌ Không có macro để xóa!")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        print("\n⚠️  Bạn có chắc muốn xóa macro hiện tại?")
        confirm = input("Nhập 'yes' để xác nhận: ").strip().lower()
        
        if confirm == 'yes':
            self.recorder.events = []
            self.recorder.current_macro_file = None
            print("✅ Đã xóa macro!")
        else:
            print("Đã hủy!")
        
        input("\nNhấn Enter để tiếp tục...")
    
    def settings(self):
        """Cài đặt"""
        print("\n" + "=" * 60)
        print("CÀI ĐẶT")
        print("=" * 60)
        print("\nHƯỚNG DẪN SỬ DỤNG:")
        print("-" * 60)
        print("  - Tất cả chức năng được điều khiển qua menu")
        print("  - Chọn số từ 0-9 để thực hiện chức năng tương ứng")
        print("  - Khi đang ghi macro, quay lại menu và chọn [2] để dừng")
        print("  - Khi đang phát macro, quay lại menu và chọn [4] để dừng")
        print("-" * 60)
        print("\nLƯU Ý:")
        print("  - Trên Windows, có thể cần chạy với quyền Administrator")
        print("  - Luôn lưu macro sau khi ghi để tránh mất dữ liệu")
        print("  - Macro được lưu dưới dạng file JSON")
        print("-" * 60)
        input("\nNhấn Enter để tiếp tục...")
    
    def exit_program(self):
        """Thoát chương trình"""
        if self.recorder.recording:
            print("\n⚠️  Đang ghi macro! Dừng ghi trước khi thoát.")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        if self.recorder.playing:
            print("\n⚠️  Đang phát macro! Dừng phát trước khi thoát.")
            input("\nNhấn Enter để tiếp tục...")
            return
        
        print("\n👋 Tạm biệt!")
        self.running = False
    
    def run(self):
        """Chạy menu chính"""
        while self.running:
            self.clear_screen()
            self.print_header()
            self.print_status()
            self.print_menu()
            
            try:
                choice = input("Chọn chức năng (0-9): ").strip()
                self.handle_choice(choice)
            except KeyboardInterrupt:
                print("\n\n⚠️  Nhấn Ctrl+C để thoát. Hoặc chọn [0] trong menu.")
                time.sleep(2)
            except Exception as e:
                print(f"\n❌ Lỗi: {e}")
                input("\nNhấn Enter để tiếp tục...")


def main():
    """Hàm chính"""
    try:
        controller = MenuController()
        controller.run()
    except KeyboardInterrupt:
        print("\n\n👋 Tạm biệt!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        input("\nNhấn Enter để thoát...")


if __name__ == "__main__":
    main()
