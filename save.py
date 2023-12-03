import json

def loads(name):
    data = ''

    with open(name) as file:
        data = file.read()
        file.close()

    return json.loads(data)


def dumps(tables, name):
    with open(name, 'w') as file:
        data = json.dumps(
            tables,
            sort_keys=True,
            indent=4
        )

        file.write(data)
        file.close()
