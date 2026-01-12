from django.urls import path
from ai_engine import views

app_name = 'ai_engine'

urlpatterns = [
    # Recommendations
    path('recommendations/', views.get_recommendations, name='recommendations'),
    path('recommendations/product/<int:product_id>/', views.get_similar_products, name='similar_products'),
    
    # Reviews
    path('review/submit/', views.submit_review, name='submit_review'),
    path('reviews/product/<int:product_id>/', views.get_product_reviews, name='product_reviews'),
    
    # Chatbot
    path('chat/', views.chat, name='chat'),
    path('chat/history/', views.chat_history, name='chat_history'),
    
    # User behavior
    path('track/', views.track_behavior, name='track_behavior'),
]
