import src.generate as generate
import prettytable  as pt
import sys

def compare(loop, args, order):
    def inner(gen, arg, tables, **kwargs):
        out = []

        for val in loop(tables, arg):
            fest, year = args(arg, val)
            year = int(year)

            res = percent(
                lambda s: s['fest'] == fest \
                      and s['year'] == year,
                tables,
                **kwargs
            )

            if gen in res:
                out.append((val, res[gen]))

        return sorted(out, key=order)

    return inner


compare_fests \
    = compare(
        lambda t, a: t.fests,
        lambda a, v: (v, a),
        lambda t: -t[1]
    )


compare_years \
    = compare(
        lambda t, a: t.fests[a]['dates'],
        lambda a, v: (a, v.split()[-1]),
        lambda t: t[0]
    )


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


def overlap(
        main, year, tables,
        *fests, diff=True):
    def num(one, two):
        a = get(one)
        b = get(two)
        c = a & b

        div = len(b if diff else a)
        res = len(c) / div * 100

        return two, res, list(c)

    def get(fest):
        sets = tables.get_set(
            fest=fest,
            year=year
        )

        return {
            s['artist']
            for s in sets
        }

    return [
        num(main, f)
        for f in fests
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
        (k, f'{round(v, 1)}%')
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
    if len(args := sys.argv) < 3:
        exit('Missing argument.')

    genre  = args[1]
    const  = args[2]
    name   = 'scripts/json.zlib'
    tables = generate.loads(name)

    if const in tables.fests:
        func = compare_years
    elif const.isdigit():
        func = compare_fests

    output = func(
        genre, const, tables
    )

    data = table(
        (f'{genre.title()} '
         f'Music ({const})'),
        output
    )

    print(data)
