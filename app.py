"""Keyboard Updates

Usage:
  keyup/app.py index
  keyup/app.py merge
  keyup/app.py search <keywords>
"""

from keyup.index.bonsai import BonsaiSearchIndex
from keyup.scrapers import AVAILABLE_SCRAPERS
from keyup.retriever import fetch
from docopt import docopt
import datetime
import datefinder
import json
import os

if __name__ == "__main__":
    arguments = docopt(__doc__, version="Keyboard Updates 2.0")
    indexer = BonsaiSearchIndex(os.environ["BONSAI_URL"])

    if "index" in arguments and arguments["index"]:
        gb_items = []
        for scraper in AVAILABLE_SCRAPERS:
            scraped_items = scraper.scrape()
            print("Scraped {} items from {}".format(len(scraped_items), type(scraper)))
            gb_items.extend(scraped_items)
        print("Indexing {} group buy items".format(len(gb_items)))
        indexer.build(gb_items)
    if "search" in arguments and arguments["search"]:
        keywords = arguments["<keywords>"]
        print("Searching with keywords: ", keywords)
        results = indexer.search(keywords)
        print(json.dumps(results[0].__dict__()))
    if "merge" in arguments and arguments["merge"]:
        now = datetime.datetime.now()
        gb_items = fetch()
        gb_items = filter(lambda g: g["type"] == "keycaps" and g["endDate"], gb_items)
        for gb_item in gb_items:
            end_date = gb_item["endDate"]
            parsed_end_dates = list(datefinder.find_dates(end_date))
            parsed_end_date = parsed_end_dates[0] if parsed_end_dates else None
            if (
                parsed_end_date
                and parsed_end_date < now
                and (now - parsed_end_date).days <= 540
            ):
                gb_item_name = gb_item["name"]
                results = indexer.search(gb_item_name)
                if len(results) > 0:
                    print("GB item name: {}, end date: {}".format(gb_item['name'], gb_item['endDate']))
                    print(
                        "GB item in search: {}, GB status: {}".format(
                            results[0].name, results[0].expected_ship_date
                        )
                    )
