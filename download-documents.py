import scrapy
import re
import json

class DocumentSpider(scrapy.Spider):
    name = 'cities'
    start_urls = [
        'https://cs.wikipedia.org/wiki/Seznam_m%C4%9Bst_v_%C4%8Cesku']

    def parse(self, response):
        with open('helpful/desks.json') as data:
            cities = json.load(data)

        # for city in cities[:10]:
        #     for desk in city['desk']:
        #         link = ''

        #         if 'http' in desk or 'https' in desk or 'www' in desk:
        #             link = desk
        #         else:
        #             prefix = city['city-web'][:-1] if city['city-web'][-1] == '/' else city['city-web']
        #             link = prefix + desk 
                    
        #         print(link)
        yield response.follow('https://www.abertamy.eu/uredni-deska/', self.download_documents)

    def download_documents(self, response):
        for h2 in response.css('div>h2.boardHeading'):
            for a in h2.css('a::attr(href)'):
                # print(a.get())
                yield response.follow(a.get(), self.download_file)

    def download_file(self, response):
        for a in response.css('a'):
            if 'download' in a.css('::attr(href)').get():
                # print(a.css('::attr(href)').get())
                yield response.follow(a.css('::attr(href)').get(), self.save_pdf)

    def save_pdf(self, response):
        folder = 'https://www.abertamy.eu/'.replace('/','-')
        
        path = folder + response.url.split('/')[-1].split('?')[0] + '.pdf'
        self.logger.info('Saving PDF %s', path)
        with open(path, 'wb') as f:
            f.write(response.body)

