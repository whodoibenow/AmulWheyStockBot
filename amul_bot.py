import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telegram import Bot

# ==== CONFIG ====
PRODUCT_URL = "https://shop.amul.com/en/product/amul-whey-protein-32-g-or-pack-of-60-sachets"
PINCODE = "388120"
TELEGRAM_BOT_TOKEN = "7862695756:AAHfJlGRWXHlkKRiwfVw1f2r3Aj4QuhdFTo"
TELEGRAM_CHAT_ID = "5246794723"  # Get it after step below      # 🔁 Replace this
# ================

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def send_telegram_message(msg):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
        print("📩 Telegram message sent.")
    except Exception as e:
        print("❌ Telegram error:", e)

def check_availability():
    print("🔍 Checking stock...")
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    try:
        driver = webdriver.Chrome(service=Service("/usr/bin/chromedriver"), options=chrome_options)
        wait = WebDriverWait(driver, 15)
        driver.get(PRODUCT_URL)

        # Step 1: Wait for popup and enter pincode
        pincode_input = wait.until(EC.presence_of_element_located((By.ID, "search")))
        pincode_input.send_keys(PINCODE)
        time.sleep(1)

        # Step 2: Click on the pincode dropdown
        pin_option = wait.until(EC.element_to_be_clickable((By.XPATH, f"//p[@class='item-name text-dark mb-0 fw-semibold fs-6' and text()='{PINCODE}']")))
        pin_option.click()
        time.sleep(5)

        # Step 3: Check if 'Sold Out' exists
        if "SOLD OUT" in driver.page_source.upper():
            print("❌ Product is SOLD OUT.")
        else:
            print("✅ Product is AVAILABLE!")
            send_telegram_message(f"🎉 Product is AVAILABLE! Go buy it now:\n{PRODUCT_URL}")

    except Exception as e:
        print("⚠️ Error occurred:", e)

    finally:
        try:
            driver.quit()
        except:
            pass

# Loop every 60 seconds
while True:
    check_availability()
    time.sleep(60)
