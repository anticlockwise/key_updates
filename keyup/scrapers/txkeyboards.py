from .base import PyQueryBasedScraper
from ..models import GroupBuyItem
from .util import normalize_date
from pyquery import PyQuery as pq
import json


URL = "https://www.us.txkeyboards.com/pages/group-buy-status"
STORE_NAME = "Tx Keyboards"


class TxKeyboardsScraper(PyQueryBasedScraper):
    def _get_url(self):
        return URL

    def _scrape(self, doc):
        gb_items = []

        update_table = doc("div.grid > .grid__item > .rte > table")
        rows = update_table("tr")
        for i, row in enumerate(rows):
            if i == 0:
                continue

            row_pq = pq(row)
            title_cell = row_pq("td").eq(0)
            status_cell = row_pq("td").eq(1)
            expected_ship_date_cell = row_pq("td").eq(2)

            gb_item = GroupBuyItem(
                title_cell.text(),
                STORE_NAME,
                status=status_cell.text(),
                expected_ship_date=normalize_date(expected_ship_date_cell.text()),
            )
            gb_items.append(gb_item)

        return gb_items


if __name__ == "__main__":
    scraper = TxKeyboardsScraper()
    gb_items = scraper.scrape()
    for gb_item in gb_items:
        print(json.dumps(gb_item.__dict__()))
