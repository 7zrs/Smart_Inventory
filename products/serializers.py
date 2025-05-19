from rest_framework import serializers
from .models import Product, Sale, Purchase

class ProductSerializer(serializers.ModelSerializer):
    purchased_amount = serializers.SerializerMethodField()
    sold_amount = serializers.SerializerMethodField()
    stock_level = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'unit', 'notes', 'purchased_amount', 'sold_amount', 'stock_level']

    def get_purchased_amount(self, obj):
        return obj.purchased_amount()

    def get_sold_amount(self, obj):
        return obj.sold_amount()

    def get_stock_level(self, obj):
        return obj.stock_level()
    
class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ['id', 'date', 'supplier', 'product', 'amount', 'notes']

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'date', 'customer', 'product', 'amount', 'notes']