from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django_filters import rest_framework as filters
from .models import Product, Purchase, Sale
from .serializers import ProductSerializer, PurchaseSerializer, SaleSerializer
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce


class ProductFilter(filters.FilterSet):
    """
    Custom filter for the Product model.
    """
    # Filters for model fields
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")  # Case-insensitive match
    unit = filters.CharFilter(field_name="unit", lookup_expr="icontains")  # Case-insensitive match
    notes = filters.CharFilter(field_name="notes", lookup_expr="icontains")  # Case-insensitive match

    # Filters for calculated fields (stock level related)
    min_stock_level = filters.NumberFilter(field_name="stock_level", lookup_expr='gte')
    max_stock_level = filters.NumberFilter(field_name="stock_level", lookup_expr='lte')

    class Meta:
        model = Product
        fields = ["name", "unit", "notes", "min_stock_level", "max_stock_level"]

    @property
    def qs(self):
        """
        Override the default queryset to include annotations for filtering.
        """
        # Start with the parent queryset
        parent_qs = super().qs
        # Annotate with the calculated fields
        annotated_qs = parent_qs.annotate(
            purchased_amount=Coalesce(Sum("purchases__amount"), Value(0)),
            sold_amount=Coalesce(Sum("sales__amount"), Value(0)),
            stock_level=F("purchased_amount") - F("sold_amount")
        )

        # Filter by stock levels
        if 'min_stock_level' in self.data:
            annotated_qs = annotated_qs.filter(stock_level__gte=self.data['min_stock_level'])
        if 'max_stock_level' in self.data:
            annotated_qs = annotated_qs.filter(stock_level__lte=self.data['max_stock_level'])

        return annotated_qs
    
class PurchaseFilter(filters.FilterSet):
    """
    Custom filter for the Purchase model.
    """
    # Filters for date
    date__gte = filters.DateFilter(field_name="date", lookup_expr="gte")  # Greater than or equal to
    date__lte = filters.DateFilter(field_name="date", lookup_expr="lte")  # Less than or equal to

    # Filters for supplier
    supplier = filters.CharFilter(field_name="supplier", lookup_expr="icontains")  # Case-insensitive substring match

    # Filters for product (foreign key)
    product = filters.NumberFilter(field_name="product")  # Exact match for product ID

    # Filters for amount
    amount__lt = filters.NumberFilter(field_name="amount", lookup_expr="lt")  # Less than
    amount__gt = filters.NumberFilter(field_name="amount", lookup_expr="gt")  # Greater than
    amount__range = filters.NumericRangeFilter(field_name="amount")  # Range filter for amount

    class Meta:
        model = Purchase
        fields = ["date", "supplier", "product", "amount"]


class SaleFilter(filters.FilterSet):
    """
    Custom filter for the Sale model.
    """
    # Filters for date
    date__gte = filters.DateFilter(field_name="date", lookup_expr="gte")  # Greater than or equal to
    date__lte = filters.DateFilter(field_name="date", lookup_expr="lte")  # Less than or equal to

    # Filters for customer
    customer = filters.CharFilter(field_name="customer", lookup_expr="icontains")  # Case-insensitive substring match

    # Filters for product (foreign key)
    product = filters.NumberFilter(field_name="product")  # Exact match for product ID

    # Filters for amount
    amount__lt = filters.NumberFilter(field_name="amount", lookup_expr="lt")  # Less than
    amount__gt = filters.NumberFilter(field_name="amount", lookup_expr="gt")  # Greater than
    amount__range = filters.NumericRangeFilter(field_name="amount")  # Range filter for amount

    class Meta:
        model = Sale
        fields = ["date", "customer", "product", "amount"]

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing products.
    """
    queryset = Product.objects.all()  # Base queryset without annotations
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]  # Allow any user to access the API
    filter_backends = [filters.DjangoFilterBackend]  # Enable filtering
    filterset_class = ProductFilter  # Use the custom filter class

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