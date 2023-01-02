from django import forms
from django.contrib.auth.models import User
from .models import MenuItem, RecipeRequirement

class MenuItemCreateForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'price']

class RecipeRequirementCreateForm(forms.ModelForm):
    class Meta:
        model = RecipeRequirement
        fields = ['menu_item_id', 'ingredient_id', 'quantity_needed']



