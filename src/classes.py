import collections

class Database(tuple):
    def __new__(cls, tables):
        return super(Database, cls) \
            .__new__(cls, tuple(tables))

    def __init__(self, tables):
        fests, artists, sets = tables
        self.tables  = tables
        self.fests   = {k:Fest  (v) for k,v in fests  .items()}
        self.artists = {k:Artist(v) for k,v in artists.items()}
        self.sets    = [Set(s) for s in sets]

    def dumps(self):
        f = {k:v.data for k,v in self.fests  .items()}
        a = {k:v.data for k,v in self.artists.items()}
        s = [s.data for s in self.sets]

        return f, a, s

    @staticmethod
    def get(table, val):
        for v in val:
            if v not in table:
                table[v] = {}

            table = table[v]

        return table

    def get_fest(self, val):
        fests = self.fests
        return self.get(fests, val)

    def get_artist(self, val):
        artists = self.artists
        return self.get(artists, val)

    def get_set(self, **keys):
        res  = [
            s for s in self.sets
            if s | keys == s
        ]

        if len(res) == 1:
            return res[0]

        return res

    @staticmethod
    def add(table, args):
        out  = Database.get(
            table, args[:-2]
        )

        key, val = args[-2:]
        out[key] = val

    def add_fest(self, val):
        fests = self.fests
        self.add(fests, val)

    def add_artist(self, val):
        artists = self.artists
        self.add(artists, val)

    def add_set(self, **vals):
        self.sets.append(vals)


def assign(**kwargs):
    def inner(key, val):
        for n, t in kwargs.items():
            test = check(n, t)

            if test(key, val):
                return True

        return False

    return inner


def check(name, test):
    def inner(key, val):
        vb = isinstance(val, test)
        kb = key == name

        return kb and vb

    return inner


def pretty(self, key=None):
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


class Fest(collections.UserDict):
    headers = ['key', 'place']
    pretty  = pretty

    def __init__(self, data):
        self.test = assign(
            dates=dict,
            place=str
        )

        super().__init__(data)


    def __setitem__(self, key, val):
        if self.test(key, val):
            super().__setitem__(key, val)


class Artist(collections.UserDict):
    headers = ['key', 'main', 'genres', 'woman']
    pretty  = pretty

    def __init__(self, data):
        self.test = assign(
            woman=(bool, type(None)),
            genres=list,
            main=str
        )

        if 'main' not in data:
            data['main'] = ''

        super().__init__(data)


    def __setitem__(self, key, val):
        if self.test(key, val):
            super().__setitem__(key, val)


class Set(collections.UserDict):
    headers = ['artist', 'bill', 'fest', 'year']
    pretty  = pretty

    def __init__(self, data):
        self.test = assign(
            artist=str,
            bill=str,
            fest=str,
            year=int
        )

        super().__init__(data)


    def __setitem__(self, key, val):
        if self.test(key, val):
            super().__setitem__(key, val)
