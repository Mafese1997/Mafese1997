from itertools import product
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib.auth.models import User
from networkx import project # type: ignore
# store/views.py
import networkx as nx
from networkx.algorithms.bipartite import projected_graph

def some_view(request):
    B = nx.Graph()
    # Add nodes and edges to the graph
    projection = projected_graph(B, [1, 2, 3])
    # Further processing...


from store.models import Cart, CartItem, Category, Promotion

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.TextField()
    paid = models.BooleanField(default=False)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(project, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

def checkout(request):
    cart = Cart.objects.get(user=request.user, active=True)
    if request.method == 'POST':
        order = Order.objects.create(user=request.user, address=request.POST['address'], paid=True)
        for cart_item in CartItem.objects.filter(cart=cart):
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
        cart.delete()
        return redirect('order_complete')
    return render(request, 'store/checkout.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to a success page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to a success page

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def home(request):
    return redirect('product_list')

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'store/product_list.html', {'category': category, 'categories': categories, 'products': products})

from django.db.models import Q

def search(request):
    query = request.GET.get('query')
    products = product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    return render(request, 'store/search_results.html', {'products': products})
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'store/order_history.html', {'orders': orders})

def apply_promotion(request):
    code = request.POST.get('code')
    try:
        promotion = Promotion.objects.get(code=code, active=True)
        # Apply discount logic
    except Promotion.DoesNotExist: (" promotion does not exist ")

import csv
from django.http import HttpResponse
from .models import Product

def upload_products(request):
    if request.method == 'POST':
        csv_file = request.FILES['file']
        reader = csv.reader(csv_file)
        for row in reader:
            Product.objects.create(name=row[0], price=row[1], stock=row[2])
    return render(request, 'admin/upload_products.html')
