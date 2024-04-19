import scrapy, urllib
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from project_1.items import ArticleItem

class NewsSpider12Spider(CrawlSpider):
    name = "news_spider_1.2"
    allowed_domains = ["thanhnien.vn"]
    start_urls = ["https://thanhnien.vn"]
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 20,
    }
    rules = (
        Rule(LinkExtractor(restrict_xpaths =r'//ul[@class = "menu-nav"]/li/a[contains(concat(" ", normalize-space(@class), " "), " nav-link ") and not(contains(@class, "home"))]'), callback="parse_nav", follow=True),
        ) 
    def parse_nav (self, response):
        category = response.url.split('/')[-1].split('.')[0]
        for link in LinkExtractor(restrict_xpaths =r'//*[@id="content"]//h3[contains (@class, "box-title-text")]/a').extract_links(response):
            yield response.follow (link, callback = self.parse_article,meta = {'category': category})
    
    def parse_article (self, response):
        article_item = ArticleItem()
        article_item['url'] = response.url
        article_item['title'] = response.xpath ('//*[@id="content"]//h1/span/text()').extract_first()
        category = response.meta['category']
        article_item['category'] = category
        article_item['author_name'] = response.xpath ('//*[@id="content"]//div[@class="author-info-top"]/a/text()').extract_first()
        article_item['author_email'] = response.xpath ('//*[@id="content"]//div[@class="author-info-top"]//span[@class="email"]/text()').extract_first()
        article_item['publish_date'] = response.xpath ('//*[@id="content"]//div[@class="detail-time"]/div[@data-role="publishdate"]/text()').extract_first()
        yield article_item 