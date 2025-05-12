from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly,AllowAny
from .models import Stock, Shipment
from .serializers import StockSerializer, ShipmentSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [AllowAny]  # for now

class ShipmentViewSet(viewsets.ModelViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
    permission_classes = [AllowAny]  # for now