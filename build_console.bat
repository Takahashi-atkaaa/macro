@echo off
chcp 65001 >nul
REM Build macro.py (file duy nhất đã gộp tất cả) với console
python -m pip install pyinstaller
pyinstaller --onefile --console --name Macro macro.py
pause

