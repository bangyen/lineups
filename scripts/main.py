import scripts.parse as parse
import src.calculate as calculate
import src.generate  as generate
import src.collect   as collect
import src.lang      as lang
import src.edit      as edit

import argparse
import dotenv

def factory(split):
    """
    Generates a customized inner function
    that parses command-line arguments,
    applies a specified split function,
    and appends results to the database.
    """
    def inner(params, tables, search):
        data   = generate.parse(params)
        lineup = split(data)

        collect.append(
            lineup,
            search,
            tables
        )

    return inner


html = factory(parse.html)
text = factory(parse.text)


def compare(params, tables):
    """
    Parses arguments to compare music data
    by genre and festival/year, calculating
    percentage values as output.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('genre')

    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--fest', choices=tables.fests.keys())
    group.add_argument('-y', '--year', type=int)

    args  = parser.parse_args(params)
    const = args.fest or args.year

    if args.fest:
        name = 'compare_years'
    else:
        name = 'compare_fests'

    func = getattr(calculate, name)
    outp = func(args.genre, const, tables)

    return calculate.percent(
        (f'{args.genre.title()} '
         f'Music ({const})'),
        outp
    )


def overlap(params, tables):
    """
    Parses arguments to find overlapping
    artists between a main festival and
    one or more additional festivals for
    a specified year, calculating percentage
    values as output.
    """
    keys   = tables.fests.keys()
    parser = argparse.ArgumentParser()
    parser.add_argument('main', choices=keys)
    parser.add_argument('rest', choices=keys, nargs='+')
    parser.add_argument('year', type=int)
    args   = parser.parse_args(params)

    output = calculate.overlap(
        args.main, args.rest,
        args.year, tables
    )

    return calculate.percent(
        f'Overlap with {args.main}',
        [t[:2] for t in output]
    )


def query(params, tables):
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd')
    args = parser.parse_args(params)

    return lang.run(args.cmd, tables)


def edit(params, tables):
    data = generate.parse(params, True)
    edit.billing(data, tables)


if __name__ == '__main__':
    dotenv.load_dotenv()

    choice = (
        'html' , 'text'   ,
        'query', 'overlap',
        'edit' , 'compare'
    )

    parser = argparse.ArgumentParser()
    parser.add_argument('func', choices=choice)
    parser.add_argument('rest', nargs=argparse.REMAINDER)
    args   = parser.parse_args()

    search = args.func in choice[:2]
    dump   = args.func == 'edit' or search

    output = generate.wrap(
        args.rest,
        eval(args.func),
        dump, search
    )

    if output:
        print(output)
