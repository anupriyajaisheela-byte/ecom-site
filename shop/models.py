from django.db import models
from django.core.files import File  # optional for admin preview


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    # session_key ties the cart item to a specific anonymous session/user
    session_key = models.CharField(max_length=40, db_index=True, default='', blank=True)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
