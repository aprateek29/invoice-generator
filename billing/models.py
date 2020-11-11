from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    quantity = models.IntegerField()

    @property
    def get_total(self):
        return self.price * self.quantity
