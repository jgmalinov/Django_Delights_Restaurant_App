from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
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
@login_required
def home_view(request):
    context = {"username": request.user.username}
    return render(request, "restaurant/home.html", context)

def logout_view(request):
    logout(request)
    return redirect("home")

def about_view(request):
    return render("restaurant/about.html")