from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time


def capture_screenshot(url: str) -> str:
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    driver.get(url)
    timestamp = int(time.time())
    domain = url.replace('http://', '').replace('https://', '').replace('/', '_').replace(':', '_')
    filename = f"screenshots/{domain}_{timestamp}.png"
    driver.save_screenshot(filename)
    driver.quit()
    return filename
