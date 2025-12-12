@echo off
chcp 65001 >nul
echo ========================================
echo BUILD MACRO THÀNH FILE .EXE
echo ========================================
echo.

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Lỗi: Không tìm thấy Python!
    echo Vui lòng cài đặt Python trước.
    pause
    exit /b 1
)

echo Đang cài đặt PyInstaller...
python -m pip install pyinstaller

echo.
echo Chương trình macro đã được gộp vào 1 file: macro.py
echo.
set script=macro.py
set name=Macro

echo.
echo Đang build %script%...
echo.

REM Build với console (để xem output)
pyinstaller --onefile --console --name %name% %script%

if errorlevel 1 (
    echo.
    echo Lỗi khi build!
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD THÀNH CÔNG!
echo ========================================
echo.
echo File .exe được tạo tại: dist\%name%.exe
echo.
echo Bạn có thể copy file này sang bất kỳ máy Windows nào!
echo.
pause

