from django import forms
from django.contrib.auth.models import User
from . import models
from .models import MenuItem, RecipeRequirement, Ingredient, Purchase

class MenuItemCreateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price']

class RecipeRequirementCreateForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = ['menu_item_id', 'ingredient_id', 'quantity_needed']

class IngredientCreateForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ["name", "price", "quantity_available", "metric"]

class PurchaseCreateForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = "__all__"