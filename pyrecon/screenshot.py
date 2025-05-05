from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os

def capture_screenshot(url: str) -> str:
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    driver.get(url)
    filename = f"screenshots/{url.replace('http://', '').replace('/', '_')}_{int(time.time())}.png"
    driver.save_screenshot(filename)
    driver.quit()
    return filename
