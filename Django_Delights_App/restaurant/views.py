from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required
def home_view(request):
    context = {"username": request.user.username}
    return render(request, "restaurant/home.html", context)

def logout_view(request):
    logout(request)
    return redirect("home")

def about_view(request):
    return render("restaurant/about.html")