import scrapy
import re
import json
import os

class DocumentSpider(scrapy.Spider):
    name = 'documents'
    # start_urls = [
    #     'https://cs.wikipedia.org/wiki/Seznam_m%C4%9Bst_v_%C4%8Cesku']

    def parse(self, response):
        folder = 'https://www.abertamy.eu/'.replace('/','-').replace(':','').replace('--','-')

        print('dir: ' + folder)
        if not os.path.exists(folder):
            os.makedirs(folder)

        yield response.follow('https://www.abertamy.eu/uredni-deska/', self.download_documents, meta={'folder' : folder})

    def download_documents(self, response):
        for h2 in response.css('div>h2.boardHeading'):
            for a in h2.css('a::attr(href)'):
                yield response.follow(a.get(), self.download_file, meta=response.meta)

    def download_file(self, response):
        for a in response.css('a'):
            if 'download' in a.css('::attr(href)').get():
                yield response.follow(a.css('::attr(href)').get(), self.save_pdf, meta=response.meta)

    def save_pdf(self, response):
        folder = response.meta.get('folder')

        path = folder + '/' + response.url.split('/')[-1].split('?')[0] + '.pdf'
        self.logger.info('Saving PDF %s', path)

        with open(path, 'wb') as f:
            f.write(response.body)

