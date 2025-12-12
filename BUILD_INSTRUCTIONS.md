# Hướng dẫn Build thành file .EXE

## Cách 1: Sử dụng file .bat (Dễ nhất - Windows)

1. **Mở Command Prompt với quyền Administrator:**
   - Nhấn `Windows + R`
   - Gõ `cmd`
   - Nhấn `Ctrl + Shift + Enter` (để chạy với quyền Admin)

2. **Chuyển đến thư mục chứa file:**
   ```cmd
   cd "C:\path\to\tapj nham"
   ```

3. **Chạy file build:**
   - **Double-click vào `build_console.bat`** (khuyến nghị - có console để xem output)
   - Hoặc double-click vào `build.bat`
   - Hoặc double-click vào `build_windowed.bat` (không có console)

4. **Đợi build xong:**
   - File .exe sẽ được tạo trong thư mục `dist\`
   - Tên file: `Macro.exe`

## Cách 2: Build thủ công (Windows)

1. **Mở Command Prompt với quyền Administrator**

2. **Chuyển đến thư mục:**
   ```cmd
   cd "C:\path\to\tapj nham"
   ```

3. **Cài đặt PyInstaller:**
   ```cmd
   pip install pyinstaller
   ```

4. **Build với console (khuyến nghị):**
   ```cmd
   pyinstaller --onefile --console --name Macro macro.py
   ```

5. **Hoặc build không có console:**
   ```cmd
   pyinstaller --onefile --windowed --name Macro macro.py
   ```

6. **File .exe sẽ ở:** `dist\Macro.exe`

## Cách 3: Sử dụng Python script

```cmd
python build_exe.py
```

## Lưu ý khi build:

- ✅ **Phải chạy trên Windows** - Không thể build .exe trên Mac/Linux
- ✅ **Cần quyền Administrator** - Để tránh lỗi
- ✅ **Cài đặt Python trước** - Python 3.6 trở lên
- ✅ **File .exe đầu tiên chạy chậm** - PyInstaller đang giải nén
- ⚠️ **Windows Defender có thể cảnh báo** - Đây là false positive, bình thường

## Sau khi build:

1. Copy file `dist\Macro.exe` ra nơi bạn muốn
2. Có thể chạy trên bất kỳ máy Windows nào (không cần cài Python)
3. Chạy với quyền Administrator nếu cần

## Troubleshooting:

### Lỗi: "pyinstaller is not recognized"
- Chạy: `pip install pyinstaller`
- Hoặc: `python -m pip install pyinstaller`

### Lỗi: "Permission denied"
- Chạy Command Prompt với quyền Administrator

### File .exe quá lớn
- Bình thường, file .exe sẽ khoảng 10-20MB (đã bao gồm Python runtime)

### File .exe bị Windows Defender xóa
- Thêm vào whitelist của Windows Defender
- Hoặc tắt tạm thời khi build

