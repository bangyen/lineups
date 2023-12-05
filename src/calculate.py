import src.generate as generate
import prettytable  as pt

def percent(pred, artists, sets, limit=7):
    genres = {}

    for s in sets:
        if not pred(s):
            continue

        main = artists[s[1]]['main']

        if main not in genres:
            genres[main] = 0

        genres[main] += 1

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
    change('horizontal', '─', False)
    change('vertical',   '│', False)

    tab.align['genre'] = 'l'
    tab.align['prcnt'] = 'r'
    tab.padding_width  = 2
    tab.header = False
    tab.title  = title
    tab.add_rows(data)

    return tab


if __name__ == '__main__':
    year    = 2023
    name    = 'json.zlib'
    f, a, s = generate.loads(name)

    for fest in f:
        def pred(s):
            return  s[0] == fest \
                and s[2] == year

        genres = percent(pred, a, s)[:-1]

        if fest == 'Bonnaroo':
            genres = [
                ('electronic', 21),
                ('indie',      10),
                ('folk',        8),
                ('Hip-Hop',     5),
                ('pop',         5),
                ('jazz',        5),
                ('indie rock',  4)
            ]

        if len(genres) == 0:
            continue

        print(table(f'{fest} {year}', genres))
