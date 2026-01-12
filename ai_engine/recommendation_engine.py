"""
AI-powered recommendation engine using hybrid approach
Combines collaborative filtering and content-based filtering
"""
from collections import defaultdict, Counter
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Q
from store.models import Product, Category
from ai_engine.models import UserBehavior, ProductReview, UserPreference


class RecommendationEngine:
    """Hybrid recommendation system"""
    
    def __init__(self):
        self.collaborative_weight = 0.5
        self.content_weight = 0.3
        self.popularity_weight = 0.2
    
    def get_recommendations(self, user, limit=10):
        """Get personalized recommendations for a user"""
        try:
            # Get recommendations from different strategies
            collaborative_recs = self._collaborative_filtering(user, limit * 2)
            content_recs = self._content_based_filtering(user, limit * 2)
            popular_recs = self._popularity_based(user, limit)
            
            # Combine and score recommendations
            combined_scores = defaultdict(float)
            
            # Add collaborative filtering scores
            for product_id, score in collaborative_recs:
                combined_scores[product_id] += score * self.collaborative_weight
            
            # Add content-based scores
            for product_id, score in content_recs:
                combined_scores[product_id] += score * self.content_weight
            
            # Add popularity scores
            for product_id, score in popular_recs:
                combined_scores[product_id] += score * self.popularity_weight
            
            # Sort by combined score
            sorted_recommendations = sorted(
                combined_scores.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:limit]
            
            # Get product objects
            product_ids = [pid for pid, _ in sorted_recommendations]
            products = Product.objects.filter(id__in=product_ids)
            
            # Maintain order
            product_dict = {p.id: p for p in products}
            recommended_products = [product_dict[pid] for pid in product_ids if pid in product_dict]
            
            return recommended_products
            
        except Exception as e:
            print(f"Error generating recommendations: {e}")
            # Fallback to popular products
            return Product.objects.annotate(
                order_count=Count('orderitem')
            ).order_by('-order_count')[:limit]
    
    def _collaborative_filtering(self, user, limit=20):
        """Find similar users and recommend products they liked"""
        try:
            # Get user's interactions
            user_products = set(
                UserBehavior.objects.filter(
                    user=user, 
                    action__in=['purchase', 'add_to_cart', 'wishlist']
                ).values_list('product_id', flat=True)
            )
            
            if not user_products:
                return []
            
            # Find similar users who interacted with same products
            similar_users = User.objects.filter(
                behaviors__product_id__in=user_products
            ).exclude(id=user.id).annotate(
                common_products=Count('behaviors')
            ).order_by('-common_products')[:20]
            
            # Get products these similar users liked
            recommendations = defaultdict(float)
            for similar_user in similar_users:
                similarity_score = similar_user.common_products / max(len(user_products), 1)
                
                # Get products the similar user liked but current user hasn't interacted with
                liked_products = UserBehavior.objects.filter(
                    user=similar_user,
                    action__in=['purchase', 'add_to_cart', 'wishlist']
                ).exclude(
                    product_id__in=user_products
                ).values_list('product_id', flat=True)
                
                for product_id in liked_products:
                    recommendations[product_id] += similarity_score
            
            # Sort by score
            sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:limit]
            return sorted_recs
            
        except Exception as e:
            print(f"Collaborative filtering error: {e}")
            return []
    
    def _content_based_filtering(self, user, limit=20):
        """Recommend products similar to user's preferences"""
        try:
            # Get user's interaction history
            user_interactions = UserBehavior.objects.filter(
                user=user,
                product__isnull=False
            ).select_related('product')
            
            if not user_interactions.exists():
                return []
            
            # Extract features from user's liked products
            liked_categories = defaultdict(int)
            liked_products = []
            
            for interaction in user_interactions:
                product = interaction.product
                liked_products.append(product.id)
                
                # Weight by action type
                weight = self._get_action_weight(interaction.action)
                
                # Count category preferences
                for category in product.categories.all():
                    liked_categories[category.id] += weight
            
            if not liked_categories:
                return []
            
            # Find products with similar categories
            recommendations = defaultdict(float)
            
            # Get products from preferred categories
            for category_id, preference_score in liked_categories.items():
                similar_products = Product.objects.filter(
                    categories__id=category_id
                ).exclude(
                    id__in=liked_products
                ).values_list('id', flat=True)[:50]
                
                for product_id in similar_products:
                    recommendations[product_id] += preference_score
            
            # Sort by score
            sorted_recs = sorted(recommendations.items(), key=lambda x: x[1], reverse=True)[:limit]
            return sorted_recs
            
        except Exception as e:
            print(f"Content-based filtering error: {e}")
            return []
    
    def _popularity_based(self, user, limit=10):
        """Recommend popular products user hasn't seen"""
        try:
            # Get products user has already interacted with
            user_products = set(
                UserBehavior.objects.filter(user=user).values_list('product_id', flat=True)
            )
            
            # Get popular products based on multiple factors
            popular_products = Product.objects.exclude(
                id__in=user_products
            ).annotate(
                order_count=Count('orderitem'),
                review_count=Count('reviews'),
                avg_rating=Avg('reviews__rating'),
                view_count=Count('userbehavior', filter=Q(userbehavior__action='view'))
            ).filter(
                order_count__gt=0  # Has at least one order
            ).order_by('-order_count', '-view_count')[:limit]
            
            # Calculate popularity scores
            scores = []
            for product in popular_products:
                score = (
                    (product.order_count or 0) * 3 +
                    (product.view_count or 0) * 1 +
                    (product.review_count or 0) * 2 +
                    (product.avg_rating or 0) * 10
                )
                scores.append((product.id, score))
            
            return scores
            
        except Exception as e:
            print(f"Popularity-based error: {e}")
            return []
    
    def _get_action_weight(self, action):
        """Get weight for different user actions"""
        weights = {
            'purchase': 5,
            'add_to_cart': 3,
            'wishlist': 2,
            'view': 1,
            'search': 0.5
        }
        return weights.get(action, 1)
    
    def get_similar_products(self, product, limit=6):
        """Find products similar to a given product"""
        try:
            # Get products from same categories
            categories = product.categories.all()
            
            similar_products = Product.objects.filter(
                categories__in=categories
            ).exclude(
                id=product.id
            ).annotate(
                common_categories=Count('categories')
            ).order_by('-common_categories')[:limit]
            
            return list(similar_products)
            
        except Exception as e:
            print(f"Similar products error: {e}")
            return []
    
    def update_user_preferences(self, user):
        """Update user preferences based on behavior"""
        try:
            preferences, created = UserPreference.objects.get_or_create(user=user)
            
            # Analyze user behavior
            behaviors = UserBehavior.objects.filter(
                user=user,
                product__isnull=False
            ).select_related('product')
            
            # Count category preferences
            category_counts = defaultdict(int)
            for behavior in behaviors:
                weight = self._get_action_weight(behavior.action)
                for category in behavior.product.categories.all():
                    category_counts[category.id] += weight
            
            # Update preferences
            preferences.favorite_categories = dict(category_counts)
            preferences.browsing_history_count = behaviors.count()
            preferences.save()
            
            return preferences
            
        except Exception as e:
            print(f"Update preferences error: {e}")
            return None
