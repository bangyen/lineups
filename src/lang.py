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


def parser(lst):
    def branch(inp):
        tok = inp[0]

        if tok == '(':
            end = match(inp)
            sub = inp[1:end - 1]
            one = branch(sub)
        else:
            end = 3
            a, op, b = inp[:3]
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


def lexer(inp):
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
            r'\w+|\d+',
            r'==|!='  ,
            r'"[^"]*"',
            r'[()]'
        )

        grp = '|'.join(regex)
        inp = add(grp, inp).strip()

    return out


def split(regex, inp):
    alt = fr'({regex})(.*)'
    mat = re.match(alt, inp)

    if not mat:
        return

    one = mat.group(1)
    two = mat.group(2)

    return one, two


if __name__ == '__main__':
    res = None

    while res is None:
        inp = input('Input: ')
        tok = lexer(inp)
        res = parser(tok)

        if res:
            print(res)
