from django.urls import path
from .views import CheckoutView, order_success, MyOrderView, OrderDetailView, StripePaymentView, stripe_success

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path("success/", order_success, name="order_success"),
    path('my-orders/', MyOrderView.as_view(), name="my_orders"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("pay/stripe/<int:order_id>/", StripePaymentView.as_view(), name="stripe_payment"),
    path("stripe/success/<int:order_id>/", stripe_success, name="stripe_success"),

    
]