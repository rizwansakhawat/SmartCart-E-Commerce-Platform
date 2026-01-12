"""
Middleware and utilities for tracking user behavior
"""
from ai_engine.models import UserBehavior


def track_user_behavior(user, action, product=None, search_query=None, session_id=None):
    """
    Track user behavior for AI personalization
    
    Args:
        user: User object
        action: 'view', 'add_to_cart', 'purchase', 'wishlist', 'search'
        product: Product object (optional)
        search_query: Search query string (optional)
        session_id: Session ID (optional)
    """
    try:
        if user and user.is_authenticated:
            UserBehavior.objects.create(
                user=user,
                action=action,
                product=product,
                search_query=search_query,
                session_id=session_id
            )
            return True
    except Exception as e:
        print(f"Error tracking user behavior: {e}")
    return False


def get_user_behavior_summary(user):
    """Get summary of user behavior"""
    try:
        from django.db.models import Count
        from ai_engine.models import UserBehavior
        
        behaviors = UserBehavior.objects.filter(user=user)
        
        summary = {
            'total_actions': behaviors.count(),
            'views': behaviors.filter(action='view').count(),
            'cart_additions': behaviors.filter(action='add_to_cart').count(),
            'purchases': behaviors.filter(action='purchase').count(),
            'wishlist_additions': behaviors.filter(action='wishlist').count(),
            'searches': behaviors.filter(action='search').count(),
            'most_viewed_products': list(
                behaviors.filter(action='view', product__isnull=False)
                .values('product__id', 'product__name')
                .annotate(view_count=Count('id'))
                .order_by('-view_count')[:5]
            )
        }
        
        return summary
    except Exception as e:
        print(f"Error getting behavior summary: {e}")
        return {}


class UserBehaviorMiddleware:
    """Middleware to automatically track page views"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Track product views
        if request.user.is_authenticated and request.path.startswith('/product/'):
            try:
                # Extract product ID from URL
                import re
                match = re.search(r'/product/(\d+)/', request.path)
                if match:
                    product_id = match.group(1)
                    from store.models import Product
                    try:
                        product = Product.objects.get(id=product_id)
                        track_user_behavior(
                            user=request.user,
                            action='view',
                            product=product,
                            session_id=request.session.session_key
                        )
                    except Product.DoesNotExist:
                        pass
            except Exception as e:
                print(f"Error in behavior middleware: {e}")
        
        return response
