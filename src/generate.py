import src.classes as classes
import src.collect as collect
import argparse
import zlib
import json
import os

def loads(name):
    """
    Opens a file, decompresses the data, and
    loads the JSON data into a Database object.
    """
    data = ''

    with open(name, 'rb') as file:
        comp = file.read()
        byte = zlib.decompress(comp)
        data = json.loads(byte)

    return classes.Database(data)


def dumps(tables, name):
    """
    Serializes the database data using JSON,
    compresses it, and writes it to a file.
    """
    with open(name, 'wb') as file:
        data = tables.dumps()
        strs = json.dumps(data)
        byte = strs.encode()

        comp = zlib.compress(byte)
        file.write(comp)


def wrap(
        params, func,
        dump=False, search=False,
        json='scripts/json.zlib'):
    """
    Loads a database from a file, passes it to
    the given function, and optionally saves
    the database afterwards. If search is True,
    it also initializes a LastFM API connection.
    """
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

    output = func(**args)

    if dump:
        dumps(tables, json)

    return output


def parse(rest):
    """
    Parses the command-line arguments, reads
    data from the specified file, and returns
    the data as a string.
    """
    parser = argparse.ArgumentParser()
    file   = argparse.FileType(encoding='utf-8')
    parser.add_argument('data', type=file)

    args = parser.parse_args(rest)
    data = args.data
    outp = data.read()

    data.close()
    return outp
