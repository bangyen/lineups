import requests
import os

if __name__ == '__main__':
    image = (
        'https://nashvilleguru.com/'
        'officialwebsite/wp-content/'
        'uploads/2021/03/Bonnaroo-Lineup-2023.png'
    )

    data = {
        'apikey': os.environ['OCR_API_KEY'],
        'url'   : image
    }

    resp = requests.get(
        'https://api.ocr.space/parse/imageurl',
        params=data
    )

    with open('output.txt', 'w') as file:
        output = resp.json()['ParsedResults'][0]['ParsedText']
        file.write(output)
        file.close()
