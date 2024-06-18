import src.generate as generate
import src.collect  as collect
import os

def interact(tables):
    """
    Prompts the user to input set information,
    validates the input, and stores the information
    in a list of tuples. If the user inputs '!redo',
    it restarts the input process. Finally, it calls
    the billing function with the collected information.
    """
    fest = artist = True
    year = bill   = ''
    res  = []

    while fest:
        fest = input('Festival: ')

        if fest not in tables.fests:
            continue

        while not year.isdigit():
            year = input('Year: ')

        while artist:
            artist = input('Artist: ')
            status = input('Headliner (y/n): ')

            if not status:
                break

            if status == '!redo':
                continue

            if status and status[0] == 'y':
                bill = 'Headliner'
            else:
                bill = 'Subheadliner'

            row = (artist, bill, fest, year)
            res.append(row)

    if res:
        billing(res, tables)


def billing(lines, tables):
    """
    Takes a list of tuples containing set information and
    updates the database with the corresponding billing
    information. If an artist is not found in the database,
    it uses a similar name. If an invalid billing status
    is provided, it exits the program.
    """
    opts  = ('Headliner', 'Subheadliner')
    names = []

    for row in lines:
        if isinstance(row, str):
            args = row.rsplit(maxsplit=3)
        else:
            args = row

        a, b, f, y = args
        y = int(y)

        if a not in tables.artists:
            for n in tables.artists:
                same = collect.strdiff(a, n)

                if same > 0.9:
                    names.append((a, n))
                    a = n

        if b not in opts:
            exit(args)

        res = tables.get_set(
            fest=f,
            year=y,
            artist=a
        )

        res['bill'] = b

    size = max(len(t[1]) for t in names)

    for k, v in names:
        diff = ' ' * (size -len(k))
        print(f'{k}{diff}  ==>  {v}')
