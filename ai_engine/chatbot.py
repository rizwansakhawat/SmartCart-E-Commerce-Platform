"""
AI-powered chatbot for customer support
Handles product inquiries, order status, and general questions
"""
import re
from typing import Dict, Tuple
from django.contrib.auth.models import User
from store.models import Product, Category
from orders.models import Order
from datetime import datetime, timedelta


class Chatbot:
    """Intelligent chatbot assistant"""
    
    def __init__(self):
        self.intents = self._load_intents()
    
    def _load_intents(self) -> Dict:
        """Define chatbot intents and patterns"""
        return {
            'greeting': {
                'patterns': [
                    r'\b(hi|hello|hey|greetings|good\s+(morning|afternoon|evening))\b',
                ],
                'responses': [
                    "Hello! Welcome to SmartCart. How can I assist you today?",
                    "Hi there! I'm here to help you with your shopping. What can I do for you?",
                    "Hey! Thanks for reaching out. What would you like to know?"
                ]
            },
            'product_search': {
                'patterns': [
                    r'\b(search|find|looking for|show me|need)\b.*\b(product|item)\b',
                    r'\bdo you (have|sell)\b',
                    r'\bwhere (can i find|is)\b'
                ],
                'responses': [
                    "I can help you find products. What are you looking for?",
                    "Sure! What type of product are you interested in?"
                ]
            },
            'order_status': {
                'patterns': [
                    r'\b(order|orders|purchase)\b.*\b(status|track|where|when)\b',
                    r'\btrack\s+(my\s+)?order\b',
                    r'\bwhere\s+(is\s+)?my\s+order\b'
                ],
                'responses': [
                    "I can help you track your order. Could you provide your order number?",
                    "Let me check your order status. What's your order ID?"
                ]
            },
            'price_inquiry': {
                'patterns': [
                    r'\b(price|cost|how much)\b',
                    r'\bhow much (does|is)\b'
                ],
                'responses': [
                    "I can help with pricing information. Which product are you asking about?",
                    "Let me get you the price details. What product interests you?"
                ]
            },
            'shipping': {
                'patterns': [
                    r'\b(shipping|delivery|ship|deliver)\b',
                    r'\bhow long\b.*\b(deliver|arrive|shipping)\b',
                    r'\bshipping\s+(cost|fee|charge)\b'
                ],
                'responses': [
                    "We offer standard shipping (5-7 business days) and express shipping (2-3 business days). Shipping is free on orders over $50!",
                    "Delivery typically takes 5-7 business days for standard shipping. Would you like more details?"
                ]
            },
            'return_policy': {
                'patterns': [
                    r'\b(return|refund|exchange)\b',
                    r'\bcan i return\b',
                    r'\breturn policy\b'
                ],
                'responses': [
                    "We have a 30-day return policy. Items must be unused and in original packaging. Would you like to start a return?",
                    "You can return items within 30 days of purchase for a full refund. Need help with a return?"
                ]
            },
            'payment': {
                'patterns': [
                    r'\b(payment|pay|credit card|debit card|stripe|paypal)\b',
                    r'\bhow (to|do i) pay\b',
                    r'\bpayment methods\b'
                ],
                'responses': [
                    "We accept credit/debit cards, Stripe, and PayPal. You can also pay cash on delivery for eligible orders.",
                    "You can pay using various methods: credit cards, Stripe, PayPal, or cash on delivery."
                ]
            },
            'recommendations': {
                'patterns': [
                    r'\b(recommend|suggest|popular|bestseller|trending)\b',
                    r'\bwhat should i buy\b',
                    r'\bshow me\b.*\b(popular|best|top)\b'
                ],
                'responses': [
                    "I'd love to recommend products! What category are you interested in?",
                    "Based on our popular items, I can suggest some great products. What are you looking for?"
                ]
            },
            'thanks': {
                'patterns': [
                    r'\b(thank|thanks|thx|appreciate)\b',
                ],
                'responses': [
                    "You're welcome! Is there anything else I can help you with?",
                    "Happy to help! Let me know if you need anything else.",
                    "My pleasure! Feel free to ask if you have more questions."
                ]
            },
            'goodbye': {
                'patterns': [
                    r'\b(bye|goodbye|see you|later|exit)\b',
                ],
                'responses': [
                    "Goodbye! Happy shopping!",
                    "See you later! Come back anytime you need help.",
                    "Bye! Thanks for visiting SmartCart!"
                ]
            }
        }
    
    def process_message(self, message: str, user: User = None, session_id: str = None) -> Dict:
        """Process user message and generate response"""
        message = message.lower().strip()
        
        # Detect intent
        intent, confidence = self._detect_intent(message)
        
        # Generate response based on intent
        response = self._generate_response(intent, message, user)
        
        # Store conversation
        if user or session_id:
            self._store_message(user, session_id, message, response, intent, confidence)
        
        return {
            'response': response,
            'intent': intent,
            'confidence': confidence,
            'suggestions': self._get_suggestions(intent)
        }
    
    def _detect_intent(self, message: str) -> Tuple[str, float]:
        """Detect user intent from message"""
        for intent, data in self.intents.items():
            for pattern in data['patterns']:
                if re.search(pattern, message, re.IGNORECASE):
                    # Simple confidence based on match
                    confidence = 0.85
                    return intent, confidence
        
        # Default intent if no match
        return 'general', 0.5
    
    def _generate_response(self, intent: str, message: str, user: User = None) -> str:
        """Generate response based on intent"""
        import random
        
        if intent in self.intents:
            responses = self.intents[intent]['responses']
            base_response = random.choice(responses)
            
            # Add personalized context
            if intent == 'order_status' and user:
                recent_orders = Order.objects.filter(user=user).order_by('-created_at')[:3]
                if recent_orders:
                    order_info = "\n\nYour recent orders:\n"
                    for order in recent_orders:
                        order_info += f"- Order #{order.id}: {order.status.title()} (${order.total_price})\n"
                    return base_response + order_info
            
            elif intent == 'recommendations' and user:
                # Get quick recommendations
                from ai_engine.recommendation_engine import RecommendationEngine
                engine = RecommendationEngine()
                products = engine.get_recommendations(user, limit=3)
                
                if products:
                    product_list = "\n\nHere are some products you might like:\n"
                    for product in products:
                        product_list += f"- {product.name} (${product.price})\n"
                    return base_response + product_list
            
            elif intent == 'product_search':
                # Extract product name from message
                products = self._search_products(message)
                if products:
                    product_list = "\n\nI found these products:\n"
                    for product in products[:5]:
                        product_list += f"- {product.name} (${product.price})\n"
                    return product_list
            
            return base_response
        
        # General response
        return (
            "I'm here to help! I can assist you with:\n"
            "- Finding products\n"
            "- Checking order status\n"
            "- Answering questions about shipping, returns, and payments\n"
            "- Product recommendations\n"
            "What would you like to know?"
        )
    
    def _search_products(self, query: str) -> list:
        """Search for products based on query"""
        try:
            # Extract potential product keywords
            words = re.findall(r'\b\w+\b', query)
            keywords = [w for w in words if len(w) > 3]
            
            if not keywords:
                return []
            
            # Search in product names and descriptions
            from django.db.models import Q
            query_filter = Q()
            for keyword in keywords:
                query_filter |= Q(name__icontains=keyword) | Q(description__icontains=keyword)
            
            products = Product.objects.filter(query_filter).distinct()[:5]
            return list(products)
            
        except Exception as e:
            print(f"Product search error: {e}")
            return []
    
    def _get_suggestions(self, intent: str) -> list:
        """Get suggested follow-up questions"""
        suggestions = {
            'greeting': [
                "Show me trending products",
                "Track my order",
                "What's your return policy?"
            ],
            'product_search': [
                "Show me similar products",
                "What are the best sellers?",
                "Filter by price"
            ],
            'order_status': [
                "When will my order arrive?",
                "Cancel my order",
                "Change delivery address"
            ],
            'general': [
                "Find products",
                "Check order status",
                "Get recommendations"
            ]
        }
        return suggestions.get(intent, suggestions['general'])
    
    def _store_message(self, user: User, session_id: str, message: str, 
                      response: str, intent: str, confidence: float):
        """Store chat message in database"""
        try:
            from ai_engine.models import ChatMessage
            ChatMessage.objects.create(
                user=user,
                session_id=session_id,
                message=message,
                response=response,
                intent=intent,
                confidence=confidence
            )
        except Exception as e:
            print(f"Error storing chat message: {e}")
    
    def get_conversation_history(self, user: User = None, session_id: str = None, limit: int = 10):
        """Get conversation history"""
        try:
            from ai_engine.models import ChatMessage
            
            if user:
                messages = ChatMessage.objects.filter(user=user)
            elif session_id:
                messages = ChatMessage.objects.filter(session_id=session_id)
            else:
                return []
            
            return list(messages.order_by('-created_at')[:limit])
            
        except Exception as e:
            print(f"Error fetching conversation history: {e}")
            return []


# Singleton instance
_chatbot = None


def get_chatbot():
    """Get or create chatbot instance"""
    global _chatbot
    if _chatbot is None:
        _chatbot = Chatbot()
    return _chatbot
