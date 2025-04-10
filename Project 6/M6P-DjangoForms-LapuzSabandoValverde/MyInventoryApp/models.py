from django.db import models # type: ignore
# Create your models here.

class Supplier(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    created_at = models.DateTimeField()

    def getName(self):
        return self.name

    def __str__(self):
        return f"{self.name} - {self.city}, {self.country}"


class WaterBottle(models.Model):
    sku = models.CharField(max_length=10, unique=True)
    brand = models.CharField(max_length=255)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.CharField(max_length=50)
    mouth_size = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    current_quantity = models.IntegerField()

    def __str__(self):
        return f"SKU: {self.sku}: {self.brand}, {self.mouth_size}, {self.size}, {self.color}, supplied by {self.supplier}, Cost: {self.cost}, Quantity: {self.current_quantity}"


class Account(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=150)

    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password