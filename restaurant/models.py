from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.

class NameField(models.CharField):
    def get_prep_value(self, value):
        return str(value).lower()


class Ingredient(models.Model):
    name = NameField(max_length=50, null=False)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity_available = models.DecimalField(decimal_places=2, max_digits=10)


    class Metrics(models.TextChoices):
        KILOGRAMS = "KG", _('kg')
        LITERS = "L", _('l')
        UNITS = "UNITS", _('units')

    metric = models.CharField(max_length=6, choices=Metrics.choices, default=Metrics.KILOGRAMS)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name"], name='ingredient_name_unique')
        ]
        ordering = ["name"]

class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=['name'], name='unique_menu_items')
        ]

    def get_cost(self):
        requirements = RecipeRequirement.objects.filter(menu_item_id=self)
        ingredients = [requirement.ingredient_id.price * requirement.quantity_needed for requirement in requirements]
        cost = sum(ingredients)
        return cost

class RecipeRequirement(models.Model):
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    menu_item_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity_needed = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('ingredient_id', 'menu_item_id'), name='menu_item_ingredient_unique')
        ]

    def is_sufficient(self, quantity_available):
        return self.quantity_needed >= quantity_available


class Purchase(models.Model):
    menu_item_name = NameField(max_length=50)
    time_of_purchase = models.DateTimeField()
    revenue = models.DecimalField(decimal_places=2, max_digits=10)
    cost = models.DecimalField(decimal_places=2, max_digits=10)
    quantity_purchased = models.IntegerField(default=1)

    class Meta:
        ordering = ["time_of_purchase"]
