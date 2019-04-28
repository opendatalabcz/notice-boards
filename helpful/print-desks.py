import json

with open('desks.json') as data:
    cities = json.load(data)

for city in cities[:10]:
    for desk in city['desk']:
        if 'http' in desk or 'https' in desk or 'www' in desk:
            print(desk)   
        else:
            prefix = city['city-web'][:-1] if city['city-web'][-1] == '/' else city['city-web']
            print(prefix + desk)