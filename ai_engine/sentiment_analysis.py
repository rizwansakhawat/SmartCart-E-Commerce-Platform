"""
Sentiment analysis for product reviews using NLP
Uses transformers library for pre-trained models
"""
from typing import Tuple, Dict
import re


class SentimentAnalyzer:
    """Analyze sentiment of product reviews"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the sentiment analysis model"""
        try:
            from transformers import pipeline
            # Use a lightweight sentiment analysis model
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=-1  # Use CPU
            )
        except ImportError:
            print("Transformers not installed. Using rule-based sentiment analysis.")
            self.sentiment_pipeline = None
        except Exception as e:
            print(f"Could not load transformer model: {e}")
            self.sentiment_pipeline = None
    
    def analyze(self, text: str) -> Tuple[str, float]:
        """
        Analyze sentiment of text
        Returns: (sentiment, score)
        - sentiment: 'positive', 'neutral', or 'negative'
        - score: float between -1 (very negative) and 1 (very positive)
        """
        if not text or not text.strip():
            return 'neutral', 0.0
        
        try:
            # Use transformer model if available
            if self.sentiment_pipeline:
                result = self.sentiment_pipeline(text[:512])[0]  # Limit text length
                label = result['label']
                confidence = result['score']
                
                # Convert to our format
                if label == 'POSITIVE':
                    sentiment = 'positive'
                    score = confidence
                elif label == 'NEGATIVE':
                    sentiment = 'negative'
                    score = -confidence
                else:
                    sentiment = 'neutral'
                    score = 0.0
                
                return sentiment, score
            else:
                # Fallback to rule-based sentiment analysis
                return self._rule_based_sentiment(text)
                
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return self._rule_based_sentiment(text)
    
    def _rule_based_sentiment(self, text: str) -> Tuple[str, float]:
        """Simple rule-based sentiment analysis as fallback"""
        text = text.lower()
        
        # Positive and negative word lists
        positive_words = {
            'good', 'great', 'excellent', 'amazing', 'awesome', 'love', 'perfect',
            'best', 'wonderful', 'fantastic', 'beautiful', 'nice', 'happy',
            'satisfied', 'recommend', 'quality', 'worth', 'impressed', 'superb'
        }
        
        negative_words = {
            'bad', 'terrible', 'awful', 'horrible', 'poor', 'worst', 'hate',
            'disappointing', 'disappointed', 'waste', 'useless', 'broken',
            'defective', 'cheap', 'overpriced', 'damaged', 'fake', 'scam'
        }
        
        # Count positive and negative words
        words = re.findall(r'\b\w+\b', text)
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        # Calculate score
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words == 0:
            return 'neutral', 0.0
        
        score = (positive_count - negative_count) / total_sentiment_words
        
        # Determine sentiment category
        if score > 0.2:
            sentiment = 'positive'
        elif score < -0.2:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return sentiment, score
    
    def analyze_review_batch(self, reviews: list) -> list:
        """Analyze sentiment for multiple reviews"""
        results = []
        for review in reviews:
            sentiment, score = self.analyze(review)
            results.append({
                'text': review,
                'sentiment': sentiment,
                'score': score
            })
        return results
    
    def get_overall_sentiment(self, reviews: list) -> Dict:
        """Get overall sentiment statistics for a product"""
        if not reviews:
            return {
                'average_score': 0.0,
                'positive_percentage': 0,
                'neutral_percentage': 0,
                'negative_percentage': 0,
                'total_reviews': 0
            }
        
        sentiments = [self.analyze(review) for review in reviews]
        
        positive_count = sum(1 for s, _ in sentiments if s == 'positive')
        neutral_count = sum(1 for s, _ in sentiments if s == 'neutral')
        negative_count = sum(1 for s, _ in sentiments if s == 'negative')
        total = len(sentiments)
        
        average_score = sum(score for _, score in sentiments) / total if total > 0 else 0
        
        return {
            'average_score': round(average_score, 2),
            'positive_percentage': round((positive_count / total) * 100, 1),
            'neutral_percentage': round((neutral_count / total) * 100, 1),
            'negative_percentage': round((negative_count / total) * 100, 1),
            'total_reviews': total,
            'sentiment_distribution': {
                'positive': positive_count,
                'neutral': neutral_count,
                'negative': negative_count
            }
        }


# Singleton instance
_sentiment_analyzer = None


def get_sentiment_analyzer():
    """Get or create sentiment analyzer instance"""
    global _sentiment_analyzer
    if _sentiment_analyzer is None:
        _sentiment_analyzer = SentimentAnalyzer()
    return _sentiment_analyzer
