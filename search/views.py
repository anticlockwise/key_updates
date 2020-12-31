from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from .documents import GroupBuyItemDocument
from .models import GroupBuyItemSerializer, GroupBuyItem

# Create your views here.


class GroupBuyItemListView(ListAPIView):
    serializer_class = GroupBuyItemSerializer

    def get_queryset(self):
        groupbuy_item_name = self.request.query_params.get("groupbuy_item_name", None)
        documents = GroupBuyItemDocument.search().query(
            "match", name=groupbuy_item_name
        )
        return documents.to_queryset()