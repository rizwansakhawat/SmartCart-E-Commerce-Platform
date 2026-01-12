from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from core.models import TimeStampedModel


class UserBehavior(TimeStampedModel):
    """Track user interactions for personalization"""
    ACTION_CHOICES = (
        ('view', 'View'),
        ('add_to_cart', 'Add to Cart'),
        ('purchase', 'Purchase'),
        ('wishlist', 'Wishlist'),
        ('search', 'Search'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='behaviors')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    search_query = models.CharField(max_length=255, null=True, blank=True)
    session_id = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['product', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.created_at}"


class ProductReview(TimeStampedModel):
    """Product reviews with AI-powered sentiment analysis"""
    SENTIMENT_CHOICES = (
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    title = models.CharField(max_length=200)
    comment = models.TextField()
    sentiment = models.CharField(max_length=20, choices=SENTIMENT_CHOICES, null=True, blank=True)
    sentiment_score = models.FloatField(null=True, blank=True)  # -1 to 1
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'product']
    
    def __str__(self):
        return f"{self.user.username} - {self.product.name} - {self.rating}★"


class ProductRecommendation(models.Model):
    """Cached recommendations for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    recommended_products = models.ManyToManyField(Product, related_name='recommended_to')
    recommendation_type = models.CharField(max_length=50)  # collaborative, content_based, hybrid
    score = models.FloatField(default=0.0)
    generated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-generated_at']
    
    def __str__(self):
        return f"Recommendations for {self.user.username}"


class ChatMessage(TimeStampedModel):
    """Store chatbot conversations"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages', null=True, blank=True)
    session_id = models.CharField(max_length=100)
    message = models.TextField()
    response = models.TextField()
    intent = models.CharField(max_length=100, null=True, blank=True)
    confidence = models.FloatField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        user_name = self.user.username if self.user else "Anonymous"
        return f"{user_name} - {self.created_at}"


class UserPreference(models.Model):
    """Store user preferences for personalization"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='preferences')
    favorite_categories = models.JSONField(default=dict)  # {"category_id": weight}
    price_range_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_range_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    preferred_brands = models.JSONField(default=list)
    browsing_history_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"Preferences for {self.user.username}"
