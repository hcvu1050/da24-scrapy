import scrapy, urllib
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from project_1.items import ArticleItem

class NewsSpider12Spider(CrawlSpider):
    name = "news_spider_1.2"
    allowed_domains = ["thanhnien.vn"]
    start_urls = ["https://thanhnien.vn"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths =r'//ul[@class = "menu-nav"]/li/a[contains(concat(" ", normalize-space(@class), " "), " nav-link ") and not(contains(@class, "home"))]'), callback="parse_nav", follow=True),
        # Rule(LinkExtractor(restrict_xpaths =r'//*[@id="content"]//h3[contains (@class, "box-title-text")]/a'), callback="parse_article", follow=True),
        ) 
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 20,
    }
    def parse_nav (self, response):
        # article_rurls = response.xpath('//*[@id="content"]//h3[contains (@class, "box-title-text")]/a/@href').extract()
        category = response.url.split('/')[-1].split('.')[0]
        # for article_rurl in article_rurls[:3]:
        #     article_url = urllib.parse.urljoin (response.url, article_rurl)
        #     yield response.follow (article_url, callback = self.parse_article, meta = {'category' : category})
        for link in LinkExtractor(restrict_xpaths =r'//*[@id="content"]//h3[contains (@class, "box-title-text")]/a').extract_links(response):
            yield response.follow (link, callback = self.parse_article,meta = {'category': category})
    
    def parse_article (self, response):
        article_item = ArticleItem()
        article_item['url'] = response.url
        article_item['title'] = response.css ('h1.detail-title span::text').get()
        category = response.meta['category']
        article_item['category'] = category
        article_item['author_name'] = response.css('.detail-author .author-info-top a::text').get()
        article_item['author_email'] = response.css ('.detail-author .author-info-top span.email::text').get()
        article_item['publish_date'] = response.css(' div[data-role="publishdate"]::text').get()
        yield article_item 