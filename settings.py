COOKIES_ENABLED = False
RETRY_ENABLED = False
REACTOR_THREADPOOL_MAXSIZE = 600
CONCURRENT_ITEMS = 100
CONCURRENT_REQUESTS = 300
CONCURRENT_REQUESTS_PER_DOMAIN = 60
LOG_LEVEL = 'INFO'
EXTENSIONS = {
    'scrapy.telnet.TelnetConsole': None,
    'scrapy.extensions.closespider.CloseSpider': 500,
}
