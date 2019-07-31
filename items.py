import scrapy


class DocumentItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    extension = scrapy.Field()
