# Lineup Database
- The script requires an API key and secret for Last.fm access (`init(key, secret, tables)`)
- The script prioritizes cached data and limits the number of Last.fm API calls to avoid overwhelming the service.

## Documentation
### Source Files
#### `collect.py`
- Artist Lookup:
  - `lookup(name)`: Attempts to find artist information using an internal cache and Last.fm API calls.
  - `backup(name)`: If artist information isn't found in the cache, performs a broader search using Last.fm.
  - `search(name)`: Calls `lookup` first, then falls back to `backup` if necessary.
- Data Processing:
  - `strdiff(name, match)`: Calculates similarity between two artist names using fuzzy matching.
  - `memoize(func)`: Caches function results to improve performance for frequently used lookups.
  - Extracts artist genre, bio summary, and gender from Last.fm data.
- Database Interaction:
  - `append(wrap, names, search, tables)`: Takes a list of artist names, searches for information using `search`, and adds them to the database (`tables`) along with associated festival and year information.

## Tutorial
- Client ID/Secret
  - Go to `https://www.last.fm/api/account/create`
  - Use `https://localhost:[port]/callback` as the Callback URL (?)
    - e.g., `https://localhost:8000/callback`
  - Submit
  - Go to `https://www.last.fm/api/accounts`
  - Copy API Key and Shared Secret
  - Paste in `variables.sh`
  - Run `source variables.sh`
- `.html` File
  - Search `[festival] [year] lineup` on Google
    - e.g., `bonnaroo 2023 lineup`
    - Right Click on Page and Click `Save Page As...`
    - Move `.html` file to Repository
- Python
  - Install Python at `https://www.python.org/`
  - Run `pip install -r requirements.txt`
  - Run `python scrape.py [lineup html file]`
    - e.g., `python scrape.py lineup.html`
