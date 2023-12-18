import scripts.parse as parse
import src.calculate as calculate
import src.generate  as generate
import src.collect   as collect
import src.lang      as lang
import src.lang      as edit
import argparse

def html(params, tables, search):
    data = generate.parse(params, False)
    wrap, names = parse.html(data)

    collect.append(
        wrap,
        names,
        search,
        tables
    )


def text(params, tables, search):
    html  = generate.parse(params, True)
    start = html.index('')

    head  = html[:start]
    wrap  = parse.text(head)

    body  = html[start + 1:]
    names = [r for r in body if r]

    collect.append(
        wrap,
        names,
        search,
        tables
    )


def compare(params, tables):
    parser = argparse.ArgumentParser()
    parser.add_argument('genre')

    group  = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-f', '--fest', choices=tables.fests.keys())
    group.add_argument('-y', '--year', type=int)

    args  = parser.parse_args(params)
    const = args.fest or args.year

    if args.fest:
        func = 'compare_years'
    else:
        func = 'compare_fests'

    output = getattr(calculate, func)(
        args.genre, const, tables
    )

    data = calculate.table(
        (f'{args.genre.title()} '
         f'Music ({const})'),
        output
    )

    print(data)


def overlap(params, tables):
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

    data = calculate.table(
        f'Overlap with {args.main}',
        [t[:2] for t in output]
    )

    print(data)


def query(params, tables):
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd')
    args = parser.parse_args(params)

    lang.run(args.cmd, tables)


def edit(params, tables):
    data = generate.parse(params, True)
    edit.billing(data, tables)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    choice = (
        'html',  'text',
        'query', 'overlap'
        'edit',  'compare'
    )

    parser.add_argument('func', choices=choice)
    parser.add_argument('rest', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    search = args.func in choice[:-1]
    dump   = args.func in choice[:-1] \
          or args.func == 'edit'

    generate.wrap(
        args.rest,
        eval(args.func),
        dump, search
    )
