from src.database import Database
from tqdm         import tqdm

import pylast
import dotenv
import time
import os

DELAY = 1

class TagParser:
    remove = ['seen live', 'usa']
    limit  = 10

    def __init__(self, client):
        self.select = TagSelector(client)
        self.client = client

    def fetch(self, name):
        client = self.client
        limit  = self.limit

        artist = client.get_artist(name)
        finder = artist.get_top_tags

        time.sleep(DELAY)

        try:
            return finder(limit=limit)
        except pylast.PyLastError:
            return []

    def parse(self, tags):
        remove = self.remove
        result = []

        for tag in tags:
            item = tag.item
            name = item.name
            diff = name.lower()

            if diff in remove:
                continue

            if 'female' in diff:
                continue

            result.append(item)

        return result

    def query(self, name):
        items = self.fetch(name)
        tags  = self.parse(items)

        names = [t.name for t in tags][:5]
        main  = self.select.choose(tags)

        return {
            '_id':  name,
            'main': main,
            'tags': names
        }


class TagSelector:
    score = 750_000

    def __init__(self, client):
        self.client = client
        self.cache = {}

    def query(self, tag):
        cache = self.cache
        name  = tag.name

        if name in cache:
            return cache[name]

        request = tag._request('tag.getInfo', True)
        extract = pylast._extract(request, 'total')
        number  = pylast._number(extract)

        cache[name] = number
        time.sleep(DELAY)

        return number

    def choose(self, tags):
        if not tags:
            return None

        best = tags[0]
        find = self.query

        for tag in tags:
            old = find(best)
            new = find(tag)

            if new > self.score:
                return tag.name

            if new > old:
                best = tag

        return best.name

if __name__ == '__main__':
    dotenv.load_dotenv()

    apikey = os.getenv('PYLAST_API_KEY')
    secret = os.getenv('PYLAST_API_SECRET')

    client = pylast.LastFMNetwork(
        api_key=apikey,
        api_secret=secret
    )

    cbase = Database('concerts')
    abase = Database('artists')
    parse = TagParser(client)

    objs = cbase.find({})
    find = abase.find

    names = [obj['name'] for obj in objs]
    found = find({'_id': {'$nin': names}})

    data = []
    done = []

    for obj in tqdm(found):
        name = obj['name']
        same = find({'_id': name})

        if same:
            continue

        if name in done:
            continue

        tags = parse.query(name)

        done.append(name)
        data.append(tags)

        if len(data) == 100:
            abase.insert(data)
            data = []

    abase.insert(data)
