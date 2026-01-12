from django.shortcuts import render
from django.views.generic import ListView, DetailView, DetailView, UpdateView
from .models import Product
from django.contrib.auth.mixins import LoginRequiredMixin
from ai_engine.recommendation_engine import RecommendationEngine
from ai_engine.tracking import track_user_behavior
from ai_engine.models import ProductReview

# Create your views here.

class ProductListView(ListView):
    model = Product
    template_name = "store/home.html"
    context_object_name = "products"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add AI-powered recommendations for authenticated users
        if self.request.user.is_authenticated:
            try:
                engine = RecommendationEngine()
                recommendations = engine.get_recommendations(self.request.user, limit=6)
                context['recommended_products'] = recommendations
            except Exception as e:
                print(f"Error getting recommendations: {e}")
                context['recommended_products'] = []
        
        return context
    

class ProductDetailView(LoginRequiredMixin ,DetailView):
    login_url = 'login'
    model = Product
    template_name = "store/product_detail.html"
    context_object_name= "product"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Track product view
        if self.request.user.is_authenticated:
            track_user_behavior(
                user=self.request.user,
                action='view',
                product=product,
                session_id=self.request.session.session_key
            )
        
        # Get similar products using AI
        try:
            engine = RecommendationEngine()
            similar_products = engine.get_similar_products(product, limit=6)
            context['similar_products'] = similar_products
        except Exception as e:
            print(f"Error getting similar products: {e}")
            context['similar_products'] = []
        
        # Get product reviews with sentiment
        reviews = ProductReview.objects.filter(
            product=product,
            is_approved=True
        ).select_related('user').order_by('-created_at')[:10]
        context['reviews'] = reviews
        
        # Calculate review statistics
        if reviews:
            total_reviews = reviews.count()
            avg_rating = sum(r.rating for r in reviews) / total_reviews
            sentiment_counts = {
                'positive': sum(1 for r in reviews if r.sentiment == 'positive'),
                'neutral': sum(1 for r in reviews if r.sentiment == 'neutral'),
                'negative': sum(1 for r in reviews if r.sentiment == 'negative'),
            }
            context['review_stats'] = {
                'total': total_reviews,
                'average_rating': round(avg_rating, 1),
                'sentiment_counts': sentiment_counts
            }
        
        return context

