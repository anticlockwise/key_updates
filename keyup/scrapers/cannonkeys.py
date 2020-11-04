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

        return gb_items