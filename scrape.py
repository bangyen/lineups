from   spotipy.oauth2  import SpotifyClientCredentials
from   bs4             import BeautifulSoup
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
    return [str(s.string) for s in span]


def search(name):
    results = spotify.search(
        q='artist:' + name,
        type='artist',
        limit=10
    )

    items = results['artists']['items']
    lower = name.lower()

    for artist in items:
        match = artist['name']

        if match.lower() == lower:
            return match, artist['genres']

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
            print(search(n))

        file.close()
