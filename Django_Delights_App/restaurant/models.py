from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=50, null=False)
    price = models.FloatField()
    quantity_available = models.FloatField()


    class Metrics(models.TextChoices):
        GRAMS = "G", _('g')
        MILILITERS = "ML", _('ml')
        UNITS = "UNITS", _('units')

    metric = models.CharField(max_length=6, choices=Metrics.choices, default=Metrics.GRAMS)

    class Meta:
        ordering = ["name"]

class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()

    class Meta:
        ordering = ["name"]

class RecipeRequirement(models.Model):
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    menu_item_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity_needed = models.FloatField()

    def is_sufficient(self, quantity_available):
        return self.quantity_needed >= quantity_available


class Purchase(models.Model):
    menu_item_id = models.ForeignKey(MenuItem, on_delete=models.PROTECT)
    time_of_purchase = models.DateTimeField()
    bill = models.FloatField()

    class Meta:
        ordering = ["time_of_purchase"]
