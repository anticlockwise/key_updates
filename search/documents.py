from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import GroupBuyItem


@registry.register_document
class GroupBuyItemDocument(Document):
    name = fields.TextField(fields={"raw": fields.KeywordField()})
    store_name = fields.KeywordField()
    expected_ship_date = fields.KeywordField()

    class Index:
        name = "groupbuy_items"

    class Django:
        model = GroupBuyItem

        fields = ["status", "update_time"]
