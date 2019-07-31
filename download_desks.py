from scrapy.crawler import CrawlerProcess
from desk_spider import DeskSpider
import json
import sys

if len(sys.argv) != 3 or sys.argv[1] != '--file':
    print('invalid arguments')
    sys.exit()

filename = sys.argv[2]
process = CrawlerProcess({'FEED_FORMAT': 'json',
                          'FEED_URI': filename, })
process.crawl(DeskSpider())
process.start()

cities = []

with open(filename, 'r') as input:
    cities = json.load(input)
    cities.sort(key=lambda k: k['city'])

with open(filename, 'w') as output:
    json.dump(cities, output)
