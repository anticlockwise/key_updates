"""Keyboard Updates

Usage:
  keyup/app.py index
  keyup/app.py merge
  keyup/app.py search <keywords>
"""

from .index.bonsai import BonsaiSearchIndex
from .scrapers import AVAILABLE_SCRAPERS
from .retriever import fetch
from docopt import docopt
import json
import os

if __name__ == '__main__':
    arguments = docopt(__doc__, version="Keyboard Updates 2.0")
    indexer = BonsaiSearchIndex(os.environ['BONSAI_URL'])

    if 'index' in arguments and arguments['index']:
        gb_items = []
        for scraper in AVAILABLE_SCRAPERS:
            scraped_items = scraper.scrape()
            gb_items.extend(scraped_items)
        print("Indexing {} group buy items".format(len(gb_items)))
        indexer.build(gb_items)
    if 'search' in arguments and arguments['search']:
        keywords = arguments['<keywords>']
        print("Searching with keywords: ", keywords)
        results = indexer.search(keywords)
        print(json.dumps(results[0].__dict__()))
    if 'merge' in arguments and arguments['merge']:
        gb_items = fetch()
        gb_items = filter(lambda g: g['type'] == 'keycaps', gb_items)
        for gb_item in gb_items:
            gb_item_name = gb_item['name']
            results = indexer.search(gb_item_name)
            if len(results) > 0:
                print("GB item name: {}".format(gb_item))
                print("GB item in search: {}, GB status: {}".format(results[0].name,
                    results[0].expected_ship_date))