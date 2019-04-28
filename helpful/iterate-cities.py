import json

with open('cities.json', 'r') as data:
    cities = json.load(data)

for city in cities:
    print(city['web'])