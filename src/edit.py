import src.generate as generate
import src.collect  as collect
import os

def interact(tables):
    fest = artist = True
    year = bill   = ''
    res  = []

    while fest:
        fest = input('Festival: ')

        if fest not in tables.fests:
            continue

        while not year.isdigit():
            year = input('Year: ')

        while artist:
            artist = input('Artist: ')
            status = input('Headliner (y/n): ')

            if not status:
                break

            if status == '!redo':
                continue

            if status and status[0] == 'y':
                bill = 'Headliner'
            else:
                bill = 'Subheadliner'

            row = (artist, bill, fest, year)
            res.append(row)

    if res:
        billing(res, tables)


def billing(lines, tables):
    opts  = ('Headliner', 'Subheadliner')
    names = []

    for row in lines:
        if isinstance(row, str):
            args = row.rsplit(maxsplit=3)
        else:
            args = row

        a, b, f, y = args
        y = int(y)

        if a not in tables.artists:
            for n in tables.artists:
                same = collect.strdiff(a, n)

                if same > 0.9:
                    names.append((a, n))
                    a = n

        if b not in opts:
            exit(args)

        res = tables.get_set(
            fest=f,
            year=y,
            artist=a
        )

        res['bill'] = b

    size = max(len(t[1]) for t in names)

    for k, v in names:
        diff = ' ' * (size -len(k))
        print(f'{k}{diff}  ==>  {v}')


if __name__ == '__main__':
    folder = 'data/billing/'
    name   = 'scripts/json.zlib'
    tables = generate.loads(name)

    for path in os.listdir(folder):
        with open(folder + path) as file:
            lines = file.readlines()
            billing(lines, tables)

    interact(tables)
    generate.dumps(tables, name)
