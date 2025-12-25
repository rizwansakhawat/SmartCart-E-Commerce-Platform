from django.shortcuts import render
from django.views.generic import ListView, DetailView, DetailView, UpdateView
from .models import Product

# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = "store/home.html"
    context_object_name = "products"
    
    

class ProductDetailView(DetailView):
    model = Product
    template_name = "store/product_detail.html"
    context_object_name= "product"

