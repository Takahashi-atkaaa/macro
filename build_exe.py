#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script để build chương trình macro thành file .exe
"""

import subprocess
import sys
import os

def install_pyinstaller():
    """Cài đặt PyInstaller nếu chưa có"""
    try:
        import PyInstaller
        print("PyInstaller đã được cài đặt!")
    except ImportError:
        print("Đang cài đặt PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("Đã cài đặt PyInstaller!")

def build_exe():
    """Build file .exe"""
    print("\n" + "="*50)
    print("BUILD CHƯƠNG TRÌNH MACRO THÀNH .EXE")
    print("="*50)
    
    # Cài đặt PyInstaller
    install_pyinstaller()
    
    # Build file macro.py (đã gộp tất cả)
    print("\nChương trình macro đã được gộp vào 1 file: macro.py")
    script = "macro.py"
    name = "Macro"
    
    print(f"\nĐang build {script}...")
    
    # Lệnh PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",  # Tạo 1 file .exe duy nhất
        "--windowed",  # Không hiện console
        "--name", name,
        script
    ]
    
    # Nếu muốn có console để xem output, dùng lệnh này thay thế:
    cmd_with_console = [
        "pyinstaller",
        "--onefile",
        "--console",  # Hiện console
        "--name", name,
        script
    ]
    
    # Hỏi người dùng có muốn console không
    console_choice = input("Có muốn hiện cửa sổ console khi chạy? (y/n, mặc định y): ").strip().lower() or "y"
    
    if console_choice == "n":
        final_cmd = cmd
    else:
        final_cmd = cmd_with_console
    
    try:
        subprocess.run(final_cmd, check=True)
        print("\n" + "="*50)
        print("BUILD THÀNH CÔNG!")
        print("="*50)
        print(f"\nFile .exe được tạo tại: dist/{name}.exe")
        print("\nBạn có thể copy file .exe này sang bất kỳ máy Windows nào để chạy!")
        print("(Không cần cài Python)")
    except subprocess.CalledProcessError as e:
        print(f"\nLỗi khi build: {e}")
        print("\nThử chạy lệnh sau trong Command Prompt (với quyền Admin):")
        print(f"pyinstaller --onefile --console --name {name} {script}")
    except Exception as e:
        print(f"\nLỗi: {e}")

if __name__ == "__main__":
    try:
        build_exe()
    except KeyboardInterrupt:
        print("\n\nĐã hủy!")
    except Exception as e:
        print(f"\nLỗi: {e}")
        import traceback
        traceback.print_exc()

