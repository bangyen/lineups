import pylast
import bs4

import time
import sys
import os

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

    def search(name, sub=False):
        artist = network.get_artist(name)
        items  = artist.get_top_tags(limit=5)
        corr   = artist.get_correction()
        tags   = [t.item.name for t in items]

        return name, corr, tags

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
