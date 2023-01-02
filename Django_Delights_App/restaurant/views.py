from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.views.generic import ListView
from .models import Ingredient, MenuItem, Purchase
# Create your views here.

def signup_view(request):
    print(request.POST)
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
        context["MenuItem"] = 'laina'
        return context