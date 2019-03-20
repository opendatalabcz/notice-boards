import scrapy


class CitySpider(scrapy.Spider):
    name = 'cities'
    start_urls = [
        'https://cs.wikipedia.org/wiki/Seznam_m%C4%9Bst_v_%C4%8Cesku']

    def parse(self, responce):
        for city in responce.css('table>tbody>tr>td>ul>li>a::attr(href)'):
            yield {'city-page': "https://cs.wikipedia.org/{}".format(city.get())}
