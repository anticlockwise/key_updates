from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from .documents import GroupBuyItemDocument
from .models import GroupBuyItemSerializer, GroupBuyItem
from django_elasticsearch_dsl_drf.filter_backends import (
    SearchFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

# Create your views here.


class GroupBuyItemReadonlyViewSet(DocumentViewSet):
    document = GroupBuyItemDocument
    serializer_class = GroupBuyItemSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = "name"
    filter_backends = [
        OrderingFilterBackend,
        DefaultOrderingFilterBackend,
        SearchFilterBackend,
    ]
    search_fields = ("name",)
    ordering_fields = {"name": "name.raw", "expected_ship_date": "expected_ship_date"}
    ordering = (
        "_score",
        "update_time",
        "name.raw",
        "expected_ship_date",
    )
