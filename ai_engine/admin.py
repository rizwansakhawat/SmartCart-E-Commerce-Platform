from django.contrib import admin
from ai_engine.models import (
    UserBehavior, ProductReview, ProductRecommendation,
    ChatMessage, UserPreference
)


@admin.register(UserBehavior)
class UserBehaviorAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'product', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['user__username', 'product__name', 'search_query']
    date_hierarchy = 'created_at'
    raw_id_fields = ['user', 'product']


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'rating', 'sentiment', 'is_approved', 'created_at']
    list_filter = ['rating', 'sentiment', 'is_approved', 'is_verified_purchase', 'created_at']
    search_fields = ['user__username', 'product__name', 'title', 'comment']
    actions = ['approve_reviews', 'analyze_sentiment']
    raw_id_fields = ['user', 'product']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"{queryset.count()} reviews approved.")
    approve_reviews.short_description = "Approve selected reviews"
    
    def analyze_sentiment(self, request, queryset):
        from ai_engine.sentiment_analysis import get_sentiment_analyzer
        analyzer = get_sentiment_analyzer()
        
        count = 0
        for review in queryset:
            sentiment, score = analyzer.analyze(review.comment)
            review.sentiment = sentiment
            review.sentiment_score = score
            review.save()
            count += 1
        
        self.message_user(request, f"Analyzed sentiment for {count} reviews.")
    analyze_sentiment.short_description = "Analyze sentiment for selected reviews"


@admin.register(ProductRecommendation)
class ProductRecommendationAdmin(admin.ModelAdmin):
    list_display = ['user', 'recommendation_type', 'score', 'generated_at']
    list_filter = ['recommendation_type', 'generated_at']
    search_fields = ['user__username']
    raw_id_fields = ['user']
    filter_horizontal = ['recommended_products']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'intent', 'confidence', 'created_at']
    list_filter = ['intent', 'created_at']
    search_fields = ['user__username', 'message', 'response', 'session_id']
    date_hierarchy = 'created_at'
    raw_id_fields = ['user']


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'browsing_history_count']
    search_fields = ['user__username']
    raw_id_fields = ['user']
