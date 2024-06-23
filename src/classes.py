import collections

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
        self.tables  = tables
        self.fests   = {k:Fest  (v) for k,v in fests  .items()}
        self.artists = {k:Artist(v) for k,v in artists.items()}
        self.sets    = [Set(s) for s in sets]

    def dumps(self):
        """
        Converts the internal data structures (dictionaries
        and lists of Fest, Artist, and Set objects) into a
        tuple that can be easily serialized and stored.
        """
        f = {k:v.data for k,v in self.fests  .items()}
        a = {k:v.data for k,v in self.artists.items()}
        s = [s.data for s in self.sets]

        return f, a, s

    @staticmethod
    def get(table, val):
        """
        Traverses the dictionary recursively, creating
        new sub-dictionaries as needed, and finally
        returns the value associated with the last key
        in the sequence.
        """
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
        """
        Searches for sets in the database that have all
        the key-value pairs specified in the arguments.
        If only one set is found, it is returned directly.
        Otherwise, a list of matching sets is returned.
        """
        res  = [
            s for s in self.sets
            if s | keys == s
        ]

        if len(res) == 1:
            return res[0]

        return res

    @staticmethod
    def add(table, args):
        """
        Uses the get method to navigate to the correct
        sub-dictionary based on the first arguments,
        and then adds the last two arguments as a
        key-value pair to that sub-dictionary.
        """
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


def pretty(self, key=None):
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


class Table(collections.UserDict):
    """
    Uses the pretty method to format its attributes.
    It also defines a custom __setitem__ method to
    validate the type of the value being assigned.
    """
    pretty = pretty

    def __setitem__(self, key, val):
        if self.test(key, val):
            super().__setitem__(key, val)


class Fest(Table):
    headers = ['key', 'place']

    def __init__(self, data):
        self.test = assign(
            dates=dict,
            place=str
        )

        super().__init__(data)


class Artist(Table):
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


class Set(Table):
    headers = ['artist', 'bill', 'fest', 'year']

    def __init__(self, data):
        self.test = assign(
            artist=str,
            bill=str,
            fest=str,
            year=int
        )

        super().__init__(data)
