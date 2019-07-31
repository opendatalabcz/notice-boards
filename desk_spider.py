import scrapy
import re
from urllib.parse import urlparse


class DeskSpider(scrapy.Spider):
    name = 'city_spider'
    start_urls = [
        'https://cs.wikipedia.org/wiki/Seznam_m%C4%9Bst_v_%C4%8Cesku']

    def parse(self, response):
        for city in response.css('table>tbody>tr>td>ul>li>a::attr(href)'):
            yield response.follow("https://cs.wikipedia.org/{}".format(city.get()), self.extract_city_page)

    def extract_city_page(self, response):
        name = response.css('h1#firstHeading::text').get()
        for td in response.css('table.infobox>tbody>tr>td'):
            if 'web:' in td.get():
                yield response.follow(td.css('span.url>a::attr(href)').get(), self.extract_edesk, meta={'city_name': name})

    def extract_edesk(self, response):
        result = {'city': response.meta['city_name'],
                  'domain': [], 'desk': []}
        result['desk'].append(response.url)
        result['domain'].append(urlparse(response.url).netloc)
        # for link in response.css('a'):
        #     if re.search('deska', link.get(), re.IGNORECASE) and not result['desk']:
        #         absolute_url = response.urljoin(
        #             link.css('::attr(href)').get())
        #         result['desk'].append(absolute_url)
        #         result['domain'].append(urlparse(absolute_url).netloc)

        yield result
