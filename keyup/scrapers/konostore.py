from ..models import GroupBuyItem
from .base import PyQueryBasedScraper
from pyquery import PyQuery as pq
import json


URL = 'https://kono.store/pages/weekly-update'
STORE_NAME = 'Kono'


class KonostoreScraper(PyQueryBasedScraper):
    def _get_url(self):
        return URL

    def _scrape(self, doc):
        updates_wrapper = doc('div.shg-rich-text').eq(2)

        titles = [pq(title).text() for title in updates_wrapper.find('h2')]
        updates = [pq(update).text() for update in updates_wrapper.find('p')]

        gb_items = []
        for title, update_status in zip(titles, updates):
            gb_item = GroupBuyItem(title, STORE_NAME, status=update_status)
            gb_items.append(gb_item)

        return gb_items


if __name__ == '__main__':
    scraper = KonostoreScraper()
    gb_items = scraper.scrape()
    for gb_item in gb_items:
        print(json.dumps(gb_item.__dict__()))
