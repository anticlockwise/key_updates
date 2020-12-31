from .base import PyQueryBasedScraper
from ..models import GroupBuyItem, USER_AGENT
from .util import extract_shipping_date
from pyquery import PyQuery as pq
import json


BASE_URL = "https://dixiemech.com"
URL = "{}/news".format(BASE_URL)


class DixieMechScraper(PyQueryBasedScraper):
    def _get_url(self):
        d = pq(URL, headers={"User-Agent": USER_AGENT})
        latest_update_link = d("a.BlogList-item-title").eq(0)
        latest_update_url = "{}{}".format(BASE_URL, latest_update_link.attr("href"))
        return latest_update_url

    def _scrape(self, doc):
        gb_items = []
        context = {}
        self._traverse(doc, gb_items, context)
        return gb_items

    def _traverse(self, parent, gb_items, context):
        children = parent.children()
        for child in children:
            text = child.text
            if text and text.lower().strip() == "groupbuy updates":
                context["groupbuy_title_found"] = True
                return  # Cutoff early
            if text and text.lower().strip() == "services":
                context["groupbuy_title_found"] = False
                return  # Cutoff early

            if context.get("groupbuy_title_found"):
                if parent.is_("h2"):
                    gb_item = GroupBuyItem(text, "DixieMech")
                    gb_items.append(gb_item)
                    context["groupbuy_item_found"] = True
                elif parent.is_("h3"):
                    latest_groupbuy_item = gb_items[-1]
                    latest_groupbuy_item.status = text
                elif pq(child).is_("p") and context.get("groupbuy_item_found") and text:
                    latest_groupbuy_item = gb_items[-1]
                    expected_ship_date = extract_shipping_date(
                        latest_groupbuy_item.name, text
                    )
                    latest_groupbuy_item.expected_ship_date = expected_ship_date
                    context['groupbuy_item_found'] = False
            self._traverse(pq(child), gb_items, context)
        pass


if __name__ == "__main__":
    scraper = DixieMechScraper()
    gb_items = scraper.scrape()
    for gb_item in gb_items:
        print(
            "Title: {}, ship date: {}".format(gb_item.name, gb_item.expected_ship_date)
        )
