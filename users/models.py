from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel

# Create your models here.

class CustomUser(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number= models.CharField(max_length=15)
    address = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"
    
