from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from store.models import Product
from ai_engine.models import ProductReview, ChatMessage
from ai_engine.recommendation_engine import RecommendationEngine
from ai_engine.sentiment_analysis import get_sentiment_analyzer
from ai_engine.chatbot import get_chatbot
from ai_engine.tracking import track_user_behavior
from orders.models import Order


@login_required
@require_http_methods(["GET"])
def get_recommendations(request):
    """Get AI-powered product recommendations for the user"""
    try:
        engine = RecommendationEngine()
        limit = int(request.GET.get('limit', 10))
        products = engine.get_recommendations(request.user, limit=limit)
        
        recommendations = [{
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'description': p.description[:200],
            'image': p.images.first().image.url if p.images.exists() else None,
        } for p in products]
        
        return JsonResponse({
            'success': True,
            'recommendations': recommendations
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def get_similar_products(request, product_id):
    """Get products similar to a specific product"""
    try:
        product = get_object_or_404(Product, id=product_id)
        engine = RecommendationEngine()
        limit = int(request.GET.get('limit', 6))
        similar_products = engine.get_similar_products(product, limit=limit)
        
        products_data = [{
            'id': p.id,
            'name': p.name,
            'price': float(p.price),
            'description': p.description[:200],
            'image': p.images.first().image.url if p.images.exists() else None,
        } for p in similar_products]
        
        return JsonResponse({
            'success': True,
            'similar_products': products_data
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_POST
def submit_review(request):
    """Submit a product review with automatic sentiment analysis"""
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        rating = data.get('rating')
        title = data.get('title')
        comment = data.get('comment')
        
        # Validate input
        if not all([product_id, rating, title, comment]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required fields'
            }, status=400)
        
        product = get_object_or_404(Product, id=product_id)
        
        # Check if user has purchased the product
        has_purchased = Order.objects.filter(
            user=request.user,
            items__product=product,
            is_paid=True
        ).exists()
        
        # Analyze sentiment
        analyzer = get_sentiment_analyzer()
        sentiment, sentiment_score = analyzer.analyze(comment)
        
        # Create or update review
        review, created = ProductReview.objects.update_or_create(
            user=request.user,
            product=product,
            defaults={
                'rating': rating,
                'title': title,
                'comment': comment,
                'sentiment': sentiment,
                'sentiment_score': sentiment_score,
                'is_verified_purchase': has_purchased,
                'is_approved': False  # Requires admin approval
            }
        )
        
        return JsonResponse({
            'success': True,
            'review': {
                'id': review.id,
                'rating': review.rating,
                'sentiment': review.sentiment,
                'is_verified_purchase': review.is_verified_purchase
            },
            'message': 'Review submitted successfully! It will appear after approval.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@require_http_methods(["GET"])
def get_product_reviews(request, product_id):
    """Get reviews for a product with sentiment analysis"""
    try:
        product = get_object_or_404(Product, id=product_id)
        reviews = ProductReview.objects.filter(
            product=product,
            is_approved=True
        ).select_related('user')
        
        # Pagination
        page = int(request.GET.get('page', 1))
        paginator = Paginator(reviews, 10)
        reviews_page = paginator.get_page(page)
        
        # Get sentiment statistics
        analyzer = get_sentiment_analyzer()
        all_comments = [r.comment for r in reviews]
        sentiment_stats = analyzer.get_overall_sentiment(all_comments)
        
        reviews_data = [{
            'id': r.id,
            'user': r.user.username,
            'rating': r.rating,
            'title': r.title,
            'comment': r.comment,
            'sentiment': r.sentiment,
            'is_verified_purchase': r.is_verified_purchase,
            'helpful_count': r.helpful_count,
            'created_at': r.created_at.strftime('%Y-%m-%d')
        } for r in reviews_page]
        
        return JsonResponse({
            'success': True,
            'reviews': reviews_data,
            'sentiment_stats': sentiment_stats,
            'pagination': {
                'current_page': page,
                'total_pages': paginator.num_pages,
                'total_reviews': paginator.count
            }
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_POST
def chat(request):
    """Handle chatbot conversations"""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        
        if not message:
            return JsonResponse({
                'success': False,
                'error': 'Message cannot be empty'
            }, status=400)
        
        # Get or create session ID
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        
        # Get chatbot response
        chatbot = get_chatbot()
        user = request.user if request.user.is_authenticated else None
        result = chatbot.process_message(message, user=user, session_id=session_id)
        
        return JsonResponse({
            'success': True,
            'response': result['response'],
            'intent': result['intent'],
            'suggestions': result['suggestions']
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_http_methods(["GET"])
def chat_history(request):
    """Get chat history for the user"""
    try:
        chatbot = get_chatbot()
        limit = int(request.GET.get('limit', 20))
        messages = chatbot.get_conversation_history(user=request.user, limit=limit)
        
        history = [{
            'message': msg.message,
            'response': msg.response,
            'intent': msg.intent,
            'created_at': msg.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for msg in messages]
        
        return JsonResponse({
            'success': True,
            'history': history
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_POST
def track_behavior(request):
    """Track user behavior for personalization"""
    try:
        data = json.loads(request.body)
        action = data.get('action')
        product_id = data.get('product_id')
        search_query = data.get('search_query')
        
        if not action:
            return JsonResponse({
                'success': False,
                'error': 'Action is required'
            }, status=400)
        
        product = None
        if product_id:
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                pass
        
        session_id = request.session.session_key
        success = track_user_behavior(
            user=request.user,
            action=action,
            product=product,
            search_query=search_query,
            session_id=session_id
        )
        
        return JsonResponse({
            'success': success
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
