from pyquery import PyQuery as pq
from ..models import GroupBuyItem, USER_AGENT
from .base import PyQueryBasedScraper
from .util import extract_shipping_date


URL = "https://cannonkeys.com/pages/group-buy-status"


class CannonkeysScraper(PyQueryBasedScraper):
    def _get_url(self):
        return URL

    def _scrape(self, doc):
        gb_items = []
        context = {}
        self._traverse(doc("main"), gb_items, context)
        return gb_items

    def _traverse(self, parent, gb_items, context):
        children = parent.children()
        for child in children:
            text = child.text
            if text and text.lower().strip() == "keysets":
                context["groupbuy_title_found"] = True
                continue  # Cutoff early

            child_pq = pq(child)
            if context.get("groupbuy_title_found"):
                if child_pq.is_("h4") or (
                    child_pq.is_("strong")
                    and parent.is_("p")
                    and (parent.text().strip() == text)
                ):
                    gb_item = GroupBuyItem(text, "CannonKeys")
                    gb_items.append(gb_item)
                    context["groupbuy_item_found"] = True
                elif child_pq.is_("p") and context.get("groupbuy_item_found") and text:
                    latest_groupbuy_item = gb_items[-1]
                    latest_groupbuy_item.status = child_pq.text()

                    expected_ship_date = extract_shipping_date(
                        latest_groupbuy_item.name, latest_groupbuy_item.status
                    )
                    latest_groupbuy_item.expected_ship_date = expected_ship_date

                    context["groupbuy_item_found"] = False
            self._traverse(child_pq, gb_items, context)
        pass


if __name__ == "__main__":
    scraper = CannonkeysScraper()
    gb_items = scraper.scrape()
    for gb_item in gb_items:
        print(
            "Title: {}, status: {}, ship date: {}".format(
                gb_item.name, gb_item.status, gb_item.expected_ship_date
            )
        )
