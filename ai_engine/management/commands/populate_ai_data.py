from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Product, Category
from ai_engine.models import UserBehavior, ProductReview
from ai_engine.sentiment_analysis import get_sentiment_analyzer
import random


class Command(BaseCommand):
    help = 'Populate AI engine with sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating AI engine with sample data...')
        
        # Get or create test users
        users = self._get_or_create_users()
        products = list(Product.objects.all())
        
        if not products:
            self.stdout.write(self.style.WARNING('No products found. Please add products first.'))
            return
        
        # Create sample user behaviors
        self._create_behaviors(users, products)
        
        # Create sample reviews
        self._create_reviews(users, products)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated AI engine with sample data!'))
    
    def _get_or_create_users(self):
        """Get or create test users"""
        users = []
        usernames = ['testuser1', 'testuser2', 'testuser3', 'demo_user']
        
        for username in usernames:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': f'{username}@example.com',
                    'first_name': username.title()
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {username}')
            users.append(user)
        
        return users
    
    def _create_behaviors(self, users, products):
        """Create sample user behaviors"""
        actions = ['view', 'add_to_cart', 'purchase', 'wishlist']
        
        for user in users:
            # Create 10-20 random behaviors per user
            num_behaviors = random.randint(10, 20)
            
            for _ in range(num_behaviors):
                product = random.choice(products)
                action = random.choice(actions)
                
                UserBehavior.objects.get_or_create(
                    user=user,
                    product=product,
                    action=action
                )
        
        total = UserBehavior.objects.count()
        self.stdout.write(f'Created {total} user behaviors')
    
    def _create_reviews(self, users, products):
        """Create sample product reviews with sentiment analysis"""
        sample_reviews = [
            {
                'rating': 5,
                'title': 'Excellent product!',
                'comment': 'This product is amazing! Great quality and fast delivery. Highly recommend to everyone.'
            },
            {
                'rating': 4,
                'title': 'Good value for money',
                'comment': 'Pretty good product overall. Works as expected. Would buy again.'
            },
            {
                'rating': 3,
                'title': 'Average product',
                'comment': 'It\'s okay. Nothing special but does the job. Could be better.'
            },
            {
                'rating': 2,
                'title': 'Disappointed',
                'comment': 'Not what I expected. Quality could be much better. Somewhat disappointed.'
            },
            {
                'rating': 5,
                'title': 'Love it!',
                'comment': 'Absolutely love this! Best purchase ever. Exceeded all my expectations.'
            },
            {
                'rating': 4,
                'title': 'Nice quality',
                'comment': 'Good quality product. Very satisfied with my purchase. Recommend it.'
            },
            {
                'rating': 1,
                'title': 'Poor quality',
                'comment': 'Terrible product. Very disappointed. Would not recommend to anyone.'
            },
            {
                'rating': 5,
                'title': 'Perfect!',
                'comment': 'Perfect in every way! Great product, great service. Very happy customer.'
            },
        ]
        
        analyzer = get_sentiment_analyzer()
        
        for user in users:
            # Each user reviews 2-4 products
            num_reviews = random.randint(2, 4)
            reviewed_products = random.sample(products, min(num_reviews, len(products)))
            
            for product in reviewed_products:
                review_data = random.choice(sample_reviews)
                
                # Analyze sentiment
                sentiment, score = analyzer.analyze(review_data['comment'])
                
                ProductReview.objects.get_or_create(
                    user=user,
                    product=product,
                    defaults={
                        'rating': review_data['rating'],
                        'title': review_data['title'],
                        'comment': review_data['comment'],
                        'sentiment': sentiment,
                        'sentiment_score': score,
                        'is_approved': True,
                        'is_verified_purchase': random.choice([True, False])
                    }
                )
        
        total = ProductReview.objects.count()
        self.stdout.write(f'Created {total} product reviews')
