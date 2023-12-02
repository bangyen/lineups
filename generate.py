import requests
import os

if __name__ == '__main__':
    image = (
        'https://nashvilleguru.com/'
        'officialwebsite/wp-content/'
        'uploads/2021/03/Bonnaroo-Lineup-2023.png'
    )

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        'apiKey': os.environ['OPTIIC_API_KEY'],
        'url'   : image
    }

    # https://curlconverter.com/
    resp = requests.get(
        'https://api.optiic.dev/process',
        headers=headers,
        json=data
    )

    with open('output.txt', 'w') as file:
        output = resp.json()['text']
        file.write(output)
        file.close()
