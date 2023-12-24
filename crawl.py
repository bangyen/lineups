import argparse
import requests
import time
import bs4
import re

def pages(tree):
    css  = re.compile('pagination-page')
    page = tree.find_all('li', class_=css)

    last = page[-1]
    name = last.a.string
    return int(name.strip())


def soup(url):
    html = requests.get(url).text
    tree = bs4.BeautifulSoup(html, 'html.parser')

    time.sleep(1)
    return tree


def listeners(artist, page):
    url = (
        'https://www.last.fm/music/'
        f'{artist}/+listeners?page={page}'
    )

    return soup(url)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('artist')
    args  = parser.parse_args()

    name  = args.artist
    print(f'{name} Scrobbles')
    tree  = listeners(name, 1)
    end   = pages(tree)
    total = 0

    for k in range(end):
        if k: tree = listeners(name, k + 1)

        page = tree.find_all(
            'h3', class_='top-listeners-item-name'
        )

        for p in page:
            user = p.a.string
            link = (
                'https://www.last.fm/user/'
                f'{user}/library/music/{name}'
            )

            html = soup(link)
            meta = html.find_all(
                'p', class_='metadata-display'
            )

            val  = meta[0].string
            num  = int(val.replace(',', ''))
            print(f'{user.ljust(20)}: {num}')
            total += num

    print(f'Total: {total}')
