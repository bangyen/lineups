import src.classes as classes
import src.collect as collect
import argparse
import zlib
import json
import os

def loads(name):
    data = ''

    with open(name, 'rb') as file:
        comp = file.read()
        byte = zlib.decompress(comp)
        data = json.loads(byte)

    return classes.Database(data)


def dumps(tables, name):
    with open(name, 'wb') as file:
        data = tables.tables
        strs = json.dumps(data)
        byte = strs.encode()

        comp = zlib.compress(byte)
        file.write(comp)


def wrap(
        params, func,
        dump=False, search=False,
        json='scripts/json.zlib'):
    tables = loads(json)

    args   = {
        'params': params,
        'tables': tables
    }

    if search:
        args['search'] = \
            collect.init(
                os.environ['PYLAST_API_KEY'],
                os.environ['PYLAST_API_SECRET'],
                tables
            )

    func(**args)

    if dump:
        dumps(tables, json)


def parse(rest, lines):
    parser = argparse.ArgumentParser()
    file   = argparse.FileType(encoding='utf-8')
    parser.add_argument('data', type=file)

    args = parser.parse_args(rest)
    data = args.data

    if lines:
        output = [
            r.strip() for r in
            data.readlines()
        ]
    else:
        output = data.read()

    data.close()
    return output
