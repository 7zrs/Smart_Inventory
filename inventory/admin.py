from django.contrib import admin
from .models import Stock, Shipment

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'last_updated')
    search_fields = ('product__name',)
    list_filter = ('last_updated',)

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'received_on', 'notes')
    search_fields = ('product__name',)
    list_filter = ('received_on',)