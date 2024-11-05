from src.database import Database

import dotenv

if __name__ == '__main__':
    dotenv.load_dotenv()

    names = ['festivals', 'concerts']

    for name in names:
        base = Database(name)

        for k in range(1990, 2025):
            find  = {'year': str(k)}
            data  = {'$set': {'year': k}}
            cache = base.cache

            cache.update_many(find, data)
