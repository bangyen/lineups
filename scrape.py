from bs4 import BeautifulSoup
import sys
import os
import re

def parse(html):
    soup = BeautifulSoup(html, 'html.parser')

    if not soup.find('span', class_='b0Xfjd', string='Lineup'):
        return

    span = soup.find_all('span', class_='nxucXc CxwsZe')
    return [s.string for s in span]

if __name__ == '__main__':
    args = sys.argv

    if len(args) == 1:
        exit('Please supply a file.')

    if not os.path.exists(args[1]):
        exit('File not found.')

    with open(args[1], encoding='utf-8') as file:
        html = file.read()
        print(parse(html))

        file.close()
