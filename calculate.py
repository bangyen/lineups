import generate

def percent(fest, artists, sets, trim=True):
    genres = {}

    for s in sets:
        if s[0] != fest:
            continue

        main = artists[s[1]]['main']

        if main not in genres:
            genres[main] = 0

        genres[main] += 1

    prune = {
        k:v for k,v in genres.items()
        if k is not None
        and v > 1
    }

    total = sum(prune.values())
    order = sorted(
        prune.items(),
        key=lambda t: t[1]
    )[::-1]

    return [
        (k, v / total * 100)
        for k,v in order
    ]


if __name__ == '__main__':
    name   = 'info.json'
    f, a, s = generate.loads(name)

    for fest in f:
        genres = percent(fest, a, s)
        long   = max(len(t[0]) for t in genres)

        print(fest)

        for k,v in genres:
            size = ' ' * (long - len(k))
            print(f'\t{k}{size}: {round(v)}%')
