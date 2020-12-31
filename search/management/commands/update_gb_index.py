from django.core.management.base import BaseCommand, CommandError
from search.models import GroupBuyItem
from keyup.scrapers import AVAILABLE_SCRAPERS


class Command(BaseCommand):
    help = "Update the group buy update index"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        gb_items = []
        for scraper in AVAILABLE_SCRAPERS:
            scraped_items = scraper.scrape()
            print("Scraped {} items from {}".format(len(scraped_items), type(scraper)))
            gb_items.extend(scraped_items)
        print("Indexing {} group buy items".format(len(gb_items)))

        for gb_item in gb_items:
            gb_item_model = GroupBuyItem(
                name=gb_item.name,
                store_name=gb_item.store_name,
                expected_ship_date=gb_item.expected_ship_date or "",
                status=gb_item.status or "",
                update_time=gb_item.update_time,
            )
            gb_item_model.save()

        print("Completed indexing of group buy item updates")
