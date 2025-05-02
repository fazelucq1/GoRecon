from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os

def capture_screenshot(url: str) -> str:
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1920, 1080)
    driver.get(url)
    filename = f"screenshot_{int(time.time())}.png"
    path = os.path.join(os.getcwd(), filename)
    driver.save_screenshot(path)
    driver.quit()
    return path
