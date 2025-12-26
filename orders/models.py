from django.db import models
from django.contrib.auth.models import User
from store.models import Product




# Create your models here.
class Order(models.Model):
    
    STATUS_CHOICES= (
        ("pending", "pending"),
        ("processing", "processing"),
        ("shipped", "shipped"),
        ("delivered","delivered"),
        ("cancelled", "cancelled"),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES , default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"order #{self.id} - {self.user.username}"
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"



    