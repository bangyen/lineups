import src.generate as generate
import src.collect  as collect
import os

def billing(lines, tables):
    opts  = ('Headliner', 'Subheadliner')
    names = []

    for row in lines:
        args = row.rsplit(maxsplit=3)
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

    generate.dumps(tables, name)
