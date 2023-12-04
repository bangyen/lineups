import zlib
import json
import bs4

def loads(name):
    data = ''

    with open(name, 'rb') as file:
        comp = file.read()
        data = zlib.decompress(comp)

        file.close()

    return json.loads(data)


def dumps(tables, name):
    with open(name, 'wb') as file:
        data = json.dumps(tables)
        byte = data.encode()
        comp = zlib.compress(byte)

        file.write(comp)
        file.close()


def parse(html):
    css = {
        'old': 'yKMVIe',
        'new': 'PZPZlf ssJ7i xgAzOe',
        'loc': 'LrzXr kno-fv wHYlTd z8gr9e',
        'set': 'nxucXc CxwsZe'
    }

    soup  = bs4.BeautifulSoup(html, 'html.parser')
    names = soup.find_all('span', class_=css['set'])
    info  = soup.find_all('span', class_=css['loc'])

    old   = soup.find('span', class_=css['old'])
    new   = soup.find('div',  class_=css['new'])

    dates = place = ''
    fest  = (old or new).string \
                        .split()[1::-1]

    if info[0].a:
        if len(info) > 1:
            dates = info[1].string

        place = info[0].a.string
    else:
        if len(info) > 1:
            place = info[1].a.string

        dates = info[0].string

    return fest              , \
           place             , \
           dates.split(' – '), \
           [s.string for s in names]
