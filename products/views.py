from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters
from .models import Product, Purchase, Sale
from .serializers import ProductSerializer, PurchaseSerializer, SaleSerializer
from django.db.models import Sum, F, Value
from django.db.models.functions import Coalesce
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class ProductFilter(filters.FilterSet):
    """
    Custom filter for the Product model.
    """

    # Filters for model fields
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    unit = filters.CharFilter(field_name="unit", lookup_expr="icontains")
    notes = filters.CharFilter(field_name="notes", lookup_expr="icontains")

    # Filters for calculated fields (stock level related)
    min_stock_level = filters.NumberFilter(field_name="stock_level", lookup_expr="gte")
    max_stock_level = filters.NumberFilter(field_name="stock_level", lookup_expr="lte")

    class Meta:
        model = Product
        fields = ["name", "unit", "notes", "min_stock_level", "max_stock_level"]

    @property
    def qs(self):
        """
        Override the default queryset to include annotations for filtering.
        Using distinct=True prevents the duplication of amounts when joining
        across multiple relationships.
        """
        parent_qs = super().qs

        # Annotate with the calculated fields using distinct=True
        annotated_qs = parent_qs.annotate(
            purchased_amount=Coalesce(
                Sum("purchases__amount", distinct=True), Value(0)
            ),
            sold_amount=Coalesce(Sum("sales__amount", distinct=True), Value(0)),
        ).annotate(stock_level=F("purchased_amount") - F("sold_amount"))

        # No need for manual filtering here; DjangoFilterBackend handles it.
        return annotated_qs


class PurchaseFilter(filters.FilterSet):
    """
    Custom filter for the Purchase model.
    """

    date__gte = filters.DateFilter(field_name="date", lookup_expr="gte")
    date__lte = filters.DateFilter(field_name="date", lookup_expr="lte")
    supplier = filters.CharFilter(field_name="supplier", lookup_expr="icontains")
    product = filters.NumberFilter(field_name="product")
    amount__lt = filters.NumberFilter(field_name="amount", lookup_expr="lt")
    amount__gt = filters.NumberFilter(field_name="amount", lookup_expr="gt")
    amount__range = filters.NumericRangeFilter(field_name="amount")

    class Meta:
        model = Purchase
        fields = ["date", "supplier", "product", "amount"]


class SaleFilter(filters.FilterSet):
    """
    Custom filter for the Sale model.
    """

    date__gte = filters.DateFilter(field_name="date", lookup_expr="gte")
    date__lte = filters.DateFilter(field_name="date", lookup_expr="lte")
    customer = filters.CharFilter(field_name="customer", lookup_expr="icontains")
    product = filters.NumberFilter(field_name="product")
    amount__lt = filters.NumberFilter(field_name="amount", lookup_expr="lt")
    amount__gt = filters.NumberFilter(field_name="amount", lookup_expr="gt")
    amount__range = filters.NumericRangeFilter(field_name="amount")

    class Meta:
        model = Sale
        fields = ["date", "customer", "product", "amount"]


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint for viewing and editing products.
    """

    queryset = Product.objects.select_related().prefetch_related("purchases", "sales")
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = ProductFilter

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in ProductViewSet.create: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in ProductViewSet.create: {e}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in ProductViewSet.update: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in ProductViewSet.update: {e}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class PurchaseViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing purchases with filtering support.
    """

    queryset = Purchase.objects.select_related("product")
    serializer_class = PurchaseSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = PurchaseFilter

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in PurchaseViewSet.create: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in PurchaseViewSet.create: {e}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SaleViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing sales with filtering support.
    """

    queryset = Sale.objects.select_related("product")
    serializer_class = SaleSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = SaleFilter

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            logger.error(f"Validation error in SaleViewSet.create: {e}")
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Unexpected error in SaleViewSet.create: {e}")
            return Response(
                {"error": "Internal server error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
