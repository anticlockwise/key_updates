from .base import PyQueryBasedScraper
from ..models import GroupBuyItem
from pyquery import PyQuery as pq
import json


URL = 'https://thekey.company/collections/updates'
EXPECTED_SHIP_DATE_LABEL = 'Expected Ship Date'
STATUS_LABEL = 'Status'
STORE_NAME = 'The Key Company'


class TkcScraper(PyQueryBasedScraper):
    def _get_url(self):
        return URL

    def _scrape(self, doc):
        gb_items = []

        product_update_items = doc('.list-product__list-item')
        for product_update_item in product_update_items:
            item_pq = pq(product_update_item)
            item_title_elem = item_pq('.list-product__title')
            item_title = item_title_elem.text()

            item_status_elem = item_pq('.list-product__description .list-product__status')
            item_status = item_status_elem.text().replace(STATUS_LABEL, '').strip()

            expected_ship_date_elem = item_pq('.list-product__description .list-product__ship-date')
            expected_ship_date = expected_ship_date_elem.text()\
                    .replace(EXPECTED_SHIP_DATE_LABEL, '').strip()

            gb_item = GroupBuyItem(item_title, STORE_NAME, expected_ship_date=expected_ship_date,
                    status=item_status)
            gb_items.append(gb_item)

        return gb_items


if __name__ == '__main__':
    scraper = TkcScraper()
    gb_items = scraper.scrape()
    for gb_item in gb_items:
        print(json.dumps(gb_item.__dict__()))
