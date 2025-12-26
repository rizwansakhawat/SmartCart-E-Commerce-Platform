from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra= 0
    readonly_fields = ("product", "quantity", "price")
    
@admin.register(Order)
class OredrAdmin(admin.ModelAdmin):
    list_display = ("id","user", "total_price", "status", "is_paid", "created_at")
    list_filter = ("status", "is_paid", "created_at")
    search_fields = ("id", "user__username")
    readonly_fields =("user", "total_price", "created_at")
    
    inlines = [OrderItemInline]