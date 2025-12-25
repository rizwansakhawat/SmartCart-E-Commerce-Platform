from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import Cart, CartItem
from store.models import Product
from django.views.generic import DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.

# class AddToCartView(LoginRequiredMixin, View):
#     login_url = "/login/"


class AddToCartView(LoginRequiredMixin, View):
    login_url = "/login/"
    
    
    def post(self, request, product_id):
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id= product_id)

        item, created = CartItem.objects.get_or_create(cart= cart, product=product)
        if not created:
            item.quantity +=1
            item.save()
            
        return redirect("cart")
    
# cart view
class CartDetailView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart.html"
    login_url= "/login/"
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        cart = Cart.objects.filter(user= self.request.user).first()
        context['cart']= cart
        
        if cart:
            items = cart.cartitem_set.all()
            total = sum(item.total_price for item in items)
            context['items'] = items
            context['total'] = total

        else:
            context['items'] = []
            context['total'] = 0
        return context
    
    
# remove item in cart
class RemoveFromCartView(View):
    
    def post(self, request, item_id):
        item = get_object_or_404(CartItem, id=item_id , cart__user=request.user)
        item.delete()
        return redirect("cart")
    
    
# # increase and decrease 
class UpdatecartItemQuantityView(View):
    def post(self, request, item_id , action):
        item = get_object_or_404(CartItem, id= item_id, cart__user= request.user)
        
        if action == "increase" :
            item.quantity += 1
            item.save()
        elif action == "decrease" :
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            else:
                item.delete()

        return redirect("cart")
