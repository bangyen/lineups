from   spotipy.oauth2  import SpotifyClientCredentials
from   difflib         import SequenceMatcher
from   bs4             import BeautifulSoup
import spotipy
import sys
import os
import re

spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials()
)


def subset(s1, s2, acc=''):
    if not s1:
        return False

    if s1 in s2 and acc in s2:
        return True

    return subset(
        s1[:-1], s2, s1[-1]
    )


def parse(html):
    soup = BeautifulSoup(
        html, 'html.parser'
    )

    span = soup.find_all(
        'span', class_='nxucXc CxwsZe'
    )

    return [str(s.string) for s in span]


def search(name, sub=False):
    results = spotify.search(
        q='artist:' + name,
        type='artist'
    )

    items = results['artists']['items']

    for artist in items:
        match = artist['name']

        ratio = SequenceMatcher(
            None,
            name.lower(),
            match.lower()
        ).ratio()

        genre = (match, artist['genres'])

        if ratio > 0.9:
            return genre

        if sub:
            b1 = subset(name, match)
            b2 = subset(match, name)

            if b1 or b2:
                return genre


def find(name):
    apost = search(name.replace("'", ''))
    paren = search(re.sub('\([^()]+\)$', '', name))
    acron = search (''.join(w[0] for w in name.split()))
    match = apost or paren or acron

    if match:
        return match

    if m := search(name, True):
        return m

    return name, []


if __name__ == '__main__':
    args = sys.argv
    res  = []

    if len(args) == 1:
        exit('Please supply a file.')

    if not os.path.exists(args[1]):
        exit('File not found.')

    with open(args[1], encoding='utf-8') as file:
        html  = file.read()
        names = parse(html)

        for n in names:
            print(*find(n))

        file.close()
