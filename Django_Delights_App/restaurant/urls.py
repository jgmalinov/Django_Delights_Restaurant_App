from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home_view),
    path('login/', include('django.contrib.auth.urls')),
    path('logout/', views.logout_view, name="logout"),
    path('about/', views.about_view, name="about")
]