# Chương trình Macro cho Windows

Chương trình macro đơn giản để ghi và phát lại các hành động bàn phím và chuột trên Windows.

## 🍃 Tool Tự Động Hái Chè GTV

**File mới:** `macro_auto.py` - Tool chuyên biệt cho tự động hóa lặp lại nhiều lần

**Cách chạy:** Double-click `CHAY_AUTO.bat`

**Tính năng:**
- ✅ Tự động phát macro với số lần lặp lớn (100, 1000, v.v.)
- ✅ Delay giữa các lần lặp
- ✅ Phím tắt tiện lợi (F9, F10, F11)
- ✅ Giao diện đơn giản, dễ sử dụng

## ✨ Tính năng

- ✅ **Tự động cài đặt thư viện** - Chỉ cần click và chạy
- ✅ Ghi lại các hành động bàn phím và chuột
- ✅ Phát lại macro đã ghi
- ✅ Lưu/tải macro từ file JSON
- ✅ Điều chỉnh tốc độ phát và số lần lặp
- ✅ **Giao diện GUI đẹp và dễ sử dụng** - Click chuột để điều khiển

## 🚀 Cách sử dụng (Cực kỳ đơn giản!)

### 📌 Cách chạy file .bat trên Windows:

**Cách 1: Double-click (Đơn giản nhất) ⭐**

1. Tìm file `.bat` (ví dụ: `CHAY_MACRO.bat`)
2. **Double-click** (nhấp đúp chuột) vào file
3. Xong!

**Cách 2: Right-click → Run as administrator (Khuyến nghị) ⭐**

1. **Right-click** (nhấp chuột phải) vào file `.bat`
2. Chọn **"Run as administrator"**
3. Nếu Windows hỏi, chọn **"Yes"**
4. Xong!

**Cách 3: Từ Command Prompt**

1. Mở Command Prompt (Win + R → gõ `cmd` → Enter)
2. Chuyển đến thư mục: `cd "đường-dẫn-đến-thư-mục"`
3. Gõ tên file: `CHAY_MACRO.bat`
4. Nhấn Enter

### 📋 Hướng dẫn từng bước:

#### Bước 1: Cài Python (nếu chưa có)

1. **Double-click** vào file `CAI_PYTHON.bat`
2. Script sẽ tự động:
   - ✅ Kiểm tra Python đã cài chưa
   - ✅ Nếu chưa có: Mở trang tải Python
   - ✅ Hướng dẫn cài đặt chi tiết

#### Bước 2: Chạy chương trình

1. **Double-click** vào file `CHAY_MACRO.bat`
2. Chương trình sẽ tự động:
   - ✅ Kiểm tra Python
   - ✅ Cài đặt Python libraries nếu chưa có
   - ✅ Khởi động menu điều khiển

**Không cần cài đặt gì thêm!**

## 📋 Yêu cầu

### Chỉ cần Python (nếu chưa có):

**Cách dễ nhất:** Double-click vào `CAI_PYTHON.bat` - Script sẽ hướng dẫn bạn!

**Hoặc cài thủ công:**

1. Tải Python từ: https://www.python.org/downloads/
2. **QUAN TRỌNG:** Khi cài, nhớ tích vào **"Add Python to PATH"**
3. Xong!

### ⚠️ Chạy với quyền Administrator (Khuyến nghị):

**Cách làm:**

1. **Right-click** (nhấp chuột phải) vào file `CHAY_MACRO.bat`
2. Chọn **"Run as administrator"**
3. Nếu Windows hỏi, chọn **"Yes"**

**Tại sao cần quyền Admin?**

- Để ghi/phát macro bàn phím và chuột
- Để cài đặt thư viện Python
- Tránh lỗi "Permission denied"

## 🎮 Giao diện điều khiển

**Giao diện GUI với các nút bấm:**

- **📹 Ghi Macro** - Bắt đầu ghi macro
- **⏹️ Dừng Ghi** - Dừng ghi macro
- **▶️ Phát Macro** - Phát macro đã ghi
- **⏸️ Dừng Phát** - Dừng phát macro
- **💾 Lưu Macro** - Lưu macro vào file
- **📂 Tải Macro** - Tải macro từ file
- **📋 Thông Tin** - Xem thông tin macro
- **🗑️ Xóa Macro** - Xóa macro hiện tại
- **⚙️ Cài Đặt** - Xem hướng dẫn

**Ưu điểm:**

- ✅ Click chuột để điều khiển (không cần gõ số)
- ✅ Hiển thị trạng thái real-time
- ✅ Nhật ký hoạt động
- ✅ Giao diện đẹp, dễ sử dụng

## 📖 Hướng dẫn sử dụng nhanh

### 1. Ghi macro:

- Click nút **"📹 Ghi Macro"**
- Thực hiện các hành động bạn muốn ghi
- Click nút **"⏹️ Dừng Ghi"** khi xong

### 2. Lưu macro:

- Click nút **"💾 Lưu Macro"**
- Chọn vị trí và tên file
- Click "Save"

### 3. Phát macro:

- Click nút **"▶️ Phát Macro"**
- Nhập số lần lặp (mặc định: 1)
- Nhập tốc độ (mặc định: 1.0 = bình thường)
- Click "Phát"

## 📁 Cấu trúc file

```
tapj nham/
  ├── CAI_PYTHON.bat    ← Cài Python (nếu chưa có) ⭐
  ├── CHAY_MACRO.bat    ← Chạy chương trình (GUI) ⭐
  ├── macro_gui.py      ← File chính với giao diện GUI
  ├── macro.py          ← File console (backup)
  └── README.md         ← File này
```

## ⚠️ Lưu ý

- Trên Windows, có thể cần chạy với quyền Administrator
- Macro được lưu dưới dạng JSON
- Thời gian giữa các sự kiện được ghi lại chính xác

## 🛠️ Xử lý lỗi

### ❌ Lỗi: "python is not recognized"

**Nguyên nhân:** Python chưa được cài hoặc chưa thêm vào PATH

**Giải pháp:**

1. Chạy file `CAI_PYTHON.bat` để cài Python
2. Hoặc cài thủ công từ: https://www.python.org/downloads/
3. **QUAN TRỌNG:** Tích vào "Add Python to PATH" khi cài

### ❌ Lỗi: "Permission denied" hoặc "Access denied"

**Nguyên nhân:** Chưa có quyền Administrator

**Giải pháp:**

1. **Right-click** vào file `.bat`
2. Chọn **"Run as administrator"**
3. Chọn **"Yes"** khi Windows hỏi

### ❌ Lỗi khi cài thư viện

**Nguyên nhân:** Thiếu quyền hoặc mất kết nối internet

**Giải pháp:**

1. Chạy với quyền Administrator (right-click → Run as administrator)
2. Kiểm tra kết nối internet
3. Thử lại

### ❌ File .bat không chạy được

**Nguyên nhân:** Windows bị chặn file .bat

**Giải pháp:**

1. **Right-click** vào file `.bat` → **Properties**
2. Nếu thấy "Unblock" → Tích vào đó
3. Click **OK**
4. Thử chạy lại

### ❌ Cửa sổ đóng ngay lập tức

**Nguyên nhân:** Có lỗi xảy ra

**Giải pháp:**

1. Mở Command Prompt (Win + R → `cmd`)
2. Kéo thả file `.bat` vào Command Prompt
3. Nhấn Enter
4. Xem thông báo lỗi để biết vấn đề

## 📝 License

Tự do sử dụng và chỉnh sửa.
