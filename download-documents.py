import scrapy
import re
import json
import os
import urllib.request


class DocumentSpider(scrapy.Spider):
    name = 'documents'
    start_urls = [
        'https://cs.wikipedia.org/wiki/Seznam_m%C4%9Bst_v_%C4%8Cesku']

    def parse(self, response):
        with open('helpful/desks.json') as data:
            cities = json.load(data)

        for i in range(0, 10):
            folder = cities[i]['city-web'].split('.')[1].replace(
                '/', '-').replace(':', '').replace('--', '-')

            if not os.path.exists(folder):
                os.makedirs(folder)

            yield response.follow(cities[i]['city-web'], self.get_desk, meta={'folder': folder, 'desk': cities[i]['desk'][0]})

    def get_desk(self, response):
        yield response.follow(response.meta.get('desk'), self.download_documents, meta=response.meta)

    def download_documents(self, response):
        file_indicator = ['download', 'pdf',
                          'oznámení o', 'dokument', 'document', 'file']
        ignore_indicator = ['.wmv']

        document_id = 0

        for a in response.css('a'):
            print('a: ' + a.get())
            if any(word in a.get().lower() for word in ignore_indicator):
                continue

            if any(word in a.get().lower() for word in file_indicator):
                print('href: ' + a.css('::attr(href)').get())
                document_id = document_id + 1
                response.meta['document_id'] = document_id
                yield response.follow(a.css('::attr(href)').get(), self.save_pdf, meta=response.meta)

    def save_pdf(self, response):
        print('content-type:' + response.headers.get('content-type').decode('utf-8'))

        if 'pdf' in response.headers.get('content-type').decode('utf-8'):
            folder = response.meta.get('folder')

            path = folder + '/' + \
                folder + str(response.meta.get('document_id'))

            if path[-4:] != '.pdf':
                path = path + '.pdf'

            self.logger.info('Saving PDF %s', path)

            with open(path, 'wb') as f:
                f.write(response.body)

        if 'html' in response.headers.get('content-type').decode('utf-8'):
            print('url: ' + response.request.url)
            self.download_documents(response)
            yield response.follow(response.request.url, self.download_documents, meta=response.meta)
