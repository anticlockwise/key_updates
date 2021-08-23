import scrapy


class CannonkeysSpider(scrapy.Spider):
    name = 'cannonkeys'
    allowed_domains = ['cannonkeys.com']
    start_urls = ['http://cannonkeys.com/pages/group-buy-status']

    def parse(self, response):
        update_wrapper = response.xpath('//h1[text()="KEYBOARDS"]/following-sibling::div')
        update_items = update_wrapper.css(".so-tab")
        for update_item in update_items:
            label_elem = update_item.xpath("./label")
            item_name = label_elem.xpath("./strong/span/text()").get()
            expected_ship_date = label_elem.xpath('./strong[contains(text(), "ETA")]/following-sibling::text()').get()
            if item_name:
                yield {
                    "name": item_name,
                    "expected_ship_date": expected_ship_date.strip()
                }