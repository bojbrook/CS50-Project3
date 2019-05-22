from django.db import models

# Create your models here.
class Toppings(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class dinnerSizes(models.Model):
    size = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.size}"

class dinnerTypes(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Food(models.Model):
    name = models.CharField(max_length=64)
    size = models.ForeignKey(dinnerSizes, on_delete=models.CASCADE)
    price = models.FloatField()
    foodType = models.ForeignKey(dinnerTypes, on_delete=models.CASCADE, related_name="type")

    def __str__(self):
        if self.size == dinnerSizes.objects.get(size="NULL"):
            return f"{self.name} Type: {self.foodType} - ${self.price}"
        else:
            return f"{self.name} Type: {self.foodType} Size: {self.size} - ${self.price}"