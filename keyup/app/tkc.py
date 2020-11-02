import urllib3
from pyquery import PyQuery as pq
from .models import GroupBuyItem, USER_AGENT


URL = 'https://thekey.company/collections/updates'
EXPECTED_SHIP_DATE_LABEL = 'Expected Ship Date'
STATUS_LABEL = 'Status'

gb_items = []

d = pq(URL, headers={'User-Agent': USER_AGENT})
product_update_items = d('.list-product__list-item')
for product_update_item in product_update_items:
    item_pq = pq(product_update_item)
    item_title_elem = item_pq('.list-product__title')
    item_title = item_title_elem.text()

    item_status_elem = item_pq('.list-product__description .list-product__status')
    item_status = item_status_elem.text().replace(STATUS_LABEL, '').strip()

    expected_ship_date_elem = item_pq('.list-product__description .list-product__ship-date')
    expected_ship_date = expected_ship_date_elem.text()\
            .replace(EXPECTED_SHIP_DATE_LABEL, '').strip()

    gb_item = GroupBuyItem(item_title, expected_ship_date=expected_ship_date,
            status=item_status)
    gb_items.append(gb_item)
