import json
import os
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from config import CONFIG
from services.instagram import Instagram

PROJ_DIR = Path(__file__).resolve().parent.parent

def _load_posts():
    with open(Path(CONFIG['cards_file']['path'])) as f:
        posts = json.loads(f.read())

    images_paths = []
    images_dir = str(Path(CONFIG['cards_file']['path']).parent)
    for file in os.listdir(images_dir):
        if file.lower().endswith('.jpg'):
            images_paths.append(Path(PROJ_DIR / images_dir).joinpath(file))
    
    return posts, images_paths

posts, images_paths = _load_posts()

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
    for i in range(len(posts)):
        print(f'Posting {posts[i]}')
        print(f'Image {images_paths[i]}')
        instagram.post(str(images_paths[i]), ', '.join(posts[i]['tags']))
finally:
    driver.quit()
