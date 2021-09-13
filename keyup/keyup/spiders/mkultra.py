import scrapy
from .utils import extract_shipping_date


BASE_URL = "https://mkultra.click"


class MkultraSpider(scrapy.Spider):
    name = 'mkultra'
    allowed_domains = ['mkultra.click']
    start_urls = ['https://mkultra.click/gb/']

    def parse(self, response):
        pages = response.css("nav.pagination")[0].css("a.pagination-link::attr(href)").getall()[:-1]
        for page in pages:
            yield scrapy.Request("{}{}".format(BASE_URL, page), self.parse_gb_list_page)

    def parse_gb_list_page(self, response):
        products = response.css("ul.productGrid li.product")
        for product_elem in products:
            product_url = product_elem.css("h4.card-title a::attr(href)").get()
            yield scrapy.Request(product_url, self.parse_gb_detail_page)

    def parse_gb_detail_page(self, response):
        product_title = response.css("div.productView-product h1.productView-title::text").get()
        product_title = product_title.replace("[GB]", "").replace("[Pre-Sale]", "").strip()
        expected_ship_date = response.css("div.productView-options").xpath('.//p[contains(text(), "Expected shipping")]/text()').get()
        if not expected_ship_date:
            return
        yield {
            "name": product_title,
            "vendor": "MKUltra",
            "expected_ship_date": extract_shipping_date(expected_ship_date)
        }
