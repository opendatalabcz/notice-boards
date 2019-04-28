import scrapy
import re
import json
import os

class DocumentSpider(scrapy.Spider):
    name = 'documents'
    start_urls = [
        'https://cs.wikipedia.org/wiki/Seznam_m%C4%9Bst_v_%C4%8Cesku']

    def parse(self, response):
        with open('helpful/desks.json') as data:
            cities = json.load(data)

        for city in cities[:10]:
            folder = city["city-web"].replace('/','-').replace(':','').replace('--','-')

            if not os.path.exists(folder):
                os.makedirs(folder)

            yield response.follow(city["desk"][0], self.download_documents, meta={'folder' : folder})

    def download_documents(self, response):
        for a in response.css('a'):
            if any(word in a.get() for word in ['download', 'pdf']):
                print(a.css('::attr(href)').get())
                yield response.follow(a.css('::attr(href)').get(), self.save_pdf, meta=response.meta)

    def save_pdf(self, response):
        folder = response.meta.get('folder')

        path = folder + '/' + response.url.split('=')[1] + '.pdf'
        self.logger.info('Saving PDF %s', path)

        with open(path, 'wb') as f:
            f.write(response.body)

