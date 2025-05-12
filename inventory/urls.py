from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockViewSet, ShipmentViewSet

router = DefaultRouter()
router.register(r'stock', StockViewSet)
router.register(r'shipments', ShipmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]