from django.db import models
from core.models import TimeStampedModel

# Create your models here.
class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Product(TimeStampedModel):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ManyToManyField(Category)
    description = models.TextField()

    def __str__(self):
        return f"{self.name} - RS {self.price}"

        
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE , related_name="images")
    image = models.ImageField(upload_to="products/")


    
    