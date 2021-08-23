import scrapy
import json


class ValasupplySpider(scrapy.Spider):
    name = 'valasupply'
    allowed_domains = ['vala.supply']
    start_urls = ['https://vala.supply/collections/group-buys/products.json']

    def parse(self, response):
        res_json = json.loads(response.body)
        products = res_json['products']
        for product in products:
            item_name = product['title']
            body_html = product['body_html']
            selector = scrapy.Selector(text=body_html, type="html")

            expected_ship_date_selector = selector.xpath('//*[re:test(text(), "(Expected delivery|Estimated (to ship|ship date))")]')
            expected_ship_date = expected_ship_date_selector.xpath("./strong/text()")
            if expected_ship_date.get() is None:
                expected_ship_date = expected_ship_date_selector.xpath("../strong/text()")

            yield {
                "name": item_name,
                "expected_ship_date": expected_ship_date.get(),
                "vendor": "Vala Supply"
            }