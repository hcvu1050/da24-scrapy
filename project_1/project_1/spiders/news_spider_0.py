import scrapy
from project_1.items import ArticleItem

class NewsSpider0Spider(scrapy.Spider):
    name = "news_spider_0"
    allowed_domains = ["thanhnien.vn"]
    start_urls = ["https://thanhnien.vn/dong-su-kien/xung-dot-nga-ukraine-165.htm/"]

    def parse(self, response):
        articles = response.css ('div.box-category-item')[:5]
        for article in articles: 
            rurl = article.css ('::attr(href)').get()
            article_url = "https://thanhnien.vn/" + rurl
            yield response.follow (article_url, callback = self.parse_article)
        # (first page only)
        
    def parse_article (self, response):
        article_item = ArticleItem()
        article_item['url'] = response.url
        article_item['title'] = response.css ('h1.detail-title span::text').get()
        article_item['author_name'] = response.css('.detail-author .author-info-top a::text').get()
        article_item['author_email'] = response.css ('.detail-author .author-info-top span.email::text').get()
        article_item['publish_date'] = response.css(' div[data-role="publishdate"]::text').get()
        yield article_item 
        
        