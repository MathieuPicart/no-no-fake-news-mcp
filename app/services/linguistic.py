import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import ssl

# Bypass SSL verification for NLTK download (Mac issue)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Download VADER lexicon if not already present
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon', quiet=True)

class LinguisticScore:
    def __init__(self, emotivity: float, clickbait: float, sentiment_label: str, total: float):
        self.emotivity = emotivity
        self.clickbait = clickbait
        self.sentiment_label = sentiment_label # 'Positive', 'Negative', 'Neutral'
        self.total_score = total # 0-100 (Higher is better/less fake)

class LinguisticAnalyzer:
    def __init__(self):
        self.sia = SentimentIntensityAnalyzer()
    
    def analyze(self, text: str, title: str = "") -> LinguisticScore:
        # 1. Sentiment/Emotivity Analysis
        # VADER compound score: -1 (most negative) to +1 (most positive)
        sentiment_scores = self.sia.polarity_scores(text)
        compound = sentiment_scores['compound']
        
        # Calculate "Emotivity" (inverse of neutrality)
        # Higher neg or pos means higher emotivity -> potentially lower credibility if excessive
        emotivity_index = sentiment_scores['neg'] + sentiment_scores['pos']
        # Score 0-10 (0 = very emotional, 10 = neutral/balanced)
        # Typical neutrality is around 0.8-0.9 for news. 
        # If emotivity > 0.3 (meaning neu < 0.7), it's highly emotional.
        # Mapping: Emotivity 0.0 -> 10 pts, 0.4 -> 0 pts.
        emotivity_score = max(0, 10 - (emotivity_index * 25))
        
        sentiment_label = "Neutral"
        if compound >= 0.05: sentiment_label = "Positive"
        elif compound <= -0.05: sentiment_label = "Negative"

        # 2. Clickbait Detection using Title
        clickbait_penalty = 0
        if title:
            # CAPS check (>30% caps)
            caps_count = sum(1 for c in title if c.isupper())
            if len(title) > 0 and (caps_count / len(title)) > 0.3:
                clickbait_penalty += 4
            
            # Execessive punctuation (!!, ???)
            if re.search(r'[?!]{2,}', title):
                clickbait_penalty += 3
                
            # Sensational words
            sensational_words = ['shocking', 'unbelievable', 'secret', 'exposed', 'miracle', 'you won\'t believe']
            if any(w in title.lower() for w in sensational_words):
                clickbait_penalty += 3
        
        clickbait_score = max(0, 10 - clickbait_penalty)
        
        # Weighted Total (just for this module)
        # Let's say 50/50 split for this component
        total = (emotivity_score + clickbait_score) / 2 * 10 # Scale to 100 for this component? 
        # No, the spec says "Analyse linguistique (30 points)"
        # So I return raw scores 0-10, and the Orchestrator/Scorer will weight it.
        # But here I return a local total 0-100 for consistency if needed, or just the parts.
        
        return LinguisticScore(
            emotivity=emotivity_score, # 0-10
            clickbait=clickbait_score, # 0-10
            sentiment_label=sentiment_label,
            total=(emotivity_score + clickbait_score) * 5 # Scale to 100
        )
