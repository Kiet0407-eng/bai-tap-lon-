
# **Dự án Tra Cứu Phạt Nguội - CSGT.vn**

## **Mục Lục**
1. [Giới thiệu](#giới-thiệu)
2. [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
3. [Cài Đặt](#cài-đặt)
4. [Hướng Dẫn Sử Dụng](#hướng-dẫn-sử-dụng)
5. [Cách Hoạt Động](#cách-hoạt-động)
6. [Lỗi Thường Gặp](#lỗi-thường-gặp)
7. [Giới Thiệu Về Các Thư Viện](#giới-thiệu-về-các-thư-viện)
8. [Liên Hệ](#liên-hệ)

---

## **Giới Thiệu**

Dự án này nhằm mục đích tự động tra cứu **phạt nguội** trên trang web của CSGT (Cảnh Sát Giao Thông) từ biển số xe và loại phương tiện. Chương trình sử dụng Selenium để tự động hóa việc tra cứu, nhận diện **mã CAPTCHA** bằng công nghệ OCR (Tesseract), và xuất ra thông tin vi phạm nếu có.

---

## **Yêu Cầu Hệ Thống**

Để chạy dự án này, bạn cần cài đặt các yêu cầu sau:

- **Python 3.x** trở lên
- **Tesseract OCR** (Cài đặt trên máy tính)
- **Trình duyệt Google Chrome** và **Chromedriver**

Các thư viện Python cần cài đặt:
- **Selenium**: Để tự động hóa tương tác với trang web.
- **Pillow**: Để xử lý ảnh (dùng cho OCR).
- **pytesseract**: Để nhận diện văn bản từ ảnh (sử dụng OCR).
- **requests**: Để tải ảnh CAPTCHA từ URL.
- **webdriver-manager**: Để tự động tải và quản lý Chromedriver.

---

## **Cài Đặt**

### **Cài Đặt Python và Thư Viện**
1. Cài đặt **Python**: [Link tải Python](https://www.python.org/downloads/)
2. Cài đặt các thư viện cần thiết bằng `pip`:
```bash
pip install selenium pillow pytesseract requests webdriver-manager
```

### **Cài Đặt Tesseract OCR**
- Tải Tesseract OCR từ [GitHub](https://github.com/tesseract-ocr/tesseract).
- Cài đặt Tesseract và đặt đường dẫn tới tesseract.exe trong code như sau:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Python\checkphatnguoi\New folder\tesseract.exe'
```
Hãy thay đổi đường dẫn phù hợp với nơi bạn đã cài đặt Tesseract.

### **Cài Đặt Google Chrome và Chromedriver**
1. Cài đặt **Google Chrome** từ trang chính thức: [Google Chrome](https://www.google.com/chrome/)
2. Tải **Chromedriver** tương ứng với phiên bản Chrome của bạn từ [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/).
3. Hoặc sử dụng `webdriver-manager` như trong code để tự động tải Chromedriver.

---

## **Hướng Dẫn Sử Dụng**

1. **Tải Dự Án**: Tải hoặc sao chép mã nguồn từ dự án của bạn.
2. **Cập nhật Biển Số Xe và Loại Phương Tiện**: Mở file `BT-lon.py` và thay đổi biển số xe cũng như loại phương tiện tại dòng dưới:
```python
tra_cuu_phat_nguoi("99A53457", "Ô tô")  # Thay đổi biển số và loại phương tiện
```
3. **Chạy Mã**: Mở terminal hoặc command prompt và chạy:
```bash
python BT-lon.py
```
4. **Kết Quả**: Sau khi chương trình chạy, bạn sẽ thấy thông tin phạt nguội (nếu có) được in ra trong terminal.
5. lịch chạy 6h sáng và 12h trưa hằng ngày

---

## **Cách Hoạt Động**

### **Các bước hoạt động của chương trình:**

1. **Mở trang web CSGT.vn**: Mở trang tra cứu phạt nguội của CSGT tại địa chỉ [https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.htm](https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.htm).
2. **Nhập Biển Số Xe và Loại Phương Tiện**: Chương trình tự động nhập biển số xe và loại phương tiện (Ví dụ: Ô tô, Xe máy).
3. **Trích xuất và Nhận Diện CAPTCHA**: Sử dụng **Tesseract OCR** để nhận diện mã CAPTCHA từ ảnh và tự động nhập vào form.
4. **Tìm kiếm và Kiểm Tra Kết Quả**: Chương trình bấm nút "Tra cứu" và kiểm tra kết quả.
5. **Lặp lại nếu cần**: Nếu CAPTCHA không nhận diện được, chương trình sẽ thử lại 10 lần.

### **Làm Mới CAPTCHA**:
Nếu không nhận diện được CAPTCHA hoặc không có kết quả phạt, chương trình sẽ tự động làm mới CAPTCHA và thử lại.

---

## **Lỗi Thường Gặp**

### **1. Không nhận diện được CAPTCHA**
- **Nguyên nhân**: Đôi khi, Tesseract OCR không nhận diện được nếu CAPTCHA quá phức tạp.
- **Giải pháp**: Chạy lại và kiểm tra kết nối internet. Nếu vẫn lỗi, thử làm mới CAPTCHA bằng cách nhấn vào nút "Làm mới CAPTCHA" trên trang.

### **2. Lỗi không tìm thấy `tesseract.exe`**
- **Nguyên nhân**: Đường dẫn tới `tesseract.exe` không chính xác.
- **Giải pháp**: Cập nhật lại đường dẫn tới Tesseract trong mã nguồn.
```python
pytesseract.pytesseract.tesseract_cmd = r'ĐƯỜNG_DẪN_TỚI_TESSERACT.EXE'
```

---

## **Giới Thiệu Về Các Thư Viện**

1. **Selenium**: Thư viện giúp tự động hóa các tác vụ trên trình duyệt web. Trong dự án này, Selenium dùng để mở trang web và tương tác với các phần tử.
2. **pytesseract**: Thư viện Python để nhận diện văn bản từ ảnh thông qua Tesseract OCR.
3. **Pillow**: Thư viện xử lý ảnh, giúp tiền xử lý ảnh trước khi đưa vào Tesseract để nhận diện.
4. **requests**: Dùng để tải ảnh CAPTCHA từ URL.
5. **webdriver-manager**: Tự động tải và cập nhật phiên bản Chromedriver phù hợp.

---




