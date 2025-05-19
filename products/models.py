from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    unit = models.CharField(max_length=50)  # Unit of measurement (e.g., pieces, kilograms)
    notes = models.TextField(blank=True, null=True)  # Editable notes about the product

    def purchased_amount(self):
        """Calculate total purchased amount for this product."""
        return sum(purchase.amount for purchase in self.purchases.all())

    def sold_amount(self):
        """Calculate total sold amount for this product."""
        return sum(sale.amount for sale in self.sales.all())

    def stock_level(self):
        """Calculate current stock level (purchased - sold)."""
        return self.purchased_amount() - self.sold_amount()

    def __str__(self):
        return f"{self.name} ({self.unit})"
    
class Purchase(models.Model):
    date = models.DateField()
    supplier = models.CharField(max_length=255, blank=True, null=True)  # Optional supplier name
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='purchases')
    amount = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)  # Purchase-specific notes

    def __str__(self):
        return f"{self.amount} {self.product.unit} of {self.product.name} purchased on {self.date}"

class Sale(models.Model):
    date = models.DateField()
    customer = models.CharField(max_length=255, blank=True, null=True)  # Optional customer name
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    amount = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)  # Sale-specific notes

    def __str__(self):
        return f"{self.amount} {self.product.unit} of {self.product.name} sold on {self.date}"