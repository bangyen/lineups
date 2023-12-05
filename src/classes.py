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
