from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django_filters import rest_framework as filters
from .models import Product, Purchase, Sale
from .serializers import ProductSerializer, PurchaseSerializer, SaleSerializer
from django.db.models import F, Sum, Value
from django.db.models.functions import Coalesce

class ProductFilter(filters.FilterSet):
    """
    Define filters for the Product model.
    """
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")  # Case-insensitive substring match
    stock_level__lt = filters.NumberFilter(field_name="stock_level", lookup_expr="lt")  # Less than
    stock_level__gt = filters.NumberFilter(field_name="stock_level", lookup_expr="gt")  # Greater than
    unit = filters.CharFilter(field_name="unit", lookup_expr="iexact")  # Exact match (case-insensitive)

    class Meta:
        model = Product
        fields = ["name", "stock_level", "unit"]

class PurchaseFilter(filters.FilterSet):
    """
    Define filters for the Purchase model.
    """
    date__gte = filters.DateFilter(field_name="date", lookup_expr="gte")  # Greater than or equal to
    date__lte = filters.DateFilter(field_name="date", lookup_expr="lte")  # Less than or equal to
    supplier = filters.CharFilter(field_name="supplier", lookup_expr="icontains")  # Case-insensitive substring match
    product = filters.NumberFilter(field_name="product")  # Exact match for product ID
    amount__lt = filters.NumberFilter(field_name="amount", lookup_expr="lt")  # Less than
    amount__gt = filters.NumberFilter(field_name="amount", lookup_expr="gt")  # Greater than

    class Meta:
        model = Purchase
        fields = ["date", "supplier", "product", "amount"]

class SaleFilter(filters.FilterSet):
    """
    Define filters for the Sale model.
    """
    date__gte = filters.DateFilter(field_name="date", lookup_expr="gte")  # Greater than or equal to
    date__lte = filters.DateFilter(field_name="date", lookup_expr="lte")  # Less than or equal to
    customer = filters.CharFilter(field_name="customer", lookup_expr="icontains")  # Case-insensitive substring match
    product = filters.NumberFilter(field_name="product")  # Exact match for product ID
    amount__lt = filters.NumberFilter(field_name="amount", lookup_expr="lt")  # Less than
    amount__gt = filters.NumberFilter(field_name="amount", lookup_expr="gt")  # Greater than

    class Meta:
        model = Sale
        fields = ["date", "customer", "product", "amount"]

class ProductViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing products with filtering support.
    """
    queryset = Product.objects.annotate(
        purchased_amount=Coalesce(Sum('purchases__amount'), Value(0)),  # Total purchased amount
        sold_amount=Coalesce(Sum('sales__amount'), Value(0)),           # Total sold amount
        stock_level=F('purchased_amount') - F('sold_amount')            # Stock level (calculated)
    )
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter

class PurchaseViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing purchases with filtering support.
    """
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [AllowAny]  # Allow any user to access the API
    filter_backends = [filters.DjangoFilterBackend]  # Enable filtering
    filterset_class = PurchaseFilter  # Use the custom filter class

class SaleViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing sales with filtering support.
    """
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [AllowAny]  # Allow any user to access the API
    filter_backends = [filters.DjangoFilterBackend]  # Enable filtering
    filterset_class = SaleFilter  # Use the custom filter class