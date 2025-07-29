import os
import time
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import pytesseract

# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Config
INPUT_FILE = "urls.txt"
TEXT_DIR = "scraped_texts"
SCREENSHOT_DIR = "screenshots"
START_INDEX = 1
MAX_SCROLLS = 300
SCROLL_INCREMENT = 340
SCROLL_WAIT = 0.4  # 🔥 Faster scroll

os.makedirs(TEXT_DIR, exist_ok=True)
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# Chrome setup
options = Options()
# options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1200")
options.add_argument("--disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Read URL list
with open(INPUT_FILE, "r") as f:
    urls = [line.strip() for line in f if line.strip()]

# Start from the 1st
for idx, url in enumerate(urls[START_INDEX - 1:], START_INDEX):
    try:
        print(f"\n🔎 Opening #{idx}: {url}")
        try:
            driver.set_page_load_timeout(60)
            driver.get(url)
        except TimeoutException:
            print(f"⏳ Timeout loading {url}, skipping.")
            continue

        time.sleep(3)

        filename = f"{idx:03d}_scribd"
        text_path = os.path.join(TEXT_DIR, f"{filename}.txt")
        ocr_text = ""

        scroll_y = 0
        scroll_count = 0
        screenshot_count = 0
        same_scroll_count = 0
        last_scroll_height = 0

        while scroll_count < MAX_SCROLLS:
            driver.execute_script(f"window.scrollTo(0, {scroll_y});")
            time.sleep(SCROLL_WAIT)

            if scroll_count % 2 == 0:
                screenshot_path = os.path.join(SCREENSHOT_DIR, f"{filename}_part{screenshot_count}.png")
                driver.save_screenshot(screenshot_path)

                image = Image.open(screenshot_path)
                extracted = pytesseract.image_to_string(image)

                cleaned = re.sub(
                    r"(?i)(ssn|social security number)?[ \t]*[:\-]?[ \t]*(?:X{3}|\*{3})[- ]?(?:X{2}|\*{2})[- ]?(\d{4})",
                    r"SSN: XXX-XX-\2",
                    extracted,
                )
                ocr_text += cleaned + "\n"
                screenshot_count += 1

            scroll_y += SCROLL_INCREMENT
            scroll_count += 1

            # End detection
            current_height = driver.execute_script("return document.body.scrollHeight")
            viewport_height = driver.execute_script("return window.innerHeight")
            if scroll_y >= current_height + 2 * viewport_height:
                same_scroll_count += 1
            else:
                same_scroll_count = 0

            if same_scroll_count >= 5:
                print(f"🛑 Reached bottom at scroll #{scroll_count}")
                break

        with open(text_path, "w", encoding="utf-8") as f:
            f.write(ocr_text.strip())

        print(f"✅ Saved: {text_path}")
        time.sleep(3)

    except Exception as e:
        print(f"❌ Error with {url}: {e}")

driver.quit()
print("\n🎉 Done. Check scraped_texts/ for all output.")
