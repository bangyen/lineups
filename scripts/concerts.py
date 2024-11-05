from src.scraper  import WebScraper
from src.database import Database
from tqdm         import tqdm

import dotenv
import time

ITEM = 'FestivalSetlistListItem-artist'

def create(item, fest):
    prev = item.previous_sibling
    name = fest['name']
    year = fest['year']
    text = prev.text

    if 'Add time' in text:
        time = None
    else:
        time = text

    return {
        'name': item.text,
        'year': int(year),
        'time': time,
        'fest': name
    }

def collect(fest):
    link = fest['_id']
    html = WebScraper(link)
    soup = html.create_soup()

    find = soup.find_all
    sets = find(class_=ITEM)

    return [
        create(item, fest)
        for item in sets
    ]

if __name__ == '__main__':
    dotenv.load_dotenv()

    fbase = Database('festivals')
    cbase = Database('concerts')
    find  = cbase.cache.find_one
    fests = fbase.find({})

    for fest in tqdm(fests):
        sets = collect(fest)
        time.sleep(5)

        if not sets:
            continue

        first = sets[0]
        match = find(first)

        if match:
            continue

        cbase.insert(sets)
