from src.scraper  import WebScraper
from src.database import Database
from urllib.parse import urljoin

import argparse
import dotenv

def get_pages(main):
    html = WebScraper(main)
    soup = html.create_soup()
    save = {main: soup}

    links = soup.find_all(
        class_='pageLink'
    )

    for link in links:
        path = link.get('href')

        if not path:
            continue

        full = urljoin(main, path)
        html = WebScraper(full)
        soup = html.create_soup()

        save[full] = soup

    return save


def reformat(pages, name):
    item = pages.items()
    data = []

    for link, soup in item:
        fest = Festival(soup, link)
        meta = fest.get_metadata()

        for link, vals in meta.items():
            data.append({
                '_id':  link,
                'name': name,
                **vals
            })

    return data


class Festival:
    fields = [
        'year',
        'name',
        'venues',
        'start',
        'end'
    ]

    def __init__(self, soup, link):
        self.soup = soup
        self.link = link

    def parse_cell(self, cell):
        name = cell['class'][0]

        if name == 'venues':
            return [
                html.text for html
                in cell.find_all('span')
            ]

        if name == 'name':
            main = self.link
            path = cell.a.get('href')
            link = urljoin(main, path)

            return link

        return cell.text

    def get_metadata(self):
        table = self.soup.tbody
        batch = table.find_all('tr')
        years = {}

        for row in batch:
            data = self.get_fields(row)
            rest = self.fields[2:]
            year = data['year']
            link = data['name']

            vals = {
                field: data[field]
                for field in rest
            }

            years[link] = {
                'year': int(year),
                **vals
            }

        return years

    def get_fields(self, row):
        parser = self.parse_cell
        fields = self.fields
        result = {}

        for field in fields:
            cell = row.find(class_=field)
            data = parser(cell)

            result[field] = data

        return result

if __name__ == '__main__':
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument('link')

    args = parser.parse_args()
    main = args.link

    base = Database('festivals')
    save = get_pages(main)

    data = reformat(save, main)
    base.insert(data)
