from django.shortcuts import render, get_object_or_404, redirect
from .models import Order, OrderItem
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from cart.models import Cart, CartItem
from django.views.generic import DetailView, ListView
from .ulits import send_order_email
from django.core.mail import send_mail
from ai_engine.tracking import track_user_behavior


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
        
        payment_method = request.POST.get("payment_method")
        total = sum(item.total_price for item in items)

        order = Order.objects.create(
            user = request.user,
            total_price = total,
            payment_method = payment_method,
            is_paid = False,
        )
        
        for item in items:
            OrderItem.objects.create(
                order= order,
                product= item.product,
                quantity = item.quantity,
                price = item.product.price
            )
            # Track purchase behavior for AI recommendations
            track_user_behavior(
                user=request.user,
                action='purchase',
                product=item.product,
                session_id=request.session.session_key
            )
            
        
        if payment_method == "cod":
            if order.user.email:
                send_order_email(order)
                
            items.delete()
            return redirect("order_success" )
        
        return redirect("stripe_payment", order.id)

#   when orsdr confirm     
def order_success(request):
    return render(request, 'orders/success.html')

# order view
class MyOrderView(LoginRequiredMixin, ListView):
    model= Order
    template_name= "orders/my_order.html"
    context_object_name= "orders"

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-created_at")
    
# order detail view
class OrderDetailView(LoginRequiredMixin , DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name= "order"
    
    def get_queryset(self):
        return Order.objects.filter(user= self.request.user)


# OPTIONAL: Prevent Item Editing (Best Practice)
# Already done via:
# readonly_fields = ("product", "quantity", "price")
# Admin cannot accidentally change order history



import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

class StripePaymentView(LoginRequiredMixin, View):

    def get(self, request, order_id):
        order = Order.objects.get(id=order_id, user=request.user)

        # ✅ Stripe minimum check (50 cents ≈ Rs 150–200)
        if order.total_price < 200:
            return render(request, "orders/payment_error.html", {
                "message": "Minimum amount for online payment is Rs 200. Please use Cash on Delivery."
            })

        intent = stripe.PaymentIntent.create(
            amount=int(order.total_price * 100),
            currency="pkr",
            metadata={"order_id": order.id}
        )

        return render(request, "orders/stripe_payment.html", {
            "client_secret": intent.client_secret,
            "stripe_key": settings.STRIPE_PUBLIC_KEY,
            "order_id": order.id,
        })
        
        
def stripe_success(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    order.is_paid = True
    order.save()

    CartItem.objects.filter(cart__user=request.user).delete()
    if order.user.email:
        send_mail(
            subject=f"Payment Successful - Order #{order.id}",
            message=f"""
Hi {order.user.username},

Your payment for order #{order.id} was successful.

Amount Paid: Rs {order.total_price}

Thank you for shopping with SmartCart!
""",
        from_email=None,
        recipient_list=[order.user.email],
    )

    return render(request, "orders/success.html")







