import scrapy
import re
import json


class DeskSpider(scrapy.Spider):
    name = 'cities'

    def parse(self, response):
        with open('cities.json', 'r') as data:
            cities = json.load(data)

        for city in cities:
            yield response.follow(city['web'],
                                      self.extract_official_board)


    def extract_official_board(self, response):
        result = {'city-web': response.request.url, 'desk': []}

        for link in response.css('a'):
            if re.search('deska', link.get(), re.IGNORECASE):
                result['desk'].append(link.css('::attr(href)').get())

        yield result
