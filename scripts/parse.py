import bs4
import re

def split(row):
    pair = row.split(maxsplit=1)
    key  = pair[0][:-1].lower()
    val  = pair[1]

    return key, val


def text(data):
    start = data.index('')
    head  = data[:start]
    body  = data[start + 1:]
    names = [r for r in body if r]

    pairs = {
        k:v for k,v in
        map(split, head)
    }

    f, p, y, d =         \
        'fest', 'place', \
        'year', 'dates'

    fest  = pairs[f]
    year  = pairs[y]
    place = pairs[p]
    dates = re.sub(
        r', \d{4}',
        '', pairs[d]
    )

    wrap  = {
        f: fest,
        y: int(year),
        p: (fest, p,       place),
        d: (fest, d, year, dates)
    }

    return wrap, names


def html(data):
    css = {
        'old': 'yKMVIe',
        'new': 'PZPZlf',
        'loc': 'LrzXr kno-fv wHYlTd z8gr9e',
        'set': 'nxucXc CxwsZe'
    }

    soup  = bs4.BeautifulSoup(data, 'html.parser')
    names = soup.find_all('span', class_=css['set'])
    info  = soup.find_all('span', class_=css['loc'])

    old   = soup.find('span', class_=css['old'])
    new   = soup.find('div',  class_=css['new'])

    title = (old or new).string.split()
    dates = place = ''

    if info[0].a:
        if len(info) > 1:
            dates = info[1].string

        place = info[0].a.string
    else:
        if len(info) > 1:
            place = info[1].a.string

        dates = info[0].string

    fest  = next(filter(str.isalpha, title))
    year  = next(filter(str.isdigit, title))
    dates = re.sub(
        r', \d{4}',
        '', dates
    )

    wrap  = {
        'fest' : fest,
        'year' : int(year),
        'place': (fest, 'place',       place),
        'dates': (fest, 'dates', year, dates)
    }

    return wrap, [s.string for s in names]
