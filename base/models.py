from django.db import models

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