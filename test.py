import json

if __name__ == '__main__':
    data = {
        'A': 'Météo',
        'B': {
            'C': '@là'
        }
    }

    d = json.dumps(data)

    print (d)

    e = json.loads(d)

    print (e)

    f = json.dumps(e)
