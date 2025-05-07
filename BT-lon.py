import schedule
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pytesseract
from PIL import Image, ImageOps, ImageFilter
from io import BytesIO

pytesseract.pytesseract.tesseract_cmd = r'C:\Python\checkphatnguoi\New folder\tesseract.exe'

def get_captcha_text(driver):
    try:
        captcha_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "imgCaptcha"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", captcha_element)

        location = captcha_element.location_once_scrolled_into_view
        size = captcha_element.size

        time.sleep(1.5)  # Đợi ảnh captcha hiển thị đầy đủ

        screenshot = driver.get_screenshot_as_png()
        img = Image.open(BytesIO(screenshot))

        left = int(location['x'])
        top = int(location['y'])
        right = int(location['x'] + size['width'])
        bottom = int(location['y'] + size['height'])

        captcha_img = img.crop((left, top, right, bottom))

        # Xử lý ảnh nâng cao
        captcha_img = captcha_img.convert("L")
        captcha_img = ImageOps.invert(captcha_img)
        captcha_img = captcha_img.filter(ImageFilter.MedianFilter())  # Khử nhiễu
        captcha_img = ImageOps.autocontrast(captcha_img)
        captcha_img = captcha_img.point(lambda x: 0 if x < 140 else 255, '1')
        captcha_img = captcha_img.resize((captcha_img.width * 3, captcha_img.height * 3), Image.LANCZOS)

        text = pytesseract.image_to_string(
            captcha_img,
            config='--psm 8 --oem 3 -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        ).strip().lower()

        text = ''.join(filter(str.isalnum, text))

        if 5 <= len(text) <= 6:
            print(f" OCR thành công: {text}")
            return text
        else:
            print(f"OCR thất bại: {text}")
            return None

    except Exception as e:
        print(f" Lỗi khi xử lý CAPTCHA: {e}")
        return None


def submit_form(driver, bien_so, loai_xe, captcha_text):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "BienKiemSoat"))).clear()
    driver.find_element(By.NAME, "BienKiemSoat").send_keys(bien_so)

    select_loai_xe = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "LoaiXe")))

    for option in select_loai_xe.find_elements(By.TAG_NAME, 'option'):
        if option.text.strip().lower() == loai_xe.strip().lower():
            option.click()
            break

    captcha_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "txt_captcha")))

    captcha_input.clear()
    captcha_input.send_keys(captcha_text)

    time.sleep(0.5)
    search_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Tra cứu')]"))
    )
    search_button.click()


def tra_cuu_phat_nguoi(bien_so, loai_xe):
    options = Options()
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    # Không dùng headless để kiểm tra dễ dàng hơn
    # options.add_argument('--headless')  
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.set_window_size(1200, 800)
    driver.get("https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html")

    try:
        attempts = 0
        while attempts < 10:
            attempts += 1
            print(f"\n Thử lần thứ {attempts}")

            captcha_text = get_captcha_text(driver)
            if not captcha_text:
                print(" Không nhận diện được captcha. Làm mới và thử lại...")
            else:
                submit_form(driver, bien_so, loai_xe, captcha_text)

                try:
                    result_box = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.ID, "bodyPrint123"))
                    )
                    content = result_box.text.strip()

                    if "Biển kiểm soát" in content and "Thời gian vi phạm" in content:
                        print(" Đã tìm thấy thông tin vi phạm:")
                        print(content)
                        return
                    else:
                        print("Không có dữ liệu hoặc CAPTCHA sai. Thử lại...")

                except Exception:
                    print(" Không tìm thấy phần tử kết quả. Có thể CAPTCHA sai.")

            # Làm mới captcha
            try:
                driver.find_element(By.ID, "btnRefreshCaptcha").click()
                time.sleep(1.2)
            except:
                pass

        print(" Không tra cứu được sau 10 lần thử.")

    finally:
        driver.quit()


# Thiết lập lịch chạy tự động vào 6h sáng và 12h trưa
import schedule

def job():
    tra_cuu_phat_nguoi("99A53457", "Ô tô")  # Thực hiện tra cứu

# Lịch chạy vào lúc 6h sáng và 12h trưa hàng ngày
schedule.every().day.at("06:00").do(job)
schedule.every().day.at("12:00").do(job)

# Kiểm tra công việc định kỳ
while True:
    schedule.run_pending()
    time.sleep(60)  # Kiểm tra mỗi phút
