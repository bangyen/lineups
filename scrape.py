import difflib
import pylast
import bs4
import re

import save
import time
import sys
import os

DELAY = 1

def strdiff(name, match):
    return difflib.SequenceMatcher(
        None,
        name.lower(),
        match.lower()
    ).ratio()


def parse(html):
    css = {
        'old': 'yKMVIe',
        'new': 'PZPZlf ssJ7i xgAzOe',
        'loc': 'LrzXr kno-fv wHYlTd z8gr9e',
        'set': 'nxucXc CxwsZe'
    }

    soup  = bs4.BeautifulSoup(html, 'html.parser')
    names = soup.find_all('span', class_=css['set'])
    info  = soup.find_all('span', class_=css['loc'])
    old   = soup.find('span', class_=css['old'])
    new   = soup.find('div',  class_=css['new'])

    dates = info[1] if info[0].a else info[0]
    place = info[0] if info[0].a else info[1]
    fest  = old or new

    return fest.string.split()[1::-1], \
           dates.string.split(' – ') , \
           place.a.string            , \
           [s.string for s in names]


def memoize():
    cache = {}

    def total(tag):
        if (name := tag.name) not in cache:
            req = tag._request('tag.getInfo', True)
            ext = pylast._extract(req, 'total')

            cache[name] = pylast._number(ext)
            time.sleep(DELAY)

        return cache[name]

    def best(tags):
        res = (None, 0)

        for t in tags:
            tot = total(t)

            if tot > res[1]:
                res = (t, tot)

            if tot > 750_000:
                break

        return res[0]

    return best


def handler(func, val, **kwargs):
    try:
        time.sleep(DELAY)
        return func(**kwargs)
    except pylast.PyLastError:
        return val


def init(key, secret):
    network = pylast.LastFMNetwork(
        api_key=key,
        api_secret=secret
    )

    best = memoize()

    def lookup(name, cache):
        res  = network.get_artist(name)
        corr = handler(res.get_correction, name)

        if corr in cache:
            return corr, cache[corr]

        summ   = handler(res.get_bio_summary, '')
        items  = handler(res.get_top_tags, [], limit=15)
        tags   = [t.item for t in items]

        woman  = any(
            'female' in t.name
            for t in tags
        )

        genres = [
            t for t in tags
            if  t.name != 'seen live'
            and 'female' not in t.name
        ][:5]

        mat = re.match(r'[^\n]+\n\n1', summ)
        alt = genres[:1] if mat else genres

        return corr, {
            'main'  : (t := best(alt)) and t.name,
            'genres': [t.name for t in genres],
            'woman' : woman
        }

    def backup(name, cache):
        regex = re.compile(r'("[^"]+"|\([^()]+\))')
        paren = regex.sub('', name)

        results =                            \
            network.search_for_artist(paren) \
                   .get_next_page()

        items = [a.name for a in results]

        for match in items:
            artist = regex.sub('', match)

            if strdiff(paren, artist) > 0.9:
                return lookup(match, cache)

        return name, {
            'main'  : None,
            'genres': [],
            'woman' : None
        }

    def search(name, cache):
        res = lookup(name, cache)

        if res[1]['main']:
            return res

        return backup(name, cache)

    return search


if __name__ == '__main__':
    args   = sys.argv
    name   = 'info.json'
    fests, artists, sets \
           = save.loads(name)

    search = init(
        os.environ['PYLAST_API_KEY'],
        os.environ['PYLAST_API_SECRET']
    )

    if len(args) == 1:
        exit('Please supply a file.')

    if not os.path.exists(args[1]):
        exit('File not found.')

    with open(args[1], encoding='utf-8') as file:
        html = file.read()
        [f, y], d, p, n = parse(html)

        if f not in fests:
            fests[f] = {
                'place': p,
                'dates': {}
            }

        dates = fests[f]['dates']
        year  = int(y)

        if year not in dates:
            dates[year] = d

        for a in n:
            c, g = search(a, artists)
            tup  = (f, c, year)
            sets.append(tup)

            if c not in artists:
                artists[c] = g

                if not g['genres']:
                    print(f'Not Found: {c}')

        file.close()

    save.dumps(tables, name)
