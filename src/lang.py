import src.classes as classes
import operator
import re

class QueryError(SyntaxError):
    pass


class Syntax:
    tables = ('fests', 'artists', 'sets')

    def __init__(self, tokens):
        def error(msg):
            raise QueryError(msg)

        if not tokens:
            msg = 'Empty query'
            error(msg)

        if (table := tokens[0]) \
                not in Syntax.tables:
            msg = 'Invalid table'
            error(msg)

        if len(tokens) < 2:
            msg = 'Missing keyword'
            error(msg)

        if tokens[1] != 'if':
            msg = 'Invalid keyword'
            error(msg)

        self.table = table
        self.tree  = Node(tokens[2:])

    @staticmethod
    def pair(table):
        if isinstance(table, dict):
            return lambda k: (k, table[k])

        return lambda k: (None, k)

    def filter(self, tables):
        """
        Filters a table based on a condition. It
        returns a tuple containing the table and
        a list of tuples that meet the condition.
        """
        name  = self.table
        tree  = self.tree

        table = getattr(tables, name)
        return table.filter(tree)


class Node:
    eqls = ('==' , '!=', '=~')
    kwrd = ('and', 'or')

    def __init__(self, tokens):
        exp = ' '.join(tokens)

        if len(tokens) < 3:
            fmt = 'Invalid expression: {}'
            msg = fmt.format(exp)
            raise QueryError(msg)

        if len(tokens) == 3:
            inv = Node.invalid
            con = Node.convert
            a, op, b = tokens

            if op not in Node.eqls: inv(exp, op)
            if Node.operator(a):    inv(exp, a)
            if Node.operator(b):    inv(exp, b)

            self.left  = con(a)
            self.right = con(b)
            self.op    = con(op)
        else:
            if tokens[0] == '(':
                end = match(tokens)
                sub = tokens[1:end - 1]
            else:
                end = 3
                sub = tokens[0:3]

            if tokens[end] not in Node.kwrd:
                Node.invalid(exp, tokens[end])

            self.left  = Node(sub)
            self.right = Node(tokens[end + 1:])
            self.op    = Node.convert(tokens[end])

    @staticmethod
    def operator(token):
        funcs = (*Node.eqls, *Node.kwrd)

        for op in funcs:
            regex = op + '$'

            if re.match(regex, token):
                return True

        return False

    @staticmethod
    def invalid(exp, tok):
        fmt = 'Invalid token {} in expression {}'
        msg = fmt.format(tok, exp)
        raise QueryError(msg)

    @staticmethod
    def convert(val):
        """
        Converts a string into a Python object or
        function, supporting various data types
        and operations.
        """
        def get(tab, key):
            return tab[key][val]

        def search(key, reg):
            return re.search(reg, key)

        expr = {
            'key': lambda t, k: k,
            'and': operator.and_ ,
            'or' : operator.or_,
            '==' : operator.eq ,
            '!=' : operator.ne ,
            '=~' : search,
            'True' : True,
            'False': False
        }

        if val in expr  : return expr[val]
        if val[0] == '"': return val[1:-1]
        if val.isdigit(): return int(val)

        return get

    def test(self, table, key):
        def inner(tree):
            if isinstance(tree, Node):
                left = tree.left
                rght = tree.right
                op   = tree.op

                lval = inner(left)
                rval = inner(rght)

                return op(lval, rval)

            if callable(tree):
                return tree(table, key)

            return tree

        return inner(self)


def lex(inp):
    """
    Tokenizes a string into a list of tokens. It
    uses regular expressions to match different
    token types.
    """
    def add(reg, val):
        res = split(reg, val)

        if not res:
            out.clear()
            return

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
        inp = add(grp, inp)

    return out


def run(inp, tables):
    token = lex(inp)
    tree  = Syntax(token)
    subt  = tree.filter(tables)

    return subt.format()


def match(lst):
    """
    Finds the index of the closing parenthesis
    that matches the opening parenthesis at the
    beginning of the list.
    """
    def count(inp, acc):
        if not acc: return len(inp)
        if not inp: return -1

        if (tok := inp[0]) == '(':
            acc += 1
        elif tok == ')':
            acc -= 1

        return count(inp[1:], acc)

    rest = count(lst[1:], 1)
    return len(lst) - rest


def split(regex, inp):
    """
    Returns the two parts of the input string:
    the part that matches the regular expression,
    and the part that follows it.
    """
    alt = fr' *({regex})( +(.*)|$)'
    mat = re.match(alt, inp)

    if not mat:
        return

    one = mat.group(1)
    two = mat.group(3)

    return one, two


