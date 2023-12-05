import src.generate as generate

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

    total = sum(genres.values()) or 1
    rest  = sum(t[1] for t in order[limit:])

    order = [
        *order[:limit],
        ('Other', rest)
    ]

    return [
        (k, v / total * 100)
        for k,v in order
    ]


def table(title, data, pad=4):
    def line(left, fill, cntr, rght):
        return (
            left + fill * keys  +
            cntr + fill * spill +
            rght + '\n'
        )

    ints  = [(k, round(v)) for k,v in data]
    keys  = max(len(t[0])  for t   in ints)
    right = keys // 2 + pad

    width = max(
        keys + right + 1,
        len(title)
    )

    keys  += pad
    width += (width % 2) + pad + 1
    spill = width - keys - 1

    return (
        line('┌', '─', '─', '┐')   + '│'
        + title.center(width)      + '│\n'
        + line('├', '─', '┬', '┤')
        + line('├', '─', '┼', '┤')
            .join(
                f'│{k.center(keys)}' +
                f'│{f"{v}%".center(spill)}│\n'
                for k,v in ints
            )
        + line('└', '─', '┴', '┘')
    )


if __name__ == '__main__':
    year    = 2023
    name    = 'json.zlib'
    f, a, s = generate.loads(name)

    for fest in f:
        def pred(s):
            return  s[0] == fest \
                and s[2] == year

        genres = percent(pred, a, s)[:-1]

        if fest == 'Bonnaroo':
            genres = [
                ('electronic', 21),
                ('indie',      10),
                ('folk',        8),
                ('Hip-Hop',     5),
                ('pop',         5),
                ('jazz',        5),
                ('indie rock',  4)
            ]

        if len(genres) == 0:
            continue

        print(table(f'{fest} {year}', genres))
