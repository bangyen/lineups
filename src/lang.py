import re

def match(lst):
    def count(inp, acc):
        if not acc:
            return len(inp)

        if (tok := inp[0]) == '(':
            acc += 1
        elif tok == ')':
            acc -= 1

        return count(inp[1:], acc)

    rest = count(lst[1:], 1)
    return len(lst) - rest


def split(regex, inp):
    alt = fr'({regex})(.*)'
    mat = re.match(alt, inp)

    one = mat.group(1)
    two = mat.group(2)

    return one, two


def conv(val):
    def get(tab, key):
        if isinstance(key, str):
            return tab[key][val]

        return key[val]

    def func(op):
        s = f'lambda a, b: a {op} b'
        return eval(s)

    keyw = ('and', 'or', '==', '!=')
    ltrl = ('True', 'False', 'None')

    if val in keyw:
        return func(val)
    if val in ltrl:
        return eval(val)
    if val.isdigit():
        return int(val)
    if val[0] == '"':
        return val[1:-1]
    if val == 'key':
        return lambda t, k: k
    if val == '=~':
        return lambda a, b: \
               re.search(b, a)

    return get


def output(pair):
    table, sub = pair
    fmt = isinstance(table, dict)

    for n in sub:
        print(n if fmt else '')

        if fmt:
            dct = table[n]
        else:
            dct = n

        for key in dct:
            tab = '\t' * fmt
            val = dct[key]

            print(f'{tab}{key}: {val}')


def test(inp, tables):
    def branch(ast, key):
        if isinstance(ast, tuple):
            op, x, y = ast
            a = branch(x, key)
            b = branch(y, key)
            return op(a, b)

        if callable(ast):
            return ast(tab, key)

        return ast

    if inp is None:
        return

    tab = getattr(tables, inp[0])

    return tab, [
        k for k in tab
        if branch(inp[1], k)
    ]


def parse(lst):
    def branch(inp):
        tok = inp[0]

        if tok == '(':
            end = match(inp)
            sub = inp[1:end - 1]
            one = branch(sub)
        else:
            end = 3
            op  = conv(inp[1])
            a   = conv(inp[0])
            b   = conv(inp[2])
            one = (op, a, b)

        if len(inp) == end:
            return one

        if inp[end] in keywrd:
            two = branch(inp[end + 1:])
            return inp[end], one, two

    if len(lst) < 2:
        return

    tables = ('fests', 'artists', 'sets')
    keywrd = ('and',   'or')
    tab, cond, *rest = lst

    if cond != 'if':
        return

    if tab in tables:
        return tab, branch(rest)


def lex(inp):
    def add(reg, val):
        res = split(reg, val)

        if not res:
            return ''

        a, b = res
        out.append(a)
        return b

    out = []

    while inp:
        regex = (
            r'\w+|\d+' ,
            r'==|!=|=~',
            r'"[^"]*"' ,
            r'[()]'
        )

        grp = '|'.join(regex)
        inp = add(grp, inp).strip()

    return out


def run(inp, tables):
    tok = lex(inp)
    ast = parse(tok)

    if ast is None:
        return

    pair = test(ast, tables)
    output(pair)
