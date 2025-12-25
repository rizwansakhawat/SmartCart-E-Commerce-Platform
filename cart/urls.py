from django.urls import path
from .views import AddToCartView, CartDetailView, RemoveFromCartView, UpdatecartItemQuantityView

urlpatterns =[
    path('add/<int:product_id>/', AddToCartView.as_view(), name="add_to_cart"),
    path('', CartDetailView.as_view(), name="cart"),
    path('remove/<int:item_id>/', RemoveFromCartView.as_view(), name="remove_from_cart"),
    path('update/<int:item_id>/<str:action>/', UpdatecartItemQuantityView.as_view(), name="update_cart_item"),
    
]