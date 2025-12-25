from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import Cart, CartItem


# Create your views here.

class CheckoutView(View):
    
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        items = CartItem.objects.filter(cart=cart)
        
        if not items.exists():
            return redirect("cart")
        
        total = sum(item.total_price for item in items)
        return render(request, "orders/checkout.html", {"items":items , "total":total})
    
    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        items = CartItem.objects.filter(cart=cart)
        total = sum(item.total_price for item in items)

        order = Order.objects.create(
            user = request.user,
            total_price = total
        )
        
        for item in items:
            OrderItem.objects.create(
                order= order,
                product= item.product,
                quantity = item.quantity,
                price = item.product.price
            )
        items.delete()
        
        return redirect("order_success")

        
def order_success(request):
    return render(request, 'orders/success.html')