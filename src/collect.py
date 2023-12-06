import src.generate as generate
import time

import difflib
import pylast
import re

DELAY = 1

def strdiff(name, match):
    return difflib.SequenceMatcher(
        None,
        name.lower(),
        match.lower()
    ).ratio()


def handler(func, val, **kwargs):
    try:
        time.sleep(DELAY)
        return func(**kwargs)
    except pylast.PyLastError:
        return val


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


def init(key, secret, tables):
    network = pylast.LastFMNetwork(
        api_key=key,
        api_secret=secret
    )

    cache = tables.artists
    best  = memoize()

    def lookup(name):
        if name in cache:
            return name, cache[name]

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
            if  t.name != 'USA'
            and t.name != 'seen live'
            and 'female' not in t.name
        ][:5]

        mat = re.match(r'[^\n]+\n\n1', summ)
        alt = genres[:1] if mat else genres

        return corr, {
            'main'  : (t := best(alt)) and t.name,
            'genres': [t.name for t in genres],
            'woman' : woman
        }

    def backup(name):
        regex = re.compile(r'("[^"]+"|\([^()]+\))')
        paren = regex.sub('', name)

        results =                            \
            network.search_for_artist(paren) \
                   .get_next_page()

        for obj in results:
            match  = obj.name
            artist = regex.sub('', match)

            if strdiff(paren, artist) > 0.9:
                return lookup(match)

        return name, {
            'main'  : None,
            'genres': [],
            'woman' : None
        }

    def search(name):
        res = lookup(name)

        if res[1]['main']:
            return res

        return backup(name)

    return search


def append(html, search, tables):
    wrap, names = generate.parse(html)

    tables.add_fest(wrap['place'])
    tables.add_fest(wrap['dates'])

    for n in names:
        c, g = search(n)
        tables.add_artist((c, g))

        tables.add_set(
            fest   = wrap['fest'],
            year   = wrap['year'],
            bill   = 'Undercard',
            artist = c
        )

        if not g['genres']:
            print(f'Not Found: {c}')
