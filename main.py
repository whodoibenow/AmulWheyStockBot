







from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import telegram
from selenium.common.exceptions import NoSuchElementException






# ====== CONFIGURATION ======
PRODUCT_URL = "https://shop.amul.com/en/product/amul-whey-protein-32-g-or-pack-of-60-sachets"  # Replace with actual product URL
PINCODE = "388120"
TELEGRAM_BOT_TOKEN = "7862695756:AAHfJlGRWXHlkKRiwfVw1f2r3Aj4QuhdFTo"
TELEGRAM_CHAT_ID = "5246794723"  # Get it after step below
# ============================

# Set up Telegram Bot
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

def send_telegram_message(msg):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)



def check_availability():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # ✅ Runs Chrome in background
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # ✅ Prevents crashes in container environments
    options.add_argument("--window-size=1920,1080")  # ✅ Ensures full layout rendering

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(PRODUCT_URL)

    wait = WebDriverWait(driver, 15)

    try:
        print("🔍 Waiting for PIN code input...")
        
        pincode_input = wait.until(EC.presence_of_element_located((By.ID, "search")))
        pincode_input.clear()
        pincode_input.send_keys(PINCODE)
        print("⌨️ PIN code entered...")

        print("⏳ Waiting for dropdown...")
        dropdown_option = wait.until(EC.element_to_be_clickable(
            (By.XPATH, f"//p[contains(@class,'item-name') and text()='{PINCODE}']")))
        dropdown_option.click()
        print("✅ Pincode selected.")

        time.sleep(5)

        try:
            sold_out_alert = driver.find_element(By.XPATH, "//div[contains(@class, 'alert-danger') and contains(text(), 'Sold Out')]")
            print("❌ Product is SOLD OUT.")
        except NoSuchElementException:
            print("✅ Product is AVAILABLE!")
            send_telegram_message("🎉 Product is AVAILABLE! Go buy it now!\n" + PRODUCT_URL)

    except Exception as e:
        print("❌ Error occurred:", e)

    finally:
        driver.quit()




# Run every 5 minutes (example)
if __name__ == "__main__":
    while True:
        check_availability()
        print("⏱️ Waiting 1 minute before next check...")
        time.sleep(60)  # 300 seconds = 5 minutes
