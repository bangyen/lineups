from bs4 import BeautifulSoup

import requests
import os
import re

class WebScraper:
    page = re.compile(r'\?page=(\d+)')

    def __init__(self, link):
        self.link = link

    def scrape_url(self, name):
        path = f'data/{name}.html'
        link = self.link

        if os.path.exists(path):
            with open(path, 'r') as file:
                return file.read()

        resp = requests.get(link)
        text = resp.text

        with open(path, 'w') as file:
            file.write(text)

        return text

    def create_soup(self):
        page = self.page
        link = self.link

        path = link.split('/')[-1]
        name = path.rsplit('-', 1)[0]

        if match := page.search(link):
            group = match.group(1)
            name  = f'{name}-{group}'

        text = self.scrape_url(name)

        return BeautifulSoup(
            text, 'html.parser'
        )
