import generate

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

    total = sum(genres.values())
    rest  = sum(t[1] for t in order[limit:])

    order = [
        *order[:limit],
        ('Other', rest)
    ]

    return [
        (k, v / total * 100)
        for k,v in order
    ]


if __name__ == '__main__':
    year    = 2023
    name    = 'json.zlib'
    f, a, s = generate.loads(name)

    for fest in f:
        def pred(s):
            return  s[0] == fest \
                and s[2] == year

        genres = percent(pred, a, s)[:-1]
        long   = max(len(t[0]) for t in genres)
        print(fest, year)

        for k,v in genres:
            size = ' ' * (long - len(k))
            print(f'\t{k}{size}: {round(v)}%')
