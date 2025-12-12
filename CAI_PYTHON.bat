@echo off
chcp 65001 >nul
title Cài đặt Python cho Macro
color 0A

echo.
echo ========================================
echo   KIỂM TRA VÀ CÀI ĐẶT PYTHON
echo ========================================
echo.

REM Kiểm tra Python đã cài chưa
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Python đã được cài đặt!
    python --version
    echo.
    echo Bạn có thể chạy CHAY_MACRO.bat ngay bây giờ!
    echo.
    pause
    exit /b 0
)

echo ❌ Python chưa được cài đặt!
echo.
echo ========================================
echo   HƯỚNG DẪN CÀI ĐẶT PYTHON
echo ========================================
echo.
echo Có 2 cách để cài Python:
echo.
echo [1] Tự động mở trang tải Python (Khuyến nghị)
echo [2] Hướng dẫn cài đặt thủ công
echo [3] Thoát
echo.
set /p choice="Chọn (1, 2 hoặc 3): "

if "%choice%"=="1" (
    echo.
    echo Đang mở trang tải Python...
    start https://www.python.org/downloads/
    echo.
    echo ========================================
    echo   HƯỚNG DẪN CÀI ĐẶT
    echo ========================================
    echo.
    echo 1. Trang web Python đã được mở
    echo 2. Click nút "Download Python" (màu vàng)
    echo 3. Chạy file .exe vừa tải về
    echo 4. QUAN TRỌNG: Tích vào "Add Python to PATH" ⭐
    echo 5. Click "Install Now"
    echo 6. Đợi cài đặt xong
    echo 7. Chạy lại file này để kiểm tra
    echo.
    echo ========================================
    pause
    exit /b 0
)

if "%choice%"=="2" (
    echo.
    echo ========================================
    echo   HƯỚNG DẪN CÀI ĐẶT THỦ CÔNG
    echo ========================================
    echo.
    echo Bước 1: Tải Python
    echo   - Vào: https://www.python.org/downloads/
    echo   - Click "Download Python" (phiên bản mới nhất)
    echo.
    echo Bước 2: Cài đặt Python
    echo   - Chạy file .exe vừa tải về
    echo   - ⭐ QUAN TRỌNG: Tích vào "Add Python to PATH"
    echo   - Click "Install Now"
    echo   - Đợi cài đặt xong
    echo.
    echo Bước 3: Kiểm tra
    echo   - Chạy lại file này
    echo   - Hoặc mở Command Prompt và gõ: python --version
    echo.
    echo ========================================
    echo.
    set /p open="Bạn có muốn mở trang tải Python không? (y/n): "
    if /i "%open%"=="y" (
        start https://www.python.org/downloads/
    )
    pause
    exit /b 0
)

if "%choice%"=="3" (
    exit /b 0
)

echo.
echo Lựa chọn không hợp lệ!
pause


