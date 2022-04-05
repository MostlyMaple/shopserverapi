from django.db import models
from django.contrib.auth.models import User


class ClothingType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class ClothingSize(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class SearchType(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Item(models.Model):
    topic = models.ForeignKey(ClothingType, on_delete=models.SET_NULL, null=True)
    item_name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    #image = 
    quantity = models.IntegerField(default=0, null=True, blank=True)
    price = models.FloatField(default=0, null=True, blank=True)
    size = models.ForeignKey(ClothingSize, on_delete=models.SET_NULL, null=True)
    digital = models.BooleanField(default=False, null=True, blank=False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.item_name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    taxPrice = models.DecimalField(max_digits = 7, decimal_places = 2, null = True, blank=True)
    totalPrice = models.DecimalField(max_digits = 7, decimal_places = 2, null = True, blank=True)
    created = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.created)

class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits = 7, decimal_places = 2, null = True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.name)

class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.address)