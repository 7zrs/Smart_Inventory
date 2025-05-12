from rest_framework import serializers
from .models import Stock, Shipment

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'product', 'quantity', 'last_updated']
        read_only_fields = ['id', 'last_updated']

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = ['id', 'product', 'quantity', 'received_on', 'notes']
        read_only_fields = ['id', 'received_on']