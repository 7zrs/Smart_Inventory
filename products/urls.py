from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, SaleViewSet, PurchaseViewSet

# Create a router and register ViewSets
router = DefaultRouter()
router.register(r'products', ProductViewSet)  # Products endpoint
router.register(r'purchases', PurchaseViewSet)  # Purchases endpoint
router.register(r'sales', SaleViewSet)  # Sales endpoint

# Define the urlpatterns
urlpatterns = [
    path('', include(router.urls)),  # Include all routes from the router
]