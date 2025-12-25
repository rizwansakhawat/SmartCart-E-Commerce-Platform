from django.urls import path
from .views import CheckoutView, order_success, MyOrderView, OrderDetailView

urlpatterns = [
    path('checkout/', CheckoutView.as_view(), name="checkout"),
    path("success/", order_success, name="order_success"),
    path('my-orders/', MyOrderView.as_view(), name="my_orders"),
    path("order/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    
]