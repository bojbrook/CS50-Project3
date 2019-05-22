from django.db import models

# Create your models here.
class Toppings(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class dinnerTypes(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Food(models.Model):
    name = models.CharField(max_length=64)
    priceOfSmall = models.FloatField()
    priceOfLarge = models.FloatField()
    foodType = models.ForeignKey(dinnerTypes, on_delete=models.CASCADE, related_name="type")

    def __str__(self):
        if self.foodType == dinnerTypes.objects.get(name="Salads") or self.foodType == dinnerTypes.objects.get(name="Pasta"):
            return f"{self.name} Type: {self.foodType} - ${self.priceOfSmall:.2f}"
        else:
            return f"{self.name} Small: ${self.priceOfSmall:.2f}  Large: ${self.priceOfLarge:.2f}"