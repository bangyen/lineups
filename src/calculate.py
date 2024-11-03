import prettytable as pt

def compare(loop, args, order):
    """
    Generates a comparison function for festival
    data. It takes a loop function to iterate over
    the data, an args function to extract relevant
    information, and an order function to sort the
    results.
    """
    def inner(gen, arg, tables, **kwargs):
        out = []

        for val in loop(tables, arg):
            fest, year = args(arg, val)
            year = int(year)

            res = tally(
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


def tally(pred, tables, limit=None):
    """
    Tallies artist occurrences in a table, filtered
    by a predicate. It returns a dictionary with
    artists and their percentages, limited to a
    specified number, with the rest grouped as "Other".
    """
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
        main, fests,
        year, tables,
        diff=True):
    """
    Calculates the overlap between a main festival
    and a list of other festivals, returning a list
    of tuples containing the festival name, overlap
    percentage, and overlapping artists.
    """
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


def table(columns):
    """
    Creates a PrettyTable object with custom
    settings. It takes column names as inputs
    and customizes the appearance of the table's
    borders and padding. 
    """
    def change(pos, char, junc=True):
        infix = '_junction' * junc
        attr  = f'{pos}{infix}_char'
        setattr(tab, attr, char)

    tab = pt.PrettyTable(columns)

    tab.junction_char = '┼'
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

    tab.padding_width = 2
    tab.header = False

    return tab


def percent(title, data):
    """
    Takes a title and data as inputs, rounds the
    values to one decimal place, and formats them
    as percentages.
    """
    tab = table(
        'genre',
        'value'
    )

    fmt = [
        (k, f'{round(v, 1)}%')
        for k,v in data
    ]

    tab.align['genre'] = 'l'
    tab.align['value'] = 'r'
    tab.add_rows(fmt)
    tab.title = title

    return tab
