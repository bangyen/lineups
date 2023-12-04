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

        cache[val] = repl(val)


if __name__ == '__main__':
    name    = 'json.zlib'
    tables  = generate.loads(name)

    search = collect.init(
        os.environ['PYLAST_API_KEY'],
        os.environ['PYLAST_API_SECRET']
    )

    lookup(
        lambda v,c: 'USA' in c[v]['genres'],
        tables[1]
    )

    generate.dumps(tables, name)
