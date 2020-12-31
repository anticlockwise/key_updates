from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import GroupBuyItem


@registry.register_document
class GroupBuyItemDocument(Document):
    class Index:
        name = 'groupbuy_items'

    class Django:
        model = GroupBuyItem

        fields = [
            'name',
            'store_name',
            'expected_ship_date',
            'status',
            'update_time'
        ]