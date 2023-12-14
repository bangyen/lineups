import src.calculate as calculate
import src.generate  as generate
import sys

if __name__ == '__main__':
    name   = 'scripts/json.zlib'
    tables = generate.loads(name)

    _, year, main, *rest \
        = sys.argv

    output = calculate.overlap(
        main,   int(year),
        tables, *rest
    )

    data = calculate.table(
        f'Overlap with {main}',
        [t[:2] for t in output]
    )

    print(data)
