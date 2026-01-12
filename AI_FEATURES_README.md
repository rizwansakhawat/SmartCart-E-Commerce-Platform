# SmartCart E-Commerce Platform with AI Features 🤖

## Overview
SmartCart is a modern, intelligent e-commerce platform built with Django that leverages artificial intelligence to provide personalized shopping experiences.

## ✨ AI Features Implemented

### 1. 🎯 Smart Product Recommendations
**Hybrid Recommendation Engine** combining three strategies:
- **Collaborative Filtering**: Recommends products based on similar users' preferences
- **Content-Based Filtering**: Suggests products similar to what users have viewed/purchased
- **Popularity-Based**: Shows trending products users haven't seen

**How it works:**
- Tracks user behavior (views, cart additions, purchases)
- Analyzes user preferences and browsing patterns
- Generates personalized recommendations on homepage
- Shows similar products on product detail pages

**API Endpoints:**
- `GET /ai/recommendations/` - Get personalized recommendations
- `GET /ai/recommendations/product/<id>/` - Get similar products

### 2. 💬 AI-Powered Sentiment Analysis
**Automatic Review Analysis** using NLP:
- Analyzes customer reviews for sentiment (positive, neutral, negative)
- Calculates sentiment scores (-1 to 1)
- Displays sentiment statistics on product pages
- Helps customers make informed decisions

**Features:**
- Rule-based sentiment analysis (fallback)
- Transformer model support (when available)
- Sentiment visualization on product pages
- Automatic sentiment detection on review submission

**API Endpoints:**
- `POST /ai/review/submit/` - Submit review with auto sentiment analysis
- `GET /ai/reviews/product/<id>/` - Get reviews with sentiment data

### 3. 🤖 Intelligent Chatbot Assistant
**AI Customer Support Bot** for:
- Product inquiries and search
- Order status tracking
- Shipping and return policy information
- Payment method questions
- Product recommendations

**Supported Intents:**
- Greeting
- Product search
- Order status
- Price inquiry
- Shipping information
- Return policy
- Payment methods
- Product recommendations
- Thanks & goodbye

**Features:**
- Real-time chat interface
- Context-aware responses
- Personalized suggestions
- Conversation history tracking

**API Endpoints:**
- `POST /ai/chat/` - Send message to chatbot
- `GET /ai/chat/history/` - Get conversation history

### 4. 📊 User Behavior Tracking
**Automatic tracking** of:
- Product views
- Add to cart actions
- Purchases
- Wishlist additions
- Search queries

**Purpose:**
- Powers recommendation engine
- Enables personalized experiences
- Provides analytics data
- Improves AI accuracy over time

**API Endpoints:**
- `POST /ai/track/` - Manually track user behavior

## 🛠️ Technical Architecture

### Models
- **UserBehavior**: Tracks all user interactions
- **ProductReview**: Stores reviews with sentiment analysis
- **ProductRecommendation**: Caches generated recommendations
- **ChatMessage**: Stores chatbot conversations
- **UserPreference**: Stores user preferences for personalization

### AI Components
1. **recommendation_engine.py**: Hybrid recommendation system
2. **sentiment_analysis.py**: NLP-based sentiment analyzer
3. **chatbot.py**: Intent-based conversational AI
4. **tracking.py**: Behavior tracking utilities

## 📦 Installation & Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Populate Sample Data
```bash
python manage.py populate_ai_data
```

### 4. Start Server
```bash
python manage.py runserver
```

## 🎮 Usage

### For Customers:
1. **Browse Products**: Get personalized recommendations on homepage
2. **View Product Details**: See AI-analyzed reviews and similar products
3. **Chat with AI**: Click chatbot icon for instant assistance
4. **Leave Reviews**: Automatic sentiment analysis applied

### For Admins:
1. **Admin Panel**: Access at `/admin/`
2. **View User Behaviors**: Track customer interactions
3. **Manage Reviews**: Approve/analyze customer reviews
4. **Monitor Chatbot**: View conversation history
5. **Analytics**: See user preferences and trends

## 📊 Admin Features

### AI Engine Admin Sections:
- **User Behaviors**: View all tracked user actions
- **Product Reviews**: Manage reviews with sentiment data
- **Product Recommendations**: View cached recommendations
- **Chat Messages**: Monitor chatbot conversations
- **User Preferences**: See personalized user data

### Admin Actions:
- Approve reviews in bulk
- Analyze sentiment for multiple reviews
- Track user behavior patterns

## 🚀 Future Enhancements

### Planned Features:
1. **Advanced NLP**: Integrate transformer models (BERT, GPT)
2. **Visual Search**: AI-powered image recognition
3. **Price Prediction**: ML-based dynamic pricing
4. **Fraud Detection**: AI-based transaction monitoring
5. **Voice Assistant**: Voice-enabled shopping
6. **Personalized Emails**: AI-generated marketing content
7. **Inventory Prediction**: ML-based stock forecasting
8. **Customer Segmentation**: AI-powered user clustering

### Performance Optimizations:
- Implement Redis caching
- Add Celery for background tasks
- Use PostgreSQL for production
- Deploy ML models separately
- Add CDN for static files

## 🔧 Configuration

### Settings (settings.py):
```python
INSTALLED_APPS = [
    ...
    'ai_engine',
]
```

### Optional AI Dependencies:
```bash
# For advanced sentiment analysis
pip install transformers torch

# For enhanced NLP
pip install nltk spacy

# For production
pip install redis celery
```

## 📝 API Documentation

### Authentication
Most AI endpoints require user authentication.

### Response Format
```json
{
    "success": true,
    "data": {...},
    "message": "Optional message"
}
```

### Error Handling
```json
{
    "success": false,
    "error": "Error description"
}
```

## 🧪 Testing

### Populate Test Data:
```bash
python manage.py populate_ai_data
```

### Test Users Created:
- Username: `testuser1` / Password: `password123`
- Username: `testuser2` / Password: `password123`
- Username: `testuser3` / Password: `password123`
- Username: `demo_user` / Password: `password123`

## 🤝 Contributing

### Areas for Contribution:
1. Improve recommendation algorithms
2. Add more chatbot intents
3. Enhance sentiment analysis accuracy
4. Create better UI/UX for AI features
5. Add more AI capabilities

## 📄 License
MIT License

## 👨‍💻 Author
M. Rizwan

## 🙏 Acknowledgments
- Django Framework
- scikit-learn for ML algorithms
- Transformers library for NLP
- Bootstrap for UI components

---

## Quick Start Commands

```bash
# Setup
python manage.py migrate
python manage.py populate_ai_data
python manage.py createsuperuser

# Run
python manage.py runserver

# Access
# - Website: http://127.0.0.1:8000/
# - Admin: http://127.0.0.1:8000/admin/
# - API: http://127.0.0.1:8000/ai/
```

**Enjoy your AI-powered SmartCart! 🛒✨**
