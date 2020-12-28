import re
import json
import hashlib
from .base import SearchIndex
from ..models import GroupBuyItem
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


GB_ITEMS_INDEX = "gb-items"


class BonsaiSearchIndex(SearchIndex):
    def __init__(self, bonsai_url):
        self._bonsai_url = bonsai_url
        self._es = Elasticsearch([self._bonsai_url], use_ssl=True)

    def build(self, gb_items):
        index_exist = self._es.indices.exists(GB_ITEMS_INDEX)
        if not index_exist:
            self._es.indices.create(index=GB_ITEMS_INDEX)

        gb_item_docs = [
            {
                "_index": GB_ITEMS_INDEX,
                "_type": "document",
                "_id": hashlib.sha1(gb_item.name.encode("utf-8")).hexdigest(),
                "name": gb_item.name,
                "store_name": gb_item.store_name,
                "status": gb_item.status,
                "expected_ship_date": gb_item.expected_ship_date,
                "update_time": gb_item.update_time
            }
            for gb_item in gb_items
        ]

        print("Number of docs: {}".format(len(gb_item_docs)))

        success, failures = bulk(self._es, gb_item_docs)
        if failures:
            print("failed: {}".format(failures))

    def search(self, keywords):
        body = {"query": {"match": {"name": {"query": keywords}}}}
        results = self._es.search(index=GB_ITEMS_INDEX, body=json.dumps(body))
        hits = results['hits']
        inner_hits = hits['hits']
        return [GroupBuyItem(**r['_source']) for r in inner_hits if r['_score'] > 5]