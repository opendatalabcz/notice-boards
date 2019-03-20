import scrapy
import re


class CitySpider(scrapy.Spider):
    name = 'cities'
    start_urls = [
        'https://cs.wikipedia.org/wiki/Seznam_m%C4%9Bst_v_%C4%8Cesku']

    def parse(self, response):
        for city in response.css('table>tbody>tr>td>ul>li>a::attr(href)'):
            yield response.follow("https://cs.wikipedia.org/{}".format(city.get()), self.extract_city_page)

    def extract_city_page(self, response):
        for td in response.css('table.infobox>tbody>tr>td'):
            if 'web:' in td.get():
                yield response.follow(td.css('span.url>a::attr(href)').get(),
                                      self.extract_official_board)

    def extract_official_board(self, response):
        result = {'city-web': response.request.url, 'desk': []}

        for link in response.css('a'):
            if re.search('deska', link.get(), re.IGNORECASE):
                result['desk'].append(link.css('::attr(href)').get())

        yield result
