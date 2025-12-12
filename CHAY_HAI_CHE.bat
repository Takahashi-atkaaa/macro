@echo off
chcp 65001 >nul
title Tool Tự Động Hái Chè GTV
color 0A

echo.
echo ========================================
echo   TOOL TỰ ĐỘNG HÁI CHÈ GTV
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

echo Đang khởi động tool hái chè...
echo.
echo LƯU Ý: Tool sẽ tự động cài đặt thư viện cần thiết
echo.
timeout /t 2 /nobreak >nul

REM Chạy chương trình
python macro_hai_che.py

if errorlevel 1 (
    echo.
    echo ❌ Có lỗi xảy ra!
    echo.
    echo Thử chạy với quyền Administrator
    echo.
    pause
)

