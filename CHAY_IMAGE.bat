@echo off
chcp 65001 >nul
title Tool Macro Nhận Diện Hình Ảnh
color 0A

echo.
echo ========================================
echo   TOOL MACRO NHẬN DIỆN HÌNH ẢNH
echo ========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ LỖI: Không tìm thấy Python!
    echo.
    echo Chạy file CAI_PYTHON.bat để cài Python
    echo.
    pause
    exit /b 1
)

echo Đang kiểm tra file macro_image.py...
if not exist "macro_image.py" (
    echo.
    echo ❌ LỖI: Không tìm thấy file macro_image.py!
    echo.
    echo Đảm bảo file macro_image.py nằm trong cùng thư mục
    echo.
    pause
    exit /b 1
)

echo ✅ Đã tìm thấy file
echo.
echo Đang khởi động tool...
echo.
echo LƯU Ý: Tool sẽ tự động cài đặt các thư viện cần thiết
echo (Pillow, opencv-python, numpy, pyautogui)
echo.
timeout /t 2 /nobreak >nul

REM Chạy chương trình
python macro_image.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo ❌ CÓ LỖI XẢY RA!
    echo ========================================
    echo.
    echo Có thể do:
    echo 1. Chưa cài đặt Python
    echo 2. Thiếu quyền Administrator
    echo 3. Lỗi khi cài đặt thư viện
    echo.
    echo Thử:
    echo - Chạy với quyền Administrator (Right-click → Run as administrator)
    echo - Kiểm tra kết nối internet
    echo - Chạy lại file này
    echo.
    pause
)

