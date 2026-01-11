# SmartCart – AI-Powered E-Commerce Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 Overview

SmartCart is a modern, intelligent e-commerce platform built with Django that leverages artificial intelligence to provide personalized shopping experiences. The platform features AI-powered product recommendations, sentiment analysis for reviews, and an intelligent chatbot assistant to enhance customer engagement and satisfaction.

## ✨ Key Features

### 🛍️ Core E-Commerce Functionality
- **Product Catalog Management** - Browse products with advanced filtering and search capabilities
- **Shopping Cart & Wishlist** - Seamless cart management with persistent sessions
- **Secure Checkout** - Integrated payment processing with Stripe/PayPal
- **Order Management** - Complete order lifecycle tracking and history
- **User Authentication** - Secure registration, login, and profile management
- **Product Reviews & Ratings** - Customer feedback system with moderation

### 🤖 AI-Powered Features
- **Smart Recommendations** - Hybrid recommendation engine combining collaborative filtering and content-based algorithms
- **Sentiment Analysis** - Automated review sentiment detection using NLP models
- **Intelligent Chatbot** - AI assistant for customer support and product inquiries
- **Personalized Experience** - Dynamic content based on user behavior and preferences

### 👨‍💼 Admin Features
- **Product Management** - Add, edit, and manage product inventory
- **Order Processing** - Monitor and manage customer orders
- **Analytics Dashboard** - Sales reports and user activity insights
- **Review Moderation** - Approve and manage customer reviews

## 🏗️ Architecture

SmartCart follows a **modular monolithic architecture** with microservices principles:

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Django Templates)               │
│              Bootstrap + JavaScript + AJAX                   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│              Django Backend (MVT + DRF APIs)                 │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐  │
│  │  Users   │ Catalog  │   Cart   │  Orders  │ Payments │  │
│  ├──────────┼──────────┼──────────┼──────────┼──────────┤  │
│  │ Reviews  │    AI    │ Chatbot  │Analytics │  Admin   │  │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘  │
└─────────────────────────────────────────────────────────────┘
                              ↓
    ┌─────────────┬──────────────────┬─────────────────┐
    ↓             ↓                  ↓                 ↓
┌─────────┐  ┌─────────┐      ┌──────────┐     ┌──────────┐
│PostgreSQL│  │  Redis  │      │  Celery  │     │ S3/Media │
│   DB    │  │  Cache  │      │ Workers  │     │ Storage  │
└─────────┘  └─────────┘      └──────────┘     └──────────┘
```

### System Components

1. **Frontend Layer** - Django Templates with Bootstrap for responsive UI
2. **Backend Layer** - Django with REST Framework for API endpoints
3. **Database** - PostgreSQL for persistent data storage
4. **Cache** - Redis for session management and performance optimization
5. **AI Engine** - ML modules for recommendations and sentiment analysis
6. **Background Jobs** - Celery for asynchronous task processing
7. **Payment Gateway** - Stripe/PayPal integration for secure transactions
8. **Media Storage** - S3-compatible storage for images and assets

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 4.2+
- **API**: Django REST Framework (DRF)
- **Database**: PostgreSQL
- **Cache**: Redis
- **Task Queue**: Celery
- **Message Broker**: Redis Streams / RabbitMQ

### Frontend
- **Template Engine**: Django Templates
- **CSS Framework**: Bootstrap 5
- **JavaScript**: Vanilla JS / jQuery for dynamic interactions

### AI/ML
- **Recommendation**: scikit-learn, FAISS/Annoy
- **NLP**: Transformers (DistilBERT), spaCy
- **Sentiment Analysis**: Fine-tuned transformer models
- **Chatbot**: Rule-based + LLM integration (OpenAI API)

### Payment Integration
- Stripe
- PayPal

### DevOps & Deployment
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Monitoring**: Sentry, Prometheus
- **Cloud Storage**: AWS S3 / MinIO / DigitalOcean Spaces

## 📦 Installation & Setup

### Prerequisites
- Python 3.10+
- PostgreSQL 13+
- Redis 6+
- Node.js (for frontend build tools, optional)

### 1. Clone the Repository
```bash
git clone https://github.com/rizwansakhawat/SmartCart-E-Commerce-Platform.git
cd SmartCart-E-Commerce-Platform
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/smartcart
REDIS_URL=redis://localhost:6379/0

# Payment Gateway
STRIPE_SECRET_KEY=your-stripe-secret-key
STRIPE_PUBLIC_KEY=your-stripe-public-key

# AI Services
OPENAI_API_KEY=your-openai-api-key

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-email-password

# AWS S3 (Optional)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser
```bash
python manage.py createsuperuser
```

### 7. Load Sample Data (Optional)
```bash
python manage.py loaddata fixtures/initial_data.json
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit `http://localhost:8000` to access the application.

### 9. Run Celery Worker (Separate Terminal)
```bash
celery -A smartcart worker -l info
```

### 10. Run Celery Beat (Scheduled Tasks)
```bash
celery -A smartcart beat -l info
```


### Authentication
```
POST /api/auth/register/     # User registration
POST /api/auth/login/        # User login
POST /api/auth/logout/       # User logout
POST /api/auth/refresh/      # Refresh token
```

### Products
```
GET    /api/products/                    # List products
GET    /api/products/{id}/               # Product detail
GET    /api/products/search/?q=query     # Search products
GET    /api/products/categories/         # List categories
```

### Cart
```
GET    /api/cart/                        # Get cart
POST   /api/cart/add/                    # Add to cart
PATCH  /api/cart/update/{item_id}/       # Update quantity
DELETE /api/cart/remove/{item_id}/       # Remove item
```

### Orders
```
GET    /api/orders/                      # List user orders
GET    /api/orders/{id}/                 # Order detail
POST   /api/orders/checkout/             # Create order
```

### AI Services
```
GET    /api/ai/recommendations/?user_id={id}  # Get recommendations
POST   /api/reviews/                           # Submit review (triggers sentiment analysis)
POST   /api/chatbot/message/                   # Chat with bot
```

### Reviews
```
GET    /api/reviews/?product_id={id}     # Get product reviews
POST   /api/reviews/                      # Submit review
```

Full API documentation available at `/api/docs/` (Swagger UI) when running the server.

## 🧪 Testing

### Run All Tests
```bash
python manage.py test
```

### Run Specific App Tests
```bash
python manage.py test users
python manage.py test catalog
python manage.py test ai
```

### Coverage Report
```bash
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

## 🚀 Deployment

### Docker Deployment

#### Build and Run with Docker Compose
```bash
docker-compose up --build
```

#### Production Deployment
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Manual Deployment Steps
1. Set `DEBUG=False` in settings
2. Configure allowed hosts
3. Collect static files: `python manage.py collectstatic`
4. Set up Gunicorn/uWSGI
5. Configure Nginx as reverse proxy
6. Set up SSL certificates (Let's Encrypt)
7. Configure database backups
8. Set up monitoring and logging

## 🔒 Security Features

- **Authentication**: JWT-based authentication with refresh tokens
- **Password Security**: Argon2 password hashing
- **HTTPS**: SSL/TLS encryption enforced in production
- **CSRF Protection**: Django's built-in CSRF middleware
- **SQL Injection**: ORM-based queries with parameterization
- **XSS Prevention**: Template auto-escaping
- **Payment Security**: PCI-DSS compliant payment processing
- **Rate Limiting**: API rate limiting with throttling
- **Data Encryption**: Sensitive data encrypted at rest

## 📊 Performance Optimization

- **Database Indexing**: Optimized queries with proper indexes
- **Redis Caching**: Frequently accessed data cached
- **Query Optimization**: select_related() and prefetch_related()
- **CDN Integration**: Static assets served via CDN
- **Image Optimization**: Compressed and lazy-loaded images
- **Asynchronous Processing**: Background tasks via Celery
- **Connection Pooling**: Database connection optimization

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards
- Follow PEP 8 style guide
- Write docstrings for all functions/classes
- Add unit tests for new features
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Rizwan Sakhawat** - *Initial work* - [@rizwansakhawat](https://github.com/rizwansakhawat)

## 🙏 Acknowledgments

- Django Framework and community
- scikit-learn for ML algorithms
- Hugging Face for transformer models
- Bootstrap for responsive UI components
- All contributors and supporters

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/rizwansakhawat/SmartCart-E-Commerce-Platform/issues)
- **Discussions**: [GitHub Discussions](https://github.com/rizwansakhawat/SmartCart-E-Commerce-Platform/discussions)
- **Email**: rizwansakhawat@example.com

---

**Note**: This project is under active development. Features and documentation are subject to change.

## 🗺️ Roadmap

### Phase 1 (Current)
- [x] Core e-commerce functionality
- [x] Basic recommendation engine
- [x] Sentiment analysis integration
- [x] Payment gateway integration

### Phase 2 (Planned)
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Multi-vendor support
- [ ] Social media integration
- [ ] Voice-based search

### Phase 3 (Future)
- [ ] AR product visualization
- [ ] Blockchain-based loyalty program
- [ ] Multi-language support
- [ ] Advanced fraud detection
- [ ] Marketplace ecosystem

---

Made with ❤️ by the SmartCart Team
