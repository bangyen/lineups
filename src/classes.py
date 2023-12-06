class Database(tuple):
    def __new__(cls, tables):
        return super(Database, cls) \
            .__new__(cls, tuple(tables))

    def __init__(self, tables):
        fests, artists, sets = tables
        self.tables  = tables
        self.fests   = fests
        self.artists = artists
        self.sets    = sets

    @staticmethod
    def get(table, val):
        for v in val:
            if v not in table:
                table[v] = {}

            table = table[v]

        return table

    def get_fest(self, val):
        fests = self.fests
        self.get(fests, val)

    def get_artis(self, val):
        artists = self.artists
        self.get(artists, val)

    @staticmethod
    def add(table, args):
        out  = Database.get(
            table, args[:-2]
        )

        key, val   = args[-2:]
        table[key] = val

    def add_fest(self, val):
        fests = self.fests
        self.add(fests, val)

    def add_artist(self, val):
        artists = self.artists
        self.add(artists, val)

    def add_set(self, **vals):
        self.sets.append(vals)
