import src.calculate as calculate
import collections

def wrapper(*fields):
    def recur(self, args):
        if not args:
            return self

        first, *rest = args
        apply = getattr(self, first)

        return recur(apply, rest)

    def inner(self, *args):
        func = recur(self, fields)
        return func(*args)

    return inner


def assign(**kwargs):
    """
    Takes keyword arguments that define the conditions
    (name, test). It returns a function that takes a
    key and a value, and checks if the value satisfies
    any of the conditions.
    """
    def inner(key, val):
        for n, t in kwargs.items():
            test = check(n, t)

            if test(key, val):
                return True

        return False

    return inner


def check(name, test):
    """
    Takes a name and a test (a type or a callable)
    as arguments. It returns a function that takes
    a key and a value, and checks if the key matches
    the name and the value is an instance of the test.
    """
    def inner(key, val):
        vb = isinstance(val, test)
        kb = key == name

        return kb and vb

    return inner


def pretty(self, key):
    """
    Uses the headers defined in the class to iterate
    over the object's attributes, converts the values
    to a string using the convert function, and returns
    them as a list.
    """
    def convert(head):
        if head == 'key':
            return key

        val = self[head]

        if isinstance(val, list):
            return ', '.join(val)

        return val

    return [
        convert(h) for h in
        type(self).headers
    ]


class Database(tuple):
    def __new__(cls, tables):
        """
        Overrides the default __new__ method to ensure
        that the tables are converted to a tuple.
        """
        return super(Database, cls) \
            .__new__(cls, tuple(tables))

    def __init__(self, tables):
        """
        Unpacks the tables into festivals, artists, and sets,
        and then converts each table into a dictionary/list
        of objects (Fest, Artist, or Set).
        """
        fests, artists, sets = tables
        f = self.table(fests,   Fest)
        a = self.table(artists, Artist)
        s = self.table(sets,    Set)

        self.tables  = (f, a, s)
        self.fests   = f
        self.artists = a
        self.sets    = s

    def dumps(self):
        """
        Converts the internal data structures (dictionaries
        and lists of Fest, Artist, and Set objects) into a
        tuple that can be easily serialized and stored.
        """
        return tuple(t.dumps() for t in self.tables)

    @staticmethod
    def table(data, sub):
        if isinstance(data, list):
            return ListTable(data, sub)

        return DictTable(data, sub)

    get_fest   = wrapper('fests',   'get')
    get_artist = wrapper('artists', 'get')
    get_set    = wrapper('sets',    'get')

    set_fest   = wrapper('fests',   'set')
    set_artist = wrapper('artists', 'set')
    set_set    = wrapper('sets',    'set')

    add_fest   = wrapper('fests',   'add')
    add_artist = wrapper('artists', 'add')
    add_set    = wrapper('sets',    'add')


class Table:
    def filter(self, tree):
        query = []

        for key in self:
            if not tree.test(self, key):
                continue

            query.append(key)

        return self.subset(query)

    def format(self):
        header = self.type.headers
        data   = self.data
        strs   = [
            self[k].format(k)
            for k in self
        ]

        table = calculate.table(header)
        table.add_rows(strs)
        table.header = True

        return table


class DictTable(Table, collections.UserDict):
    def __init__(self, data, subtype):
        self.type = subtype
        self.data = {
            k:subtype(data[k])
            for k in data
        }

    def subset(self, keys):
        cls  = self.type
        data = self.data
        sub  = DictTable({}, cls)

        sub.data = {
            k:data[k]
            for k in keys
        }

        return sub

    def get(self, row, col=None):
        res = self.data.get(row)

        if res is None:
            return

        if col is None:
            return res

        return res.get(col)

    def set(self, row, col, value):
        res = self.get(row, col)

        if res is None:
            return False

        ent = self.get(row)
        ent[col] = value

        return True

    def add(self, key, value):
        new = self.type(value)
        self.data[key] = new

    def dumps(self):
        return {
            k:v.data for k,v in
            self.data.items()
        }


class ListTable(Table, collections.UserList):
    def __init__(self, data, subtype):
        self.data = [subtype(v) for v in data]
        self.type = subtype

    def __iter__(self):
        size = len(self.data)
        return iter(range(size))

    def subset(self, keys):
        cls  = self.type
        data = self.data
        sub  = ListTable([], cls)

        sub.data = [
            data[k] for k in keys
        ]

        return sub

    def get(self, keys):
        res = [
            s for s in self.data
            if s | keys == s
        ]

        return res

    def set(self, key, val, params):
        res = self.get(params)

        for ent in res:
            ent[key] = res

        return len(res) > 0

    def add(self, data):
        new = self.type(data)
        self.data.append(new)

    def dumps(self):
        return [v.data for v in self.data]


class Entry(collections.UserDict):
    """
    Uses the pretty method to format its attributes.
    It also defines a custom __setitem__ method to
    validate the type of the value being assigned.
    """
    format = pretty

    def __setitem__(self, key, val):
        if self.test(key, val):
            super().__setitem__(key, val)


class Fest(Entry):
    headers = ['key']
    fields  = {
        'count': {
            'func': lambda n: len(n),
            'type': int
        }
    }

    def __init__(self, data):
        self.test = assign(
            **Fest.get('type')
        )

        super().__init__(data)

    @staticmethod
    def get(key):
        if key not in ('func', 'type'):
            raise ValueError

        return {
            k:v[key] for k,v in
            Fest.fields.items()
        }


class Artist(Entry):
    headers = ['key', 'main', 'genres', 'woman']

    def __init__(self, data):
        self.test = assign(
            woman=(bool, type(None)),
            genres=list,
            main=str
        )

        if 'main' not in data:
            data['main'] = ''

        super().__init__(data)


class Set(Entry):
    headers = ['artist', 'bill', 'fest', 'year']

    def __init__(self, data):
        self.test = assign(
            artist=str,
            bill=str,
            fest=str,
            year=int
        )

        super().__init__(data)
