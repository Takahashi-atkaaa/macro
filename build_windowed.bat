@echo off
chcp 65001 >nul
REM Build macro.py (file duy nhất) không có console (chạy ngầm)
python -m pip install pyinstaller
pyinstaller --onefile --windowed --name Macro macro.py
pause

