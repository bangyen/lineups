import src.generate as generate
import src.collect  as collect
import os

def lookup(pred, cache):
    for val in cache:
        if not pred(val, cache):
            continue

        c, g = search(val, {})
        cache[c] = g

        if c != val:
            del cache[val]


def replace(pred, repl, cache):
    for val in cache:
        if not pred(val, cache):
            continue

        cache[val] \
            = repl(val, cache)


def billing(lines, tables):
    res = {}

    def update(v, c):
        end = c[v]

        for b, f, y in res[v]:
            c[v][int(y)][f] = b

        return end

    for s in lines:
        k, *v = s.split()

        if k not in res:
            res[k] = []

        res[k].append(v)

    replace(
        lambda v,c: v in res,
        update,
        tables.sets
    )


if __name__ == '__main__':
    name   = 'scripts/json.zlib'
    tables = generate.loads(name)

    search = collect.init(
        os.environ['PYLAST_API_KEY'],
        os.environ['PYLAST_API_SECRET']
    )

    with open('headliners.txt') as file:
        lines = file.readlines()
        billing(lines, tables)

    generate.dumps(tables, name)
