import re

def match(inp, acc=0):
    if not acc:
        return len(inp)

    if (tok := inp[0]) == '(':
        acc += 1
    elif tok == ')':
        acc -= 1

    return match(inp, acc)


def parser(inp):
    ...


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
            r'\w+'    ,
            r'\d+'    ,
            r'=='     ,
            r'!='     ,
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
    inp = input('Input: ')
    print(lexer(inp))
