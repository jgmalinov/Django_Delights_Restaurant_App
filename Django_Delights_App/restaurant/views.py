from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import MenuItemCreateForm, RecipeRequirementCreateForm
from functools import reduce
import json
from django.core import serializers
# Create your views here.

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, "Registration Successful! Please log into your account!")
            return redirect("login")
        else:
            return render(request, "registration/signup.html", {"form": form})
    else:
        form = UserCreationForm()
        return render(request, "registration/signup.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")


@login_required
def home_view(request):
    context = {"username": request.user.username}
    return render(request, "restaurant/home.html", context)

@login_required
def about_view(request):
    return render("restaurant/about.html")

class InventoryList(LoginRequiredMixin, ListView):
    model = Ingredient


class MenuItemList(LoginRequiredMixin, ListView):
    model = MenuItem

class PurchaseList(LoginRequiredMixin, ListView):
    model = Purchase

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        menu_items_purchased = [purchase.menu_item_id for purchase in Purchase.objects.all()]
        cost_and_revenue_per_item = {}

        for menu_item in menu_items_purchased:
            if not menu_item.name in cost_and_revenue_per_item.keys():
                recipe_requirements = RecipeRequirement.objects.get(menu_item_id=menu_item)
                total_menu_item_cost = 0
                cost_per_req = map(lambda recipe_req: recipe_req.quantity_needed * recipe_req.ingredient_id.price, recipe_requirements)
                cost_per_item = reduce(lambda a, b: a+b, cost_per_req)

                cost_and_revenue_per_item[menu_item.name] = {revenue: menu_item.price, cost: cost_per_item}

            else:
                cost_and_revenue_per_item[menu_item.name].revenue += cost_and_revenue_per_item[menu_item.name].revenue
                cost_and_revenue_per_item[menu_item.name].cost += cost_and_revenue_per_item[menu_item.name].cost

        total_purchases_cost = sum(map(lambda menu_item_values: menu_item_values.cost, cost_and_revenue_per_item.values()))
        total_purchases_revenue = sum(map(lambda menu_item_values: menu_item_values.revenue, cost_and_revenue_per_item.values()))
        context["total_purchases_cost"] = total_purchases_cost
        context["total_purchases_revenue"] = total_purchases_revenue
        context["net_profit"] = total_purchases_revenue - total_purchases_cost

        return context
@login_required
def MenuItemCreate(request):
    if request.method == "POST":
        menu_item_data = {'name': request.POST["name"].lower(), 'price': request.POST["price"]}
        menu_item_form = MenuItemCreateForm(menu_item_data)
        if menu_item_form.is_valid():
            menu_item_form.save()
            menu_item = MenuItem.objects.get(name=request.POST["name"].lower())

            ingredient_counter = 1
            while True:
                ingredient_dict = dict(filter(lambda field: field[0][-1] == str(ingredient_counter), request.POST.items()))
                if len(ingredient_dict) == 0:
                    break

                ingredient_name = ingredient_dict[f'ingredient{ingredient_counter}'].lower()
                ingredient_quantity = ingredient_dict[f'quantity{ingredient_counter}']
                ingredient_metric = ingredient_dict[f'metric{ingredient_counter}'].upper()

                ingredient = Ingredient.objects.get_or_create(name=ingredient_name,
                                                              price=0, quantity_available=0,
                                                              metric=ingredient_metric)

                RecipeRequirement.objects.get_or_create(ingredient_id = ingredient[0],
                                                        menu_item_id = menu_item,
                                                        quantity_needed = ingredient_quantity)



    else:
        form = MenuItemCreateForm()
        ingredients = Ingredient.objects.all();
        ingredients_json = serializers.serialize('json', ingredients)
        context = {"ingredients": ingredients, "form": form, "ingredients_json": ingredients_json }
        return render(request, "restaurant/menuitem_create.html", context)
