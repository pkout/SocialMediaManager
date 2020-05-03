import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import CONFIG
from services.instagram import Instagram

PROJ_DIR = Path(__file__).resolve().parent.parent

mobile_emulation = {
    'deviceMetrics': {'width': 360, 'height': 640, 'pixelRatio': 3.0},
    'userAgent': 'Mozilla/5.0 (Linux; Android 4.2.1; en-us; '
                 'Nexus 5 Build/JOP40D) AppleWebKit/535.19 '
                 '(KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19'
}

chrome_options = Options()
chrome_options.add_experimental_option('mobileEmulation', mobile_emulation)
driver = webdriver.Chrome(options = chrome_options)

try: 
    instagram = Instagram(driver=driver)

    instagram.login(CONFIG['instagram']['username'], CONFIG['instagram']['password'])
    instagram.skip_initial_popups()
    instagram.post(str(Path(PROJ_DIR, 'posts', 'agar.jpg')), 'my post text')
finally:
    driver.quit()