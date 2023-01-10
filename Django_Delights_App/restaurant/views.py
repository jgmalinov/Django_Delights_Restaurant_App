from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import MenuItemCreateForm, RecipeRequirementCreateForm, IngredientCreateForm, PurchaseCreateForm
from functools import reduce
import json
from django.core import serializers
from django.db.models import F
from datetime import datetime
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recipe_requirements = []
        requirements = RecipeRequirement.objects.all()
        for requirement in RecipeRequirement.objects.all():
            menu_item = requirement.menu_item_id.name
            ingredient = requirement.ingredient_id.name
            metric = requirement.ingredient_id.metric.lower()
            quantity_needed = requirement.quantity_needed
            requirement_str = f'{ingredient} - {quantity_needed}{metric}\n'

            recipe_requirements.append({menu_item: requirement_str})

        context["recipe_requirements"] = recipe_requirements
        return context

class PurchaseList(LoginRequiredMixin, ListView):
    model = Purchase

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchases = Purchase.objects.all()

        total_cost = sum([purchase.cost for purchase in purchases])
        total_revenue = sum([purchase.revenue for purchase in purchases])
        net_profit = total_revenue - total_cost

        context["total_cost"] = total_cost
        context["total_revenue"] = total_revenue
        context["net_profit"] = net_profit

        return context

@login_required
def MenuItemCreate(request):
    context = {}
    ingredients = Ingredient.objects.all()
    ingredients_json = serializers.serialize('json', ingredients)

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

                ingredient = ''
                ingredient_type = ingredient_dict[f'radio{ingredient_counter}'].lower();
                ingredient_name = ingredient_dict[f'ingredient{ingredient_counter}'].lower()
                ingredient_quantity = ingredient_dict[f'quantity{ingredient_counter}']
                ingredient_metric = ingredient_dict[f'metric{ingredient_counter}'].upper()

                if ingredient_type == 'existingingredient':
                    ingredient = Ingredient.objects.get(name=ingredient_name)

                elif ingredient_type == 'newingredient':
                    ingredient_price = ingredient_dict[f'price{ingredient_counter}']
                    ingredient = Ingredient.objects.update_or_create(name=ingredient_name,
                                                                     defaults={'price': ingredient_price,
                                                                               'quantity_available': 0,
                                                                               'metric': ingredient_metric})[0]

                recipe_requirement = RecipeRequirement.objects.update_or_create(ingredient_id = ingredient,
                                                        menu_item_id = menu_item,
                                                        defaults= {'quantity_needed': ingredient_quantity})
                ingredient_counter+= 1

            messages.add_message(request, messages.SUCCESS, 'Menu item successfully added!')
            context = {"ingredients": ingredients, "form": menu_item_form, "ingredients_json": ingredients_json}


        else:
            form = MenuItemCreateForm()
            context = { "ingredients": ingredients, "form": menu_item_form, "ingredients_json": ingredients_json }

    else:
        form = MenuItemCreateForm()
        context = {"ingredients": ingredients, "form": form, "ingredients_json": ingredients_json }

    return render(request, "restaurant/menuitem_create.html", context)


def MenuItemDelete(request, pk):
    menu_item = MenuItem.objects.get(pk=pk)
    requirements = RecipeRequirement.objects.filter(menu_item_id = menu_item)

    for requirement in requirements:
        requirement.delete()

    menu_item.delete()

    messages.add_message(request, messages.SUCCESS, f'Menu item "{menu_item.name}" successfully removed from the menu!')
    return redirect("menu")


@login_required
def PurchaseCreate(request):
    menu_items = MenuItem.objects.all()
    context = {'menu_items': menu_items}

    if request.method == "POST":
        menu_item = MenuItem.objects.get(name=request.POST['menu_item'])
        item_quantity = int(request.POST['item_quantity'])
        recipe_requirements = RecipeRequirement.objects.filter(menu_item_id=menu_item)
        not_enough = []

        for requirement in recipe_requirements:
            ingredient = requirement.ingredient_id
            quantity_needed = requirement.quantity_needed * float(item_quantity)
            if quantity_needed > ingredient.quantity_available:
                message_str = f'{ingredient.name} ({ingredient.quantity_available:.2f}/{quantity_needed:.2f}{ingredient.metric.lower()})'
                not_enough.append(message_str)

        if len(not_enough) > 0:
            messages.add_message(request, messages.ERROR, f'Not enough {", ".join(not_enough)}')

        else:
            cost_per_item = menu_item.get_cost()
            cost = menu_item.get_cost() * item_quantity
            revenue = menu_item.price * item_quantity
            now = datetime.now()
            now_str = now.strftime("%Y-%m-%d %H:%M")
            for requirement in recipe_requirements:
                ingredient = requirement.ingredient_id
                ingredient.quantity_available = ingredient.quantity_available - requirement.quantity_needed * item_quantity
                ingredient.save()

            new_purchase = Purchase(menu_item_id=menu_item,
                                    time_of_purchase=now_str,
                                    revenue=revenue,
                                    cost=cost,
                                    quantity_purchased = item_quantity)
            new_purchase.save()

            messages.add_message(request, messages.SUCCESS, f'{item_quantity} {menu_item.name}/s purchased for {round(cost, 2)}lv.')

    return render(request, 'restaurant/purchase_create.html', context)




class IngredientCreateView(LoginRequiredMixin, CreateView):
    model = Ingredient
    form_class = IngredientCreateForm
    template_name = "restaurant/ingredient_create.html"
    success_url = "/accounts/inventory"

class IngredientUpdateView(LoginRequiredMixin, UpdateView):
    model = Ingredient
    fields = "__all__"
    template_name = "restaurant/ingredient_update.html"
    success_url = "/accounts/inventory"

class IngredientDeleteView(LoginRequiredMixin, DeleteView):
    model = Ingredient
    success_url = "/accounts/inventory"