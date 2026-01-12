// AI-powered features JavaScript

// Chatbot functionality
class SmartCartChatbot {
    constructor() {
        this.chatContainer = null;
        this.messagesContainer = null;
        this.inputField = null;
        this.sendButton = null;
        this.isOpen = false;
        this.initChatbot();
    }

    initChatbot() {
        // Create chatbot UI
        this.createChatbotUI();
        this.attachEventListeners();
    }

    createChatbotUI() {
        const chatbotHTML = `
            <div id="chatbot-container" class="chatbot-container">
                <div class="chatbot-header">
                    <h4>SmartCart Assistant</h4>
                    <button id="close-chatbot" class="close-btn">&times;</button>
                </div>
                <div id="chatbot-messages" class="chatbot-messages">
                    <div class="bot-message">
                        <p>Hello! I'm your SmartCart AI assistant. How can I help you today?</p>
                    </div>
                </div>
                <div class="chatbot-input">
                    <input type="text" id="chatbot-input" placeholder="Type your message..." />
                    <button id="send-message" class="send-btn">Send</button>
                </div>
                <div id="chatbot-suggestions" class="chatbot-suggestions"></div>
            </div>
            <button id="chatbot-toggle" class="chatbot-toggle">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                </svg>
            </button>
        `;

        document.body.insertAdjacentHTML('beforeend', chatbotHTML);

        this.chatContainer = document.getElementById('chatbot-container');
        this.messagesContainer = document.getElementById('chatbot-messages');
        this.inputField = document.getElementById('chatbot-input');
        this.sendButton = document.getElementById('send-message');
    }

    attachEventListeners() {
        document.getElementById('chatbot-toggle').addEventListener('click', () => {
            this.toggleChat();
        });

        document.getElementById('close-chatbot').addEventListener('click', () => {
            this.toggleChat();
        });

        this.sendButton.addEventListener('click', () => {
            this.sendMessage();
        });

        this.inputField.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }

    toggleChat() {
        this.isOpen = !this.isOpen;
        this.chatContainer.style.display = this.isOpen ? 'flex' : 'none';
        if (this.isOpen) {
            this.inputField.focus();
        }
    }

    async sendMessage() {
        const message = this.inputField.value.trim();
        if (!message) return;

        // Display user message
        this.addMessage(message, 'user');
        this.inputField.value = '';

        // Show typing indicator
        this.showTypingIndicator();

        try {
            // Send to backend
            const response = await fetch('/ai/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            // Remove typing indicator
            this.removeTypingIndicator();

            if (data.success) {
                this.addMessage(data.response, 'bot');
                this.showSuggestions(data.suggestions);
            } else {
                this.addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }
        } catch (error) {
            this.removeTypingIndicator();
            this.addMessage('Sorry, I could not connect to the server.', 'bot');
        }
    }

    addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `${sender}-message`;
        messageDiv.innerHTML = `<p>${text}</p>`;
        this.messagesContainer.appendChild(messageDiv);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.id = 'typing-indicator';
        indicator.innerHTML = '<span></span><span></span><span></span>';
        this.messagesContainer.appendChild(indicator);
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    showSuggestions(suggestions) {
        const suggestionsContainer = document.getElementById('chatbot-suggestions');
        suggestionsContainer.innerHTML = '';

        if (suggestions && suggestions.length > 0) {
            suggestions.forEach(suggestion => {
                const button = document.createElement('button');
                button.className = 'suggestion-btn';
                button.textContent = suggestion;
                button.addEventListener('click', () => {
                    this.inputField.value = suggestion;
                    this.sendMessage();
                });
                suggestionsContainer.appendChild(button);
            });
        }
    }
}

// Product recommendations
async function loadRecommendations() {
    try {
        const response = await fetch('/ai/recommendations/?limit=6');
        const data = await response.json();

        if (data.success && data.recommendations.length > 0) {
            displayRecommendations(data.recommendations);
        }
    } catch (error) {
        console.error('Error loading recommendations:', error);
    }
}

function displayRecommendations(products) {
    const container = document.getElementById('ai-recommendations');
    if (!container) return;

    container.innerHTML = '<h3>Recommended for You</h3><div class="recommendations-grid"></div>';
    const grid = container.querySelector('.recommendations-grid');

    products.forEach(product => {
        const productCard = `
            <div class="product-card">
                <img src="${product.image || '/static/images/placeholder.jpg'}" alt="${product.name}">
                <h4>${product.name}</h4>
                <p class="price">$${product.price}</p>
                <a href="/product/${product.id}/" class="btn btn-primary">View Details</a>
            </div>
        `;
        grid.insertAdjacentHTML('beforeend', productCard);
    });
}

// Track user behavior
function trackBehavior(action, productId = null, searchQuery = null) {
    fetch('/ai/track/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            action: action,
            product_id: productId,
            search_query: searchQuery
        })
    }).catch(error => {
        console.error('Error tracking behavior:', error);
    });
}

// Submit review with sentiment analysis
async function submitReview(productId, rating, title, comment) {
    try {
        const response = await fetch('/ai/review/submit/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                product_id: productId,
                rating: rating,
                title: title,
                comment: comment
            })
        });

        const data = await response.json();

        if (data.success) {
            alert(data.message);
            return true;
        } else {
            alert('Error submitting review: ' + data.error);
            return false;
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        alert('Failed to submit review');
        return false;
    }
}

// Load product reviews
async function loadProductReviews(productId) {
    try {
        const response = await fetch(`/ai/reviews/product/${productId}/`);
        const data = await response.json();

        if (data.success) {
            displayReviews(data.reviews, data.sentiment_stats);
        }
    } catch (error) {
        console.error('Error loading reviews:', error);
    }
}

function displayReviews(reviews, sentimentStats) {
    const container = document.getElementById('product-reviews');
    if (!container) return;

    // Display sentiment statistics
    const statsHTML = `
        <div class="sentiment-stats">
            <h4>Customer Sentiment</h4>
            <div class="sentiment-bar">
                <div class="positive" style="width: ${sentimentStats.positive_percentage}%">
                    ${sentimentStats.positive_percentage}% Positive
                </div>
                <div class="neutral" style="width: ${sentimentStats.neutral_percentage}%">
                    ${sentimentStats.neutral_percentage}% Neutral
                </div>
                <div class="negative" style="width: ${sentimentStats.negative_percentage}%">
                    ${sentimentStats.negative_percentage}% Negative
                </div>
            </div>
        </div>
    `;

    container.innerHTML = statsHTML + '<div class="reviews-list"></div>';
    const reviewsList = container.querySelector('.reviews-list');

    reviews.forEach(review => {
        const sentimentClass = review.sentiment;
        const verifiedBadge = review.is_verified_purchase ? '<span class="verified-badge">✓ Verified Purchase</span>' : '';
        
        const reviewHTML = `
            <div class="review-card ${sentimentClass}">
                <div class="review-header">
                    <strong>${review.user}</strong>
                    <span class="rating">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</span>
                </div>
                <h5>${review.title}</h5>
                <p>${review.comment}</p>
                <div class="review-footer">
                    <span class="sentiment-badge ${sentimentClass}">${review.sentiment}</span>
                    ${verifiedBadge}
                    <span class="date">${review.created_at}</span>
                </div>
            </div>
        `;
        reviewsList.insertAdjacentHTML('beforeend', reviewHTML);
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize chatbot
    const chatbot = new SmartCartChatbot();

    // Load recommendations if container exists
    if (document.getElementById('ai-recommendations')) {
        loadRecommendations();
    }

    // Track product views
    const productId = document.querySelector('[data-product-id]');
    if (productId) {
        trackBehavior('view', productId.dataset.productId);
    }

    // Track search
    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const query = this.querySelector('input[name="q"]').value;
            trackBehavior('search', null, query);
        });
    }
});
