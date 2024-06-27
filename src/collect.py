import difflib
import pylast
import tqdm
import time
import re

CACHED_MIN = 0.9
SEARCH_MIN = 0.9
DELAY = 1

def strdiff(name, match):
    """
    Takes two string arguments, name and match, and
    returns a ratio indicating their similarity. The
    ratio is a float between 0 and 1, where 1 means
    the strings are identical and 0 means they are
    completely different.
    """
    return difflib.SequenceMatcher(
        None,
        name.lower(),
        match.lower()
    ).ratio()


def handler(func, val, **kwargs):
    """
    Waits for DELAY seconds, then calls func with
    kwargs. Returns func's result if successful,
    or val if an error occurs.
    """
    try:
        time.sleep(DELAY)
        return func(**kwargs)
    except pylast.PyLastError:
        return val


def memoize():
    """
    Returns a function that takes a list of tags and
    outputs the tag with the highest total count. The
    tag getInfo request is memoized to avoid repeated
    requests.
    """
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
    """
    Sets up a LastFM API connection, memoizes the tag
    getInfo request, and creates a search function that
    queries the LastFM database for artist info.

    The search function searches the cache and LastFM,
    handling name variations through normalization.
    """
    # Initialize LastFM API connection
    network = pylast.LastFMNetwork(
        api_key=key,
        api_secret=secret
    )

    cache = tables.artists
    best  = memoize()

    def lookup(name):
        # Check cache for match
        for key in cache:
            diff = strdiff(name, key)

            if diff > CACHED_MIN or name == key:
                return key, cache[key]

        # Search LastFM for artist
        res  = network.get_artist(name)
        corr = handler(res.get_correction, name)

        if corr in cache:
            return corr, cache[corr]

        # Extract artist info from LastFM response
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

        # Return artist info
        return corr, {
            'main'  : (t := best(alt)) and t.name,
            'genres': [t.name for t in genres],
            'woman' : woman
        }

    def backup(name):
        regex = re.compile(r'("[^"]+"|\([^()]+\))')
        paren = regex.sub('', name)

        # Search LastFM for similar artists
        results =                            \
            network.search_for_artist(paren) \
                   .get_next_page()

        for obj in results:
            match  = obj.name
            artist = regex.sub('', match)

            if strdiff(paren, artist) > SEARCH_MIN:
                return lookup(match)

        # Return empty result if no match found
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


def append(lineup, search, tables):
    """
    Searches for each artist in the names list, adds
    them to the database, and creates a lineup entry
    if not already present.
    """
    names = lineup.names
    fest  = lineup.fest
    year  = lineup.year
    empty = []

    args  = {
        'fest': fest,
        'year': year,
        'bill': 'undercard'
    }

    if entry := tables.get_set(args):
        return

    for n in tqdm.tqdm(names):
        c, g = search(n)
        tables.add_artist(c, g)

        args['artist'] = c
        tables.add_set(args)

        if not g['genres']:
            empty.append(c)

    plus = {
        'count': len(names)
    }

    if tables.get_fest(fest):
        for key, val in plus:
            val = plus[key]
            entry[key][year] = val
    else:
        for key in plus:
            val = plus[key]
            plus[key] = {year: val}

        tables.add_fest(fest, plus)

    for n in empty:
        print(f'Not Found: {n}')
