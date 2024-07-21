from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from store.views import OrderItem
from django.db import models
from django.apps import apps

Product = apps.get_model('store', 'Product')


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey( Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user, active=True)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

def cart_detail(request):
    cart = Cart.objects.get(user=request.user, active=True)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'store/cart_detail.html', {'cart_items': cart_items})

# Create your models here.
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/')

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
from django.shortcuts import render, get_object_or_404, redirect
from .forms import ReviewForm # type: ignore

def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('product_detail', id=product.id)
    else:
        form = ReviewForm()
    return render(request, 'store/add_review.html', {'form': form})



   
    
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    wishlist.products.add(product)
    return redirect('wishlist')

def wishlist(request):
    wishlist = Wishlist.objects.get(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist': wishlist})

class Product(models.Model):
    # Other fields
    stock = models.PositiveIntegerField()

    def reduce_stock(self, quantity):
        self.stock -= quantity
        self.save()

class Promotion(models.Model):
    code = models.CharField(max_length=50)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    active = models.BooleanField(default=True)

from django.core.mail import send_mail

def send_order_confirmation(order):
    subject = 'Order Confirmation'
    message = f'Your order {order.id} has been placed successfully.'
    recipient_list = [order.user.email]
    send_mail(subject, message, 'from@example.com', recipient_list)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')

from django.contrib import admin
from django.db.models import Sum

class ProductAdmin(admin.ModelAdmin):
    def total_stock(self):
        return Product.objects.aggregate(Sum('stock'))['stock__sum']

    def total_sales(self):
        return OrderItem.objects.aggregate(Sum('quantity'))['quantity__sum']

class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)





    