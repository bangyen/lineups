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


def init(key, secret):
    network = pylast.LastFMNetwork(
        api_key=key,
        api_secret=secret
    )

    best = memoize()

    def lookup(name, cache):
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


def append(html, search, tables):
    fests, artists, sets = tables
    [f, y], p, d, n = generate.parse(html)

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

        if c not in sets:
            sets[c] = {}

        if year not in sets[c]:
            sets[c][year] = {}

        sets[c][year][f] = 'Undercard'

        if c not in artists:
            artists[c] = g

            if not g['genres']:
                print(f'Not Found: {c}')
