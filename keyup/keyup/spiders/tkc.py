import scrapy
import scrapy.http


BASE_URL = "https://thekey.company"


class TkcSpider(scrapy.Spider):
    name = 'tkc'
    allowed_domains = ['thekey.company']
    start_urls = ['https://thekey.company/collections/updates/']

    def parse(self, response: scrapy.http.Response):
        update_items = response.css('.list-product__list-item')
        for item in update_items:
            item_name = item.css(".list-product__title::text").get().strip()
            expected_ship_date = item.css('.list-product__ship-date::text').getall()
            product_url = "{}{}".format(BASE_URL, item.css('.grid-product-modal__content a.dialog__button::attr(href)').get())

            if not expected_ship_date:
                continue

            yield {
                "name": item_name,
                "expected_ship_date": expected_ship_date[1].strip(),
                "product_url": product_url
            }