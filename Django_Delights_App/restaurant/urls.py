from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home_view, name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup', views.signup_view, name="signup"),
    path('logout/', views.logout_view, name="logout"),
    path('about/', views.about_view, name="about")
]