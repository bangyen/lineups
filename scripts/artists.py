from src.database import Database

import dotenv

if __name__ == '__main__':
    dotenv.load_dotenv()

    base = Database('artists')
