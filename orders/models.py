from django.db import models

# Create your models here.
class Toppings(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Salads(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f"{self.name} - ${self.price}"


class Pasta(models.Model):
    name = models.CharField(max_length=64)
    price = models.FloatField()

    def __str__(self):
        return f"{self.name} - ${self.price}"

    