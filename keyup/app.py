"""Keyboard Updates

Usage:
  keyup/app.py index
  keyup/app.py merge
  keyup/app.py search <keywords>
"""

from .index.base import WhooshSearchIndex, GroupBuyItemSchema, create_index_dir, open_index_dir
from .scrapers import AVAILABLE_SCRAPERS
from .retriever import fetch
from docopt import docopt
import json

if __name__ == '__main__':
    arguments = docopt(__doc__, version="Keyboard Updates 2.0")
    schema = GroupBuyItemSchema()
    if 'index' in arguments and arguments['index']:
        ix = create_index_dir("index/keyboard_updates", schema)
        indexer = WhooshSearchIndex(ix)
        gb_items = []
        for scraper in AVAILABLE_SCRAPERS:
            scraped_items = scraper.scrape()
            gb_items.extend(scraped_items)
        print("Indexing {} group buy items".format(len(gb_items)))
        indexer.build(gb_items)
    if 'search' in arguments and arguments['search']:
        ix = open_index_dir("index/keyboard_updates")
        indexer = WhooshSearchIndex(ix)
        keywords = arguments['<keywords>']
        print("Searching with keywords: ", keywords)
        results = indexer.search(keywords)
        print(json.dumps(results[0].__dict__()))
    if 'merge' in arguments and arguments['merge']:
        ix = open_index_dir("index/keyboard_updates")
        indexer = WhooshSearchIndex(ix)
        gb_items = fetch()
        gb_items = filter(lambda g: g['type'] == 'keycaps', gb_items)
        for gb_item in gb_items:
            gb_item_name = gb_item['name']
            results = indexer.search(gb_item_name)
            if len(results) > 0:
                print("GB item name: {}".format(gb_item_name))
                print("GB item in search: {}, GB status: {}".format(results[0].name,
                    results[0].expected_ship_date))