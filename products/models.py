from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True)  # Ensure unique product names
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
    date = models.DateField(db_index=True)  # Add index for filtering by date
    supplier = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='purchases')
    amount = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('product', 'date', 'supplier')  # Prevent duplicate purchases

    def clean(self):
        """
        Custom validation for the Purchase model.
        """
        # Ensure the purchase amount is greater than zero
        if self.amount <= 0:
            raise ValidationError("Purchase amount must be greater than zero.")

    def save(self, *args, **kwargs):
        """
        Override the save method to enforce validation before saving.
        """
        self.full_clean()  # Run all validations
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Purchase of {self.product.name} on {self.date}"


class Sale(models.Model):
    date = models.DateField(db_index=True)  # Add index for filtering by date
    customer = models.CharField(max_length=255, blank=True, null=True)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='sales')
    amount = models.PositiveIntegerField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('product', 'date', 'customer')  # Prevent duplicate sales

    def clean(self):
        """
        Custom validation for the Sale model.
        """
        # Ensure the sale amount is greater than zero
        if self.amount <= 0:
            raise ValidationError("Sale amount must be greater than zero.")

        # Ensure the sale amount does not exceed the product's stock level
        if self.product.stock_level() < self.amount:
            raise ValidationError(
                f"Cannot sell {self.amount} {self.product.unit}. "
                f"Only {self.product.stock_level} {self.product.unit} available."
            )

    def save(self, *args, **kwargs):
        """
        Override the save method to enforce validation before saving.
        """
        self.full_clean()  # Run all validations
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Sale of {self.product.name} on {self.date}"