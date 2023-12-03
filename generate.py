import json

def loads(name):
    data = ''

    with open(name) as file:
        data = file.read()
        file.close()

    return json.loads(data)


def dumps(tables, name):
    with open(name, 'w') as file:
        data = json.dumps(
            tables,
            sort_keys=True,
            indent=4
        )

        file.write(data)
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

    dates = info[1] if info[0].a else info[0]
    place = info[0] if info[0].a else info[1]
    fest  = old or new

    return fest.string.split()[1::-1], \
           dates.string.split(' – ') , \
           place.a.string            , \
           [s.string for s in names]
