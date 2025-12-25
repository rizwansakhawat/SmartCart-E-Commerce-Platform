from django.urls import path
from .views import CheckoutView, order_success

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path("success/", order_success, name="order_success"),
]