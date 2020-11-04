import os, os.path
import typing
from ..models import GroupBuyItem
from whoosh import index
from whoosh.fields import SchemaClass, TEXT, KEYWORD, ID, STORED, DATETIME
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser


def create_index_dir(dir_path, schema):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    ix = index.create_in(dir_path, schema)
    return ix


def open_index_dir(dir_path):
    ix = index.open_dir(dir_path)
    return ix


class GroupBuyItemSchema(SchemaClass):
    name = TEXT(stored=True)
    store_name = TEXT(stored=True)
    expected_ship_date = TEXT(stored=True)
    status = TEXT(stored=True)


class SearchIndex:
    def build(self, gb_items):
        pass

    def search(self, keywords):
        pass


class WhooshSearchIndex(SearchIndex):
    def __init__(self, ix: index.Index):
        self._ix = ix

    def build(self, gb_items: typing.List[GroupBuyItem]):
        writer = self._ix.writer()
        for gb_item in gb_items:
            print("Indexing {} group buy item".format(gb_item.name))
            writer.add_document(
                name=gb_item.name,
                store_name=gb_item.store_name,
                expected_ship_date=gb_item.expected_ship_date,
                status=gb_item.status
            )
        writer.commit()

    def search(self, keywords):
        qp = QueryParser("name", schema=GroupBuyItemSchema())
        q = qp.parse(keywords)

        converted_results = []
        with self._ix.searcher() as searcher:
            results = searcher.search(q, limit=10)
            converted_results.extend([GroupBuyItem(result["name"], result["store_name"],
                expected_ship_date=result.get("expected_ship_date"),
                status=result.get("status"))
                for result in results])
        return converted_results