import src.generate as generate
import prettytable  as pt
import sys

def compare_fests(gen, year, tables, **kwargs):
    out = []

    for fest in tables.fests:
        res = percent(
            lambda s: s['fest'] == fest \
                  and s['year'] == year,
            tables,
            **kwargs
        )

        if gen in res:
            out.append((fest, res[gen]))

    return sorted(out, reverse=True)


def compare_years(gen, fest, tables, **kwargs):
    out = []

    for y in tables.fests[fest]['dates']:
        year = int(y.split()[-1])

        res = percent(
            lambda s: s['fest'] == fest \
                  and s['year'] == year,
            tables,
            **kwargs
        )

        if gen in res:
            out.append((year, res[gen]))

    return sorted(out, reverse=True)


def percent(pred, tables, limit=None):
    genres = {}

    for s in tables.sets:
        if not pred(s):
            continue

        ind  = (s['artist'], 'main')
        main = tables.get_artist(ind)
        prev = genres.get(main, 0)
        genres[main] = prev + 1

    order = sorted(
        genres.items(),
        key=lambda t: -t[1] * bool(t[0])
    )

    if limit is None:
        limit = len(order) - 1

    total = sum(genres.values()) or 1
    rest  = sum(t[1] for t in order[limit:])

    order = [
        *order[:limit],
        ('Other', rest)
    ]

    return {
        k:(v / total * 100)
        for k,v in order
    }


def table(title, data):
    def change(pos, char, junc=True):
        infix = '_junction' * junc
        attr  = f'{pos}{infix}_char'
        setattr(tab, attr, char)

    tab = pt.PrettyTable(
        ['genre', 'prcnt']
    )

    data = [
        (k, f'{round(v)}%')
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
    if len(args := sys.argv) == 1:
        exit('Missing argument.')

    genre  = 'electronic'
    const  = args[1]
    name   = 'scripts/json.zlib'
    tables = generate.loads(name)

    output = compare_years(
        genre, const, tables
    )

    data = table(
        (f'{genre.title()} '
         f'Music ({const})'),
        output
    )

    print(data)
