import scrapy
import json
import sys
import re
from scrapy.crawler import CrawlerProcess
from document_spider import DocumentSpider
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from multiprocessing import Process, Queue
from twisted.internet import reactor


def f(q, city, url, domain):
    try:
        runner = CrawlerRunner()
        deferred = runner.crawl(DocumentSpider(
            city=city), start_urls=url, allowed_domains=domain)
        deferred.addBoth(lambda _: reactor.stop())
        reactor.run()
        q.put(None)
    except Exception as e:
        q.put(e)


def run_spider(city, url, domain):
    q = Queue()
    p = Process(target=f, args=(q, city, url, domain))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result


def get_short_name(citi_name):
    return citi_name.split(' (')[0].strip().lower()


def get_cities_beginning_with(args, cities):
    begin = args[0].lower()

    if not any(get_short_name(city['city']) == begin
               for city in cities):
        print('no city satisfying begin criteria')
        sys.exit()
    if len(args) == 1:
        return [city for city in cities if get_short_name(city['city']) >= begin]
    if len(args) != 3:
        print('invalid arguments')
        sys.exit()
    if args[1] == '--count':
        return [city for city in cities if get_short_name(city['city']) >= begin
                ][:int(args[2])]

    end = args[2].lower()
    if not any(get_short_name(city['city']) == end
               for city in cities):
        print('no city satisfying end criteria')
        sys.exit()
    return [city for city in cities if get_short_name(city['city']) >= begin and get_short_name(city['city']) <= end]


if __name__ == '__main__':
    cities_to_download = []
    cities = []

    if sys.argv[1] != '--file':
        print('invalid arguments')
        sys.exit()

    with open(sys.argv[2], 'r') as data:
        cities = json.load(data)

    if len(sys.argv) >= 5 and sys.argv[3] == '--cities':
        cities_to_download = [
            city for city in cities if get_short_name(city['city']) in map(str.lower, sys.argv[4:])]
        print(cities_to_download)
    elif len(sys.argv) in [5, 7] and sys.argv[3] == '--begin':
        cities_to_download = get_cities_beginning_with(sys.argv[4:], cities)
    elif len(sys.argv) == 3:
        cities_to_download = cities
    else:
        print('invalid arguments')
        sys.exit()

    for i in range(len(cities_to_download)):
        print('downloading documents for city: {} ({} cities left)'.format(
            cities_to_download[i]['city'], len(cities_to_download)-i-1))
        run_spider(cities_to_download[i]['city'], cities_to_download[i]['desk'],
                   cities_to_download[i]['domain'])
