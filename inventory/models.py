from django.db import models
from products.models import Product
from django.db.models.signals import post_save
from django.dispatch import receiver

class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock')
    quantity = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"

class Shipment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='shipments')
    quantity = models.PositiveIntegerField()
    received_on = models.DateField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.quantity} units of {self.product.name} received on {self.received_on}"
    

@receiver(post_save, sender=Shipment)
def update_stock_on_shipment(sender, instance, created, **kwargs):
    if created:
        stock, _ = Stock.objects.get_or_create(product=instance.product)
        stock.quantity += instance.quantity
        stock.save()