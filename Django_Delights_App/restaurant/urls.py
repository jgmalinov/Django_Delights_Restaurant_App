from django.urls import path, include
from . import views


urlpatterns = [
    path('accounts/profile/', views.home_view, name="home"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup_view, name="signup"),
    path('logout/', views.logout_view, name="logout"),
    path('accounts/inventory/', views.InventoryList.as_view(), name = "inventory"),
    path('accounts/menu/', views.MenuItemList.as_view(), name = "menu"),
    path('accounts/purchase/', views.PurchaseList.as_view(), name = "purchase"),
    path('about/', views.about_view, name="about")
]