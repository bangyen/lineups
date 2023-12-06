import src.classes as classes
import zlib
import json
import bs4

def loads(name):
    data = ''

    with open(name, 'rb') as file:
        comp = file.read()
        byte = zlib.decompress(comp)
        data = json.loads(byte)

    return classes.Database(data)


def dumps(tables, name):
    with open(name, 'wb') as file:
        data = tables.tables
        strs = json.dumps(data)
        byte = strs.encode()

        comp = zlib.compress(byte)
        file.write(comp)


def parse(html):
    css = {
        'old': 'yKMVIe',
        'new': 'PZPZlf',
        'loc': 'LrzXr kno-fv wHYlTd z8gr9e',
        'set': 'nxucXc CxwsZe'
    }

    soup  = bs4.BeautifulSoup(html, 'html.parser')
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
    dates = dates.split(' - ')

    wrap  = {
        'fest' : fest,
        'year' : int(year),
        'place': (fest, 'place', place),
        'dates': (fest, 'dates', dates)
    }

    return wrap, [s.string for s in names]
