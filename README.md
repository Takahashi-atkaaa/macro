# Chương trình Macro cho Windows

Chương trình macro đơn giản để ghi và phát lại các hành động bàn phím và chuột trên Windows.

## Tính năng

- ✅ Ghi lại các hành động bàn phím và chuột
- ✅ Phát lại macro đã ghi
- ✅ Lưu/tải macro từ file JSON
- ✅ Điều chỉnh tốc độ phát và số lần lặp
- ✅ **Menu điều khiển đẹp và dễ sử dụng** (chỉ dùng menu, không cần hotkeys)

## Cài đặt

1. Cài đặt Python 3.6 trở lên

2. Cài đặt các thư viện cần thiết:

```bash
pip install -r requirements.txt
```

**Lưu ý:** Trên Windows, bạn có thể cần chạy với quyền Administrator để sử dụng các thư viện `keyboard` và `mouse`.

## Quick Start (Bắt đầu nhanh)

### 3 bước đơn giản:

1. **Cài đặt:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Chạy chương trình:**

   ```bash
   python macro.py
   ```

   _(Chạy Command Prompt với quyền Administrator nếu cần)_

3. **Sử dụng ngay:**
   - Nhấn **[1]** → Enter để ghi macro
   - Thực hiện các hành động bạn muốn ghi lại
   - Nhấn **[2]** → Enter để dừng ghi
   - Nhấn **[5]** → Enter để lưu macro
   - Nhấn **[3]** → Enter để phát macro

**Xem hướng dẫn chi tiết bên dưới để biết thêm!**

## Sử dụng

### Chạy chương trình:

**Tất cả tính năng đã được gộp vào 1 file duy nhất:**

```bash
python macro.py
```

File này bao gồm:

- ✅ Menu điều khiển đẹp và dễ sử dụng
- ✅ Tất cả các tính năng ghi/phát macro
- ✅ Chỉ dùng menu, không cần nhớ hotkeys

### Menu điều khiển:

Menu với các tùy chọn:

- **[1]** 📹 Ghi macro mới
- **[2]** ⏹️ Dừng ghi macro
- **[3]** ▶️ Phát macro
- **[4]** ⏸️ Dừng phát macro
- **[5]** 💾 Lưu macro
- **[6]** 📂 Tải macro
- **[7]** 📋 Xem thông tin macro
- **[8]** 🗑️ Xóa macro hiện tại
- **[9]** ⚙️ Cài đặt
- **[0]** ❌ Thoát

### Lưu ý:

- **Chỉ sử dụng menu** - Tất cả chức năng được điều khiển qua menu số (0-9)
- **Không cần hotkeys** - Đơn giản và dễ sử dụng hơn

## Hướng dẫn sử dụng chi tiết

### Bước 1: Khởi động chương trình

1. Mở Command Prompt hoặc PowerShell
2. Chuyển đến thư mục chứa file `macro.py`
3. Chạy lệnh: `python macro.py`
4. Giao diện menu sẽ hiện ra

**Lưu ý:** Nếu gặp lỗi về quyền truy cập, hãy chạy Command Prompt với quyền Administrator (Right-click → Run as administrator)

### Bước 2: Ghi macro mới

#### Cách 1: Sử dụng Menu (Khuyến nghị cho người mới)

1. Trong menu chính, nhấn phím **1** và Enter
2. Đọc hướng dẫn, sau đó nhấn **Enter** để bắt đầu ghi
3. **Thực hiện các hành động** bạn muốn ghi lại:
   - Gõ phím, nhấn tổ hợp phím
   - Di chuyển chuột, click chuột
   - Scroll chuột
4. Sau khi xong, quay lại menu và nhấn **[2]** → Enter để dừng ghi
5. Bạn sẽ thấy thông báo số sự kiện đã ghi

**Ví dụ thực tế:**

- Ghi macro mở Notepad và gõ "Hello World":
  1. Nhấn [1] trong menu → Enter
  2. Nhấn Windows + R (mở Run)
  3. Gõ "notepad" → Enter
  4. Gõ "Hello World"
  5. Quay lại menu và nhấn [2] để dừng ghi

### Bước 3: Xem thông tin macro

1. Nhấn phím **7** trong menu
2. Xem thống kê:
   - Tổng số sự kiện
   - Số sự kiện bàn phím
   - Số sự kiện chuột
   - Thời lượng macro

### Bước 4: Lưu macro

**Quan trọng:** Luôn lưu macro sau khi ghi để không bị mất!

1. Nhấn phím **5** trong menu
2. Nhập tên file (ví dụ: `notepad_macro.json`)
3. Nhấn Enter
4. File sẽ được lưu trong cùng thư mục với chương trình

**Lưu ý:**

- Không cần gõ `.json`, chương trình sẽ tự thêm
- Nếu không nhập tên, mặc định là `macro.json`

### Bước 5: Phát macro

1. Nhấn phím **3** trong menu
2. Nhập số lần lặp lại:
   - Nhấn Enter để phát 1 lần (mặc định)
   - Hoặc nhập số (ví dụ: 5 để phát 5 lần)
3. Nhập tốc độ phát:
   - Nhấn Enter để phát tốc độ bình thường (1.0)
   - Hoặc nhập số:
     - `0.5` = chậm gấp đôi
     - `1.0` = bình thường
     - `2.0` = nhanh gấp đôi
     - `5.0` = nhanh gấp 5 lần
4. Đợi 2 giây (thời gian chuẩn bị)
5. Macro sẽ tự động phát
6. Quay lại menu và nhấn **[4]** → Enter để dừng nếu cần

**Ví dụ:**

```
Số lần lặp lại: 3
Tốc độ phát: 2.0
→ Macro sẽ phát 3 lần với tốc độ nhanh gấp đôi
```

### Bước 6: Tải macro đã lưu

1. Nhấn phím **6** trong menu
2. Xem danh sách các file macro có sẵn (nếu có)
3. Nhập tên file (ví dụ: `notepad_macro.json`)
4. Nhấn Enter
5. Macro sẽ được tải vào bộ nhớ

**Lưu ý:**

- Có thể nhập số thứ tự từ danh sách (nếu có)
- Không cần gõ `.json`

### Bước 7: Xóa macro hiện tại

1. Nhấn phím **8** trong menu
2. Nhập `yes` để xác nhận
3. Macro trong bộ nhớ sẽ bị xóa

**Lưu ý:** File đã lưu trên đĩa không bị xóa, chỉ xóa macro trong bộ nhớ

### Các tình huống sử dụng thực tế

#### Tình huống 1: Tự động mở và gõ email

1. Ghi macro:

   - Mở trình duyệt
   - Mở Gmail
   - Click vào "Compose"
   - Gõ địa chỉ email
   - Gõ tiêu đề
   - Gõ nội dung
   - Quay lại menu và nhấn [2] để dừng ghi

2. Lưu với tên: `send_email.json`

3. Khi cần: Phát macro với số lần lặp = 1

#### Tình huống 2: Tự động mở nhiều chương trình

1. Ghi macro:

   - Mở Notepad
   - Mở Calculator
   - Mở Browser
   - Quay lại menu và nhấn [2] để dừng ghi

2. Lưu và phát khi khởi động máy

#### Tình huống 3: Lặp lại thao tác nhiều lần

1. Ghi macro cho 1 lần thao tác
2. Phát macro với số lần lặp = 10, 20, 100...
3. Dùng tốc độ cao (2.0 - 5.0) để tiết kiệm thời gian

### Mẹo sử dụng

1. **Luôn lưu macro sau khi ghi** - Tránh mất công khi tắt chương trình
2. **Đặt tên file rõ ràng** - Dễ nhớ và quản lý (ví dụ: `open_chrome.json`, `type_password.json`)
3. **Test macro trước khi dùng nhiều lần** - Phát 1 lần để kiểm tra
4. **Dùng tốc độ phát hợp lý** - Quá nhanh có thể gây lỗi
5. **Dừng macro khi cần** - Quay lại menu và chọn [4] để dừng phát
6. **Backup file macro** - Copy các file `.json` để dự phòng

### Xử lý lỗi thường gặp

#### Lỗi: "Không có macro để phát"

- **Nguyên nhân:** Chưa ghi hoặc chưa tải macro
- **Giải pháp:** Ghi macro mới hoặc tải macro từ file

#### Lỗi: "Không tìm thấy file"

- **Nguyên nhân:** Tên file sai hoặc file không tồn tại
- **Giải pháp:** Kiểm tra tên file, xem danh sách file có sẵn trong menu [6]

#### Macro phát không đúng

- **Nguyên nhân:** Màn hình/resolution thay đổi, cửa sổ đã đóng
- **Giải pháp:** Đảm bảo môi trường giống khi ghi, ghi lại macro

#### Không ghi được sự kiện

- **Nguyên nhân:** Chưa chạy với quyền Administrator
- **Giải pháp:** Chạy Command Prompt với quyền Administrator

#### Menu không phản hồi

- **Nguyên nhân:** Chương trình đang xử lý macro
- **Giải pháp:** Đợi một chút hoặc nhấn Ctrl+C để thoát và chạy lại

## Ví dụ

### Ghi và phát macro tự động:

```python
from macro import MacroRecorder

recorder = MacroRecorder()

# Bắt đầu ghi
recorder.start_recording()
# ... thực hiện các hành động ...
recorder.stop_recording()

# Lưu macro
recorder.save_macro('my_macro.json')

# Tải và phát lại
recorder.load_macro('my_macro.json')
recorder.play_macro(repeat=5, speed=2.0)  # Phát 5 lần với tốc độ 2x
```

## Lưu ý

- Trên Windows, có thể cần chạy với quyền Administrator
- Macro được lưu dưới dạng JSON, có thể chỉnh sửa thủ công nếu cần
- Thời gian giữa các sự kiện được ghi lại chính xác để phát lại đúng nhịp độ

## Yêu cầu hệ thống

- Windows 7 trở lên
- Python 3.6+
- Quyền Administrator (khuyến nghị)

## Cách chạy chương trình (Không cần build .exe)

### Trên Windows:

- **Cách 1:** Double-click vào `run_macro.bat`
- **Cách 2:** Mở Command Prompt và chạy: `python macro.py`

### Trên Mac/Linux:

- Chạy: `python3 macro.py`
- Hoặc: `chmod +x run_macro.sh && ./run_macro.sh`

**Lưu ý:** Cần cài Python và các thư viện trước (xem phần Cài đặt)

## Build thành file .EXE

### ⭐ Cách 1: Build tự động trên GitHub (Không cần máy Windows!)

**Cách dễ nhất và miễn phí - Build .exe trên cloud:**

1. Tạo repository trên GitHub
2. Upload code lên GitHub (đã có sẵn file `.github/workflows/build_exe.yml`)
3. GitHub sẽ tự động build .exe trên Windows server
4. Tải file .exe từ tab **Actions** → **Artifacts**

**Xem hướng dẫn chi tiết:**

- `BUILD_AUTO.md` - Build tự động trên GitHub (không cần máy Windows)
- `HUONG_DAN_BUILD_EXE_CHI_TIET.md` - Hướng dẫn build chi tiết nhất (có máy Windows) ⭐

### Cách 2: Build trên Windows (Nếu có máy Windows)

Để chuyển đổi chương trình Python sang file .exe (chạy được mà không cần cài Python):

### Cách 1: Sử dụng file .bat (Dễ nhất)

1. **Double-click vào `build.bat`** - Sẽ tự động build
2. Hoặc chạy:
   - `build_console.bat` - Build với cửa sổ console
   - `build_windowed.bat` - Build không có console (chạy ngầm)

### Cách 2: Sử dụng Python script

```bash
python build_exe.py
```

### Cách 3: Build thủ công

```bash
# Cài đặt PyInstaller
pip install pyinstaller

# Build với console (xem được output) - KHUYẾN NGHỊ
pyinstaller --onefile --console --name Macro macro.py

# Hoặc build không có console (chạy ngầm)
pyinstaller --onefile --windowed --name Macro macro.py
```

**Lưu ý:** Tất cả tính năng đã được gộp vào file `macro.py` duy nhất!

Sau khi build xong, file `.exe` sẽ nằm trong thư mục `dist/`

**Lưu ý khi build:**

- File .exe có thể bị Windows Defender cảnh báo (false positive) - đây là bình thường
- Có thể cần chạy với quyền Administrator
- File .exe đầu tiên có thể chạy chậm (PyInstaller đang giải nén)

## Xử lý lỗi

Nếu gặp lỗi khi cài đặt hoặc chạy:

1. Đảm bảo đã cài đặt Python đúng cách
2. Chạy Command Prompt/Terminal với quyền Administrator
3. Kiểm tra firewall/antivirus có chặn không
4. Khi build exe, đảm bảo đã cài đặt tất cả dependencies
