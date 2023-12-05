import src.generate as generate
import src.collect  as collect
import sys
import os

if __name__ == '__main__':
    args   = sys.argv
    name   = 'json.zlib'
    tables = generate.loads(name)

    search = collect.init(
        os.environ['PYLAST_API_KEY'],
        os.environ['PYLAST_API_SECRET']
    )

    if len(args) == 1:
        exit('Please supply a file.')

    if not os.path.exists(args[1]):
        exit('File not found.')

    with open(args[1], encoding='utf-8') as file:
        collect.append(
            file.read(),
            search,
            tables
        )

    generate.dumps(tables, name)
