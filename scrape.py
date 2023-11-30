import spotipy.oauth2 as oauth2
import spotipy
import difflib
import pylast
import bs4
import re

import time
import sys
import os

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

    return [str(s.string) for s in span]


def init(key, secret):
    network = pylast.LastFMNetwork(
        api_key=key,
        api_secret=secret
    )

    spotify = spotipy.Spotify(
        auth_manager=oauth2. \
            SpotifyClientCredentials()
    )

    def lookup(name):
        artist = network.get_artist(name)
        items  = artist.get_top_tags(limit=10)
        corr   = artist.get_correction()

        tags   = [t.item.name for t in items]
        top    = [
            t for t in tags
            if t != 'seen live'
        ]

        return corr, top[:5]

    def backup(name):
        paren = re.sub(r'\([^()]+\)$', '', name)

        results = spotify.search(
            q=f'artist:{paren}',
            type='artist'
        )

        items = results['artists']['items']

        for artist in items:
            match = artist['name']

            if all(s in match for s in name.split()) or \
               all(s in name for s in match.split()) or \
                    strdiff(name , match) > 0.9      or \
                    strdiff(paren, match) > 0.9:
                return match, artist['genres']

        return name, []

    def search(name):
        res = lookup(name)

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
            print(*search(n))
            time.sleep(1)

        file.close()
