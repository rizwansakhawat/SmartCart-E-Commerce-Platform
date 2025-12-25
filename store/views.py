from django.shortcuts import render
from django.views.generic import ListView, DetailView, DetailView, UpdateView
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = "store/home.html"
    context_object_name = "products"
    
    

class ProductDetailView(LoginRequiredMixin ,DetailView):
    login_url = 'login'
    model = Product
    template_name = "store/product_detail.html"
    context_object_name= "product"

