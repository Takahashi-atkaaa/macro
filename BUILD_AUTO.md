# Cách Build .EXE Tự Động (Không cần máy Windows)

## Phương pháp 1: Sử dụng GitHub Actions (Khuyến nghị)

### Bước 1: Tạo repository trên GitHub

1. Đăng nhập vào [GitHub.com](https://github.com)
2. Tạo repository mới (ví dụ: `macro-windows`)
3. **KHÔNG** tích vào "Initialize with README" (vì đã có file rồi)

### Bước 2: Upload code lên GitHub

```bash
# Trong thư mục dự án
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/macro-windows.git
git push -u origin main
```

### Bước 3: Chờ build tự động

1. GitHub sẽ tự động build .exe trên Windows server
2. Vào tab **Actions** trong repository
3. Chọn workflow vừa chạy
4. Tải file **Macro-EXE** từ phần **Artifacts**

### Bước 4: Download file .exe

- File .exe sẽ có trong phần Artifacts
- Click vào để tải về

## Phương pháp 2: Sử dụng dịch vụ Cloud Windows

### Option A: AWS EC2 (Free tier có sẵn)

1. Đăng ký AWS (có free tier)
2. Tạo Windows EC2 instance
3. Kết nối qua RDP
4. Upload code và build

### Option B: Azure (Free trial)

1. Đăng ký Azure (có $200 credit miễn phí)
2. Tạo Windows VM
3. Kết nối và build

### Option C: Google Cloud (Free trial)

1. Đăng ký GCP (có $300 credit)
2. Tạo Windows VM
3. Kết nối và build

## Phương pháp 3: Nhờ người khác build

Gửi các file sau cho người có Windows:
- `macro.py`
- `requirements.txt`
- `build_console.bat`

Họ chỉ cần:
1. Double-click `build_console.bat`
2. Gửi lại file `dist\Macro.exe`

## Phương pháp 4: Sử dụng máy ảo Windows

1. Cài VirtualBox (miễn phí)
2. Download Windows 10 ISO (có thể dùng bản evaluation)
3. Cài Windows trên máy ảo
4. Build trong máy ảo

## So sánh các phương pháp:

| Phương pháp | Độ khó | Thời gian | Chi phí |
|------------|--------|----------|---------|
| GitHub Actions | ⭐ Dễ | 5-10 phút | Miễn phí |
| Cloud Windows | ⭐⭐ Trung bình | 30-60 phút | Miễn phí (trial) |
| Nhờ người khác | ⭐ Rất dễ | Tùy | Miễn phí |
| Máy ảo | ⭐⭐⭐ Khó | 2-3 giờ | Miễn phí |

**Khuyến nghị:** Dùng GitHub Actions - nhanh, dễ, miễn phí!

