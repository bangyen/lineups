import src.generate as generate
import src.collect  as collect
import sys
import os

def split(row):
    pair = row.split(maxsplit=1)
    key  = pair[0][:-1].lower()
    val  = pair[1]

    return key, val


def header(rows):
    pairs = {
        k:v for k,v in
        map(split, rows)
    }

    f, p, y, d =         \
        'fest', 'place', \
        'year', 'dates'

    fest  = pairs[f]
    year  = pairs[y]
    place = pairs[p]
    dates = pairs[d]

    year  = int(year)
    dates = dates.split(' – ')

    return {
        f:  fest,
        y:  year,
        p: (fest, p, place),
        d: (fest, d, dates)
    }


if __name__ == '__main__':
    args   = sys.argv
    name   = 'scripts/json.zlib'
    tables = generate.loads(name)

    search = collect.init(
        os.environ['PYLAST_API_KEY'],
        os.environ['PYLAST_API_SECRET'],
        tables
    )

    with open(args[1], encoding='utf-8') as file:
        lines = file.readlines()
        html  = [l.strip() for l in lines]
        start = html.index('')

        head  = html[:start]
        wrap  = header(head)
        names = html[start + 1:]

        collect.append(
            wrap,
            names,
            search,
            tables
        )

    generate.dumps(tables, name)
