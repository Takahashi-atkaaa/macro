@echo off
chcp 65001 >nul
title Chương trình Macro cho Windows
echo.
echo ========================================
echo   CHƯƠNG TRÌNH MACRO CHO WINDOWS
echo ========================================
echo.
echo Đang khởi động...
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ LỖI: Không tìm thấy Python!
    echo.
    echo ========================================
    echo   PYTHON CHƯA ĐƯỢC CÀI ĐẶT
    echo ========================================
    echo.
    echo Có 2 cách:
    echo.
    echo [1] Chạy file CAI_PYTHON.bat để cài đặt tự động
    echo [2] Cài đặt thủ công từ: https://www.python.org/downloads/
    echo.
    echo QUAN TRỌNG: Khi cài, nhớ tích vào "Add Python to PATH"
    echo.
    set /p choice="Chọn (1 hoặc 2): "
    if "%choice%"=="1" (
        if exist "CAI_PYTHON.bat" (
            call CAI_PYTHON.bat
        ) else (
            echo File CAI_PYTHON.bat không tìm thấy!
            echo Vui lòng cài Python thủ công.
            pause
        )
    )
    exit /b 1
)

REM Chạy chương trình (GUI)
python macro_gui.py

REM Nếu có lỗi
if errorlevel 1 (
    echo.
    echo ❌ Có lỗi xảy ra!
    echo.
    echo Thử chạy với quyền Administrator:
    echo Right-click file này → Run as administrator
    echo.
    pause
)

