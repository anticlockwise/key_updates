import scrapy


class MekiboSpider(scrapy.Spider):
    name = 'mekibo'
    allowed_domains = ['mekibo.com']
    start_urls = ['http://mekibo.com/pages/group-buy-status']

    def parse(self, response):
        tables = response.xpath("//table")
        for table in tables:
            rows = table.xpath(".//tr[position()>1]")
            for row in rows:
                cells = row.xpath("./td")
                item_name = cells[0].xpath(".//text()").get()

                if item_name and item_name.strip():
                    expected_ship_date = cells[2].xpath(".//text()").get()
                    yield {
                        "name": item_name,
                        "expected_ship_date": expected_ship_date
                    }