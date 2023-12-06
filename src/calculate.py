import src.generate as generate
import prettytable  as pt

def percent(pred, tables, limit=7):
    genres = {}

    for s in tables.sets:
        if not pred(s):
            continue

        ind  = (s[1], 'main')
        main = tables.get_artist(ind)
        prev = genres.get(main, 0)

        genres[main] = prev + 1

    order = sorted(
        genres.items(),
        key=lambda t: -t[1] * bool(t[0])
    )

    total = sum(genres.values()) or 1
    rest  = sum(t[1] for t in order[limit:])

    order = [
        *order[:limit],
        ('Other', rest)
    ]

    return [
        (k, v / total * 100)
        for k,v in order
    ]


def table(title, data):
    def change(pos, char, junc=True):
        infix = '_junction' * junc
        attr  = f'{pos}{infix}_char'
        setattr(tab, attr, char)

    tab = pt.PrettyTable(
        ['genre', 'prcnt']
    )

    data = [
        (k, f'{v}%')
        for k,v in data
    ]

    change('bottom_right', '╯')
    change('bottom_left',  '╰')
    change('top_right',    '╮')
    change('top_left',     '╭')
    change('bottom',       '┴')
    change('top',          '┬')
    change('right',        '┤')
    change('left',         '├')
    change('horizontal',   '─', False)
    change('vertical',     '│', False)

    tab.align['genre'] = 'l'
    tab.align['prcnt'] = 'r'
    tab.padding_width  = 2
    tab.header = False
    tab.title  = title
    tab.add_rows(data)

    return tab


if __name__ == '__main__':
    year   = 2023
    name   = 'scripts/json.zlib'
    tables = generate.loads(name)

    for fest in tables.fests:
        def pred(s):
            return  s['fest'] == fest \
                and s['year'] == year

        genres = percent(pred, tables)[:-1]

        if len(genres) == 0:
            continue

        title = f'{fest} {year}'
        print(table(title, genres))
