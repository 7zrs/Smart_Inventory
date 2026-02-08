from rest_framework import serializers
from .models import Product, Purchase, Sale


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.
    Includes calculated fields `purchased_amount`, `sold_amount`, and `stock_level`.
    """

    purchased_amount = serializers.IntegerField(read_only=True)
    sold_amount = serializers.IntegerField(read_only=True)
    stock_level = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "unit",
            "notes",
            "purchased_amount",
            "sold_amount",
            "stock_level",
        ]

    def validate(self, data):
        """
        Custom validation to ensure unique product names and units.
        """
        name = data.get("name")
        unit = data.get("unit")

        # Check for duplicate products based on name and unit
        if Product.objects.filter(name=name, unit=unit).exists():
            raise serializers.ValidationError(
                "A product with this name and unit already exists."
            )
        return data


class PurchaseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Purchase model.
    """

    class Meta:
        model = Purchase
        fields = ["id", "date", "supplier", "product", "amount", "notes"]

    def validate(self, data):
        """
        Custom validation to ensure purchase amount is greater than zero.
        """
        amount = data.get("amount")
        if amount <= 0:
            raise serializers.ValidationError(
                "Purchase amount must be greater than zero."
            )
        return data


class SaleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Sale model.
    """

    class Meta:
        model = Sale
        fields = ["id", "date", "customer", "product", "amount", "notes"]

    def validate(self, data):
        """
        Custom validation to ensure sale amount does not exceed stock level.
        """
        product = data.get("product")
        amount = data.get("amount")

        # Calculate stock level - stock_level is a method on Product model
        stock_level_attr = getattr(product, "stock_level", None)
        stock_level = stock_level_attr() if callable(stock_level_attr) else stock_level_attr
        if amount > stock_level:
            raise serializers.ValidationError(
                f"Cannot sell {amount} {product.unit}. Only {stock_level} {product.unit} available."
            )
        return data
