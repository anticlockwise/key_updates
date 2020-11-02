from pyquery import PyQuery as pq
from ..models import GroupBuyItem, USER_AGENT
from .base import PyQueryBasedScraper


URL = 'https://cannonkeys.com/pages/group-buy-status'


class CannonkeysScraper(PyQueryBasedScraper):
    def _get_url(self):
        return URL

    def _scrape(self, doc):
        gb_items = []

        gb_status_div = doc('div.rte')
        children = gb_status_div.contents()
        for child in children:
            if str(child).strip():
                if child.tag == 'h4':
                    print(pq(child).text())
                elif child.tag == 'p':
                    title_elem = pq(child).find('strong')
                    if title_elem:
                        print(title_elem.text())
