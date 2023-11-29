from   spotipy.oauth2  import SpotifyClientCredentials
from   bs4             import BeautifulSoup
from   multiprocessing import Pool
import spotipy
import sys
import os

spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials()
)

def parse(html):
    soup = BeautifulSoup(html, 'html.parser')

    if not soup.find('span', class_='b0Xfjd', string='Lineup'):
        return

    span = soup.find_all('span', class_='nxucXc CxwsZe')
    return [s.string for s in span]


def search(name):
    results = spotify.search(
        q='artist:' + name,
        type='artist'
    )

    items = results['artists']['items']

    if len(items) == 0:
        return

    artist = items[0]
    return artist['name'], artist['genres']


if __name__ == '__main__':
    args = sys.argv
    pool = Pool()
    res  = []

    if len(args) == 1:
        exit('Please supply a file.')

    if not os.path.exists(args[1]):
        exit('File not found.')

    with open(args[1], encoding='utf-8') as file:
        html = file.read()
        res  = pool.map(search, html)

        for n in html:
            proc = pool.apply_async(search, [n])
            res.append(proc)

        for p in res:
            t = p.get(timeout=10)
            print(t)

        file.close()
