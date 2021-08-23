import scrapy
import collections


class KonostoreSpider(scrapy.Spider):
    name = 'konostore'
    allowed_domains = ['kono.store']
    start_urls = ['https://kono.store/pages/weekly-update']

    def parse(self, response):
        columns = response.css(".shg-fw .shg-rich-text")
        items = collections.defaultdict(list)
        for column in columns:
            cur_item = ""
            for elem in column.xpath("./*[not(self::h1)]"):
                elem_content = elem.get().strip()
                if elem_content.startswith("<h2>"):
                    item_name = elem.xpath("./descendant::text()").get()
                    cur_item = item_name
                elif elem_content.startswith("<p>"):
                    description = elem.xpath("./descendant::text()").get()
                    items[cur_item].append(description)

        for item_name, description in items.items():
            yield {
                "name": item_name,
                "expected_ship_date": "".join(description),
                "vendor": "Kono Store"
            }