import requests
from typing import Dict, Any, Optional
from app.config import settings

class PropagationResult:
    def __init__(self, score: float, article_count: int, sources: list):
        self.score = score  # 0 to 20
        self.article_count = article_count
        self.sources = sources

class PropagationService:
    def __init__(self):
        self.api_key = settings.NEWS_API_KEY
        self.base_url = "https://newsapi.org/v2/everything"

    def analyze(self, query: str) -> PropagationResult:
        """
        Search for recent articles related to the query to estimate propagation.
        """
        if not self.api_key:
            return PropagationResult(score=0, article_count=0, sources=[])

        params = {
            "q": query,
            "apiKey": self.api_key,
            "language": "fr",
            "sortBy": "relevancy",
            "pageSize": 5
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=settings.REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()

            total_results = data.get("totalResults", 0)
            articles = data.get("articles", [])
            
            # Extract distinct source names
            seen_sources = []
            for art in articles:
                source_name = art.get("source", {}).get("name")
                if source_name and source_name not in seen_sources:
                    seen_sources.append(source_name)

            # Scoring logic (Max 20 pts)
            # 0 results: 0 pts
            # 1-3 results: 5 pts
            # 4-10 results: 12 pts
            # > 10 results: 20 pts
            
            score = 0
            if total_results > 10:
                score = 20.0
            elif total_results >= 4:
                score = 12.0
            elif total_results >= 1:
                score = 5.0

            return PropagationResult(
                score=score,
                article_count=total_results,
                sources=seen_sources
            )

        except Exception as e:
            print(f"Error in PropagationService: {e}")
            return PropagationResult(score=0, article_count=0, sources=[])
