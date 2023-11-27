import sys
import os
import re

def parse(html):
    tab = (
        '<span class="b0Xfjd" '
        'style="color:#[0-9A-F]{6}">'
        'Lineup</span>'
    )

    artist = (
        '<span class='
        '"nxucXc CxwsZe">'
        '([^<]+)</span>'
    )

    if re.search(tab, html):
        return re.findall(artist, html)

if __name__ == '__main__':
    args = sys.argv

    if len(args) == 1:
        exit('Please supply a file.')

    if not os.path.exists(args[1]):
        exit('File not found.')

    with open(args[1]) as file:
        html = file.read()
        print(parse(html))

        file.close()
