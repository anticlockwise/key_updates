import scrapy
import scrapy.http

UPDATE_COLUMN_CELL_XPATH = '//div[@data-pf-type="TabContentWrapper"]//div[@data-pf-type="Column"]'


class NovelkeysSpider(scrapy.Spider):
    name = 'novelkeys'
    allowed_domains = ['novelkeys.xyz']
    start_urls = ['http://novelkeys.xyz/pages/updates']

    def parse(self, response):
        update_cells = response.xpath(UPDATE_COLUMN_CELL_XPATH)
        for cell in update_cells:
            product_url = cell.attrib.get('data-href')
            item_name = cell.xpath('.//h3[@data-pf-type="Heading"][1]/span/text()').get()
            expected_ship_date = cell.xpath('.//h4[@data-pf-type="Heading"]/span[text()="Expected Ship Date:"]/../../../following-sibling::div//text()').get()
            if product_url is None or item_name is None or expected_ship_date is None:
                continue

            yield {
                "name": item_name,
                "url": product_url,
                "expected_ship_date": expected_ship_date,
                "vendor": "Novelkeys"
            }