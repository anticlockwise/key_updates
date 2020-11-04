"""Keyboard Updates

Usage:
  keyup/app.py index
  keyup/app.py search <keywords>
"""

from .index.base import WhooshSearchIndex, GroupBuyItemSchema, create_index_dir, open_index_dir
from .scrapers import AVAILABLE_SCRAPERS
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