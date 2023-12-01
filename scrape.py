import difflib
import pylast
import bs4
import re

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
    soup = bs4.BeautifulSoup(
        html, 'html.parser'
    )

    span = soup.find_all(
        'span', class_='nxucXc CxwsZe'
    )

    return [s.string for s in span]


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

    def lookup(name):
        artist = network.get_artist(name)
        items  = artist.get_top_tags(limit=15)
        summ   = artist.get_bio('summary')
        corr   = artist.get_correction()
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

        if re.match(r'[^\n]+\n\n1', summ):
            alt = genres[:1]
        else:
            alt = genres

        return corr          , \
            best(alt)        , \
            f'woman: {woman}', \
            [t.name for t in genres]

    def backup(name):
        regex = re.compile(r'("[^"]+"|\([^()]+\))')
        paren = regex.sub('', name)

        results =                            \
            network.search_for_artist(paren) \
                   .get_next_page()

        items = [a.name for a in results]

        for match in items:
            artist = regex.sub('', match)

            if strdiff(paren, artist) > 0.9:
                return lookup(match)

        return name, [], None

    def search(name):
        res = lookup(name)
        time.sleep(DELAY)

        if (res := lookup(name))[1]:
            return res

        return backup(name)

    return search


if __name__ == '__main__':
    args   = sys.argv
    search = init(
        os.environ['PYLAST_API_KEY'],
        os.environ['PYLAST_API_SECRET']
    )


    if len(args) == 1:
        exit('Please supply a file.')

    if not os.path.exists(args[1]):
        exit('File not found.')

    with open(args[1], encoding='utf-8') as file:
        html  = file.read()
        names = parse(html)

        for n in names:
            print(*search(n), sep='\n\t')
            time.sleep(1)

        file.close()
