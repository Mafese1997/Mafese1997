from django.urls import path
from . import views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    # Other URL patterns...
]

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
]
