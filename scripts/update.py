from src.database import Database

import dotenv

if __name__ == '__main__':
    dotenv.load_dotenv()

    names = ['artists']

    for name in names:
        base = Database(name)
        data = base.find({})

        for obj in data:
            name = obj['_id']
            tags = obj['tags']
            diff = {'tags': tags[:5]}

            base.cache.update_one(
                {'_id':  name},
                {'$set': diff}
            )
