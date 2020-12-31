from django.db import models
from rest_framework import serializers
from keyup.models import GroupBuyItem

# Create your models here.
class GroupBuyItem(models.Model):
    name = models.CharField(max_length=500)
    store_name = models.CharField(max_length=200)
    expected_ship_date = models.CharField(max_length=200)
    status = models.TextField()
    update_time = models.DateTimeField()


class GroupBuyItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupBuyItem
        fields = ["name", "store_name", "expected_ship_date", "status", "update_time"]
        read_only_fields = [
            "name",
            "store_name",
            "expected_ship_date",
            "status",
            "update_time",
        ]
