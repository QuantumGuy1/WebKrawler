from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy_proxies import Proxies


class MySpider(CrawlSpider): #class inherits from scrapy.spiders
    name = 'mycrawler'
    allowed_domains = ["toscrape.com"]
    start_urls = ['http://books.toscrape.com/']


    rules = (
        Rule(LinkExtractor(allow='catalogue/category')),
        Rule(LinkExtractor(allow='catalogue', deny='category'), callback ="parse_item")
    )

    def __init__(self, *args, **kwargs):
        # Initialize the spider with proxy settings
        super(MySpider, self).__init__(*args, **kwargs)
        self.proxies = Proxies()

    def start_requests(self):
        # Generate requests using proxy rotation
        for url in self.start_urls:
            proxy = self.proxies.random_proxy()
            yield scrapy.Request(url, callback=self.parse, meta={'proxy': proxy})

    def parse_item(self,response):
        yield {
            "title": response.css(".product_main h1::text").get(),
            "price": response.css(".price_color::text").get(),
            "availability": response.css(".availability::text")[1].get().replace("\n","").replace(" ","")
        }

