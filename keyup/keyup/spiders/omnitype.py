import scrapy


BASE_URL = "https://omnitype.com"


class OmnitypeSpider(scrapy.Spider):
    name = 'omnitype'
    allowed_domains = ['omnitype.com']
    start_urls = ['https://omnitype.com/blogs/timelines']

    def parse(self, response):
        pagination_elem = response.css(".Pagination__Nav").xpath("./*/text()").getall()
        for page in pagination_elem:
            yield scrapy.Request("{}?page={}".format(self.start_urls[0], page), callback=self.parse_timeline)

    def parse_timeline(self, response):
        article_items = response.css(".ArticleItem")
        for article_item in article_items:
            item_name = article_item.css(".ArticleItem__Title a::text").get()
            expected_ship_date = article_item.css(".ArticleItem__Excerpt::text").get()
            yield {
                "name": item_name,
                "expected_ship_date": expected_ship_date
            }