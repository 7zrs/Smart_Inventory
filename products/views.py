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

    # Django-style lookup filters for stock_level
    stock_level__lt = filters.NumberFilter(method="filter_stock_level_lookup")
    stock_level__gt = filters.NumberFilter(method="filter_stock_level_lookup")
    stock_level__lte = filters.NumberFilter(method="filter_stock_level_lookup")
    stock_level__gte = filters.NumberFilter(method="filter_stock_level_lookup")
    stock_level__exact = filters.NumberFilter(method="filter_stock_level_lookup")

    # Keep backward compatibility filters
    min_stock_level = filters.NumberFilter(method="filter_min_stock_level")
    max_stock_level = filters.NumberFilter(method="filter_max_stock_level")

    class Meta:
        model = Product
        fields = [
            "name",
            "unit",
            "notes",
            "stock_level__lt",
            "stock_level__gt",
            "stock_level__lte",
            "stock_level__gte",
            "stock_level__exact",
            "min_stock_level",
            "max_stock_level",
        ]

    def filter_stock_level_lookup(self, queryset, name, value):
        """
        Filter products by stock_level using specific lookup expressions.
        """
        if value is not None:
            # Extract lookup expression from name (e.g., "stock_level__lt" -> "lt")
            lookup_expr = name.split("__")[-1]

            # Annotate with calculated fields
            queryset = queryset.annotate(
                purchased_amount=Coalesce(
                    Sum("purchases__amount", distinct=True), Value(0)
                ),
                sold_amount=Coalesce(Sum("sales__amount", distinct=True), Value(0)),
            ).annotate(stock_level=F("purchased_amount") - F("sold_amount"))

            # Apply filter with the extracted lookup
            filter_kwargs = {f"stock_level__{lookup_expr}": value}
            queryset = queryset.filter(**filter_kwargs)

        return queryset

    def filter_min_stock_level(self, queryset, name, value):
        """
        Filter products with stock level greater than or equal to the given value.
        """
        if value is not None:
            # Annotate with calculated fields and filter
            queryset = queryset.annotate(
                purchased_amount=Coalesce(
                    Sum("purchases__amount", distinct=True), Value(0)
                ),
                sold_amount=Coalesce(Sum("sales__amount", distinct=True), Value(0)),
            ).annotate(stock_level=F("purchased_amount") - F("sold_amount"))

            queryset = queryset.filter(stock_level__gte=value)
        return queryset

    def filter_max_stock_level(self, queryset, name, value):
        """
        Filter products with stock level less than or equal to the given value.
        """
        if value is not None:
            # Annotate with calculated fields and filter
            queryset = queryset.annotate(
                purchased_amount=Coalesce(
                    Sum("purchases__amount", distinct=True), Value(0)
                ),
                sold_amount=Coalesce(Sum("sales__amount", distinct=True), Value(0)),
            ).annotate(stock_level=F("purchased_amount") - F("sold_amount"))

            queryset = queryset.filter(stock_level__lte=value)
        return queryset

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

        return annotated_qs


class PurchaseFilter(filters.FilterSet):
    """
    Custom filter for the Purchase model.
    """

    date__gte = filters.DateFilter(field_name="date", lookup_expr="gte")
    date__lte = filters.DateFilter(field_name="date", lookup_expr="lte")
    date__gt = filters.DateFilter(field_name="date", lookup_expr="gt")
    date__lt = filters.DateFilter(field_name="date", lookup_expr="lt")
    date__exact = filters.DateFilter(field_name="date", lookup_expr="exact")
    supplier = filters.CharFilter(field_name="supplier", lookup_expr="icontains")
    supplier__icontains = filters.CharFilter(
        field_name="supplier", lookup_expr="icontains"
    )
    supplier__exact = filters.CharFilter(field_name="supplier", lookup_expr="exact")
    product = filters.NumberFilter(field_name="product")
    product__exact = filters.NumberFilter(field_name="product", lookup_expr="exact")
    amount__lt = filters.NumberFilter(field_name="amount", lookup_expr="lt")
    amount__gt = filters.NumberFilter(field_name="amount", lookup_expr="gt")
    amount__lte = filters.NumberFilter(field_name="amount", lookup_expr="lte")
    amount__gte = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    amount__exact = filters.NumberFilter(field_name="amount", lookup_expr="exact")
    amount__range = filters.NumericRangeFilter(field_name="amount")
    notes = filters.CharFilter(field_name="notes", lookup_expr="icontains")
    notes__icontains = filters.CharFilter(field_name="notes", lookup_expr="icontains")
    notes__exact = filters.CharFilter(field_name="notes", lookup_expr="exact")
    notes__contains = filters.CharFilter(field_name="notes", lookup_expr="contains")

    class Meta:
        model = Purchase
        fields = [
            "date",
            "date__gte",
            "date__lte",
            "date__gt",
            "date__lt",
            "date__exact",
            "supplier",
            "supplier__icontains",
            "supplier__exact",
            "product",
            "product__exact",
            "amount",
            "amount__lt",
            "amount__gt",
            "amount__lte",
            "amount__gte",
            "amount__exact",
            "amount__range",
            "notes",
            "notes__icontains",
            "notes__exact",
            "notes__contains",
        ]


class SaleFilter(filters.FilterSet):
    """
    Custom filter for Sale model.
    """

    date__gte = filters.DateFilter(field_name="date", lookup_expr="gte")
    date__lte = filters.DateFilter(field_name="date", lookup_expr="lte")
    date__gt = filters.DateFilter(field_name="date", lookup_expr="gt")
    date__lt = filters.DateFilter(field_name="date", lookup_expr="lt")
    date__exact = filters.DateFilter(field_name="date", lookup_expr="exact")
    customer = filters.CharFilter(field_name="customer", lookup_expr="icontains")
    customer__icontains = filters.CharFilter(
        field_name="customer", lookup_expr="icontains"
    )
    customer__exact = filters.CharFilter(field_name="customer", lookup_expr="exact")
    product = filters.NumberFilter(field_name="product")
    product__exact = filters.NumberFilter(field_name="product", lookup_expr="exact")
    amount__lt = filters.NumberFilter(field_name="amount", lookup_expr="lt")
    amount__gt = filters.NumberFilter(field_name="amount", lookup_expr="gt")
    amount__lte = filters.NumberFilter(field_name="amount", lookup_expr="lte")
    amount__gte = filters.NumberFilter(field_name="amount", lookup_expr="gte")
    amount__exact = filters.NumberFilter(field_name="amount", lookup_expr="exact")
    amount__range = filters.NumericRangeFilter(field_name="amount")
    notes = filters.CharFilter(field_name="notes", lookup_expr="icontains")
    notes__icontains = filters.CharFilter(field_name="notes", lookup_expr="icontains")
    notes__exact = filters.CharFilter(field_name="notes", lookup_expr="exact")
    notes__contains = filters.CharFilter(field_name="notes", lookup_expr="contains")

    class Meta:
        model = Sale
        fields = [
            "date",
            "date__gte",
            "date__lte",
            "date__gt",
            "date__lt",
            "date__exact",
            "customer",
            "customer__icontains",
            "customer__exact",
            "product",
            "product__exact",
            "amount",
            "amount__lt",
            "amount__gt",
            "amount__lte",
            "amount__gte",
            "amount__exact",
            "amount__range",
            "notes",
            "notes__icontains",
            "notes__exact",
            "notes__contains",
        ]


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
