from .base import PyQueryBasedScraper
from ..models import GroupBuyItem, USER_AGENT
from pyquery import PyQuery as pq
import json


BASE_URL = 'https://dixiemech.com'
URL = '{}/news'.format(BASE_URL)


class DixieMechScraper(PyQueryBasedScraper):
    def _get_url(self):
        d = pq(URL, headers={'User-Agent': USER_AGENT})
        latest_update_link = d("a.BlogList-item-title").eq(0)
        latest_update_url = '{}{}'.format(BASE_URL, latest_update_link.attr("href"))
        return latest_update_url

    def _scrape(self, doc):
        print(doc('.sqs-layout[data-type="item"] > .row > .col > .sqs-block.html-block').eq(5))
        return []


if __name__ == '__main__':
    scraper = DixieMechScraper()
    gb_items = scraper.scrape()
    for gb_item in gb_items:
        print(json.dumps(gb_item.__dict__()))
