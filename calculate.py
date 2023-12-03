import generate

def percent(fest, artists, sets, limit=5):
    genres = {}

    for s in sets:
        if s[0] != fest:
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
    name   = 'json.zlib'
    f, a, s = generate.loads(name)

    for fest in f:
        genres = percent(fest, a, s)[:-1]
        long   = max(len(t[0]) for t in genres)

        print(fest)

        for k,v in genres:
            size = ' ' * (long - len(k))
            print(f'\t{k}{size}: {round(v)}%')
