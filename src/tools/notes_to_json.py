import json
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from config import CONFIG

PROJ_DIR = Path(__file__).resolve().parent.parent.parent
CARDS_FILE_PATH = PROJ_DIR.joinpath(CONFIG['cards_file']['path'])

html = requests.get(CONFIG['scrape_webpage']['url'])

skip = True
cards_json = []
soup = BeautifulSoup(html.text, 'html.parser')
cards = soup.find_all('fieldset')
for card in cards:
    image_tag = card.find('img')
    tags = [f'#{t.strip()}' for t in card.find('span', class_='tags').get_text().split(',')]
    image_url = image_tag['src'] if image_tag is not None else None
    if image_url == '/learning/virology/images/helical-symmetry.jpg':
        skip = False
    if not skip:
        cards_json.append({
            'tags': tags,
            'image_url': image_url
        })
print(json.dumps(cards_json, indent=4))
with open(CARDS_FILE_PATH, 'w') as f:
    f.write(json.dumps(cards_json, indent=4))

print('\nScrape complete!')
