import scrapy
from scrapy.loader import ItemLoader
from items import DocumentItem
from pipelines import DocumentDownloaderPipeline


class DocumentSpider(scrapy.Spider):
    name = 'document_spider'

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2049.0 Safari/537.36',
        'ITEM_PIPELINES': {'pipelines.DocumentDownloaderPipeline': 1},
        'DOWNLOAD_TIMEOUT': 1200,
        'DEPTH_LIMIT': 3,
        'CLOSESPIDER_ITEMCOUNT': 10,
        'CLOSESPIDER_PAGECOUNT': 1000,
    }

    def __init__(self, city='', url='', domain='', **kwargs):
        self.custom_settings['FILES_STORE'] = 'C:/cvut/crawler-new/files/{}'.format(
            city)
        if url != '':
            self.start_urls = [url]
        if domain != '':
            self.allowed_domains = [domain]
        super().__init__(**kwargs)

    def parse(self, response):
        for title in response.css('a::attr(href)'):
            yield response.follow(title.get(), self.save_pdf)

    def save_pdf(self, response):
        if 'pdf' in response.headers.get('content-type').decode('utf-8'):
            loader = ItemLoader(item=DocumentItem())
            loader.add_value('file_urls', response.request.url)
            yield loader.load_item()

        if 'html' in response.headers.get('content-type').decode('utf-8'):
            for title in response.css('a::attr(href)'):
                yield response.follow(title.get(), self.save_pdf)
