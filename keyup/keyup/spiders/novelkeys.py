import scrapy
import scrapy.http


BASE_URL = "https://novelkeys.com"


class NovelkeysSpider(scrapy.Spider):
    name = 'novelkeys'
    allowed_domains = ['novelkeys.com']
    start_urls = ['https://novelkeys.com/pages/Product-Updates']

    def parse(self, response):
        update_links = response.css("a.preorder-timeline-link")
        for cell in update_links:
            product_url = BASE_URL + cell.attrib.get('href')
            item_name = cell.css('h2.preorder-timeline-title::text').get()
            expected_ship_date = cell.xpath('.//p/b[contains(text(), "Estimated Arrival")]/../text()').get()
            if product_url is None or item_name is None or expected_ship_date is None:
                continue

            yield {
                "name": item_name,
                "url": product_url,
                "expected_ship_date": expected_ship_date.strip(),
                "vendor": "Novelkeys"
            }