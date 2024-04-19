import scrapy, urllib
from project_1.items import ArticleItem

class NewsSpider0Spider(scrapy.Spider):
    name = "news_spider_1"
    allowed_domains = ["thanhnien.vn"]
    start_urls = ["https://thanhnien.vn/"]

    def parse(self, response):
        # get nav selectors
        nav_rurls = response.xpath ('//ul[@class = "menu-nav"]/li/a[contains(concat(" ", normalize-space(@class), " "), " nav-link ") and not(contains(@class, "home"))]/@href').extract()
        for nav_rurl in nav_rurls[:3]:
            nav_url = urllib.parse.urljoin (response.url, nav_rurl )
            yield response.follow (nav_url, callback = self.parse_nav)
            
    def parse_nav (self, response):
        article_rurls = response.xpath('//*[@id="content"]//h3[contains (@class, "box-title-text")]/a/@href').extract()
        category = response.url.split('/')[-1].split('.')[0]
        for article_rurl in article_rurls[:3]:
            article_url = urllib.parse.urljoin (response.url, article_rurl)
            yield response.follow (article_url, callback = self.parse_article, meta = {'category' : category})
        
    def parse_article (self, response):
        article_item = ArticleItem()
        category = response.meta['category']
        article_item['category'] = category
        article_item['url'] = response.url
        article_item['title'] = response.css ('h1.detail-title span::text').get()
        article_item['author_name'] = response.css('.detail-author .author-info-top a::text').get()
        article_item['author_email'] = response.css ('.detail-author .author-info-top span.email::text').get()
        article_item['publish_date'] = response.css(' div[data-role="publishdate"]::text').get()
        yield article_item 