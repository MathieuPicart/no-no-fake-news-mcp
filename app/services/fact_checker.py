import requests
from typing import List, Dict, Any, Optional
from app.config import settings

class FactCheckResult:
    def __init__(self, score: float, claims: List[Dict[str, Any]]):
        self.score = score  # 0 to 25
        self.claims = claims

class FactChecker:
    def __init__(self):
        self.api_key = settings.GOOGLE_FACT_CHECK_API_KEY
        self.base_url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

    def check(self, query: str) -> FactCheckResult:
        """
        Search for fact checks related to a query (usually the article title).
        Returns a score and a list of claims found.
        """
        if not self.api_key:
            return FactCheckResult(score=0, claims=[])

        params = {
            "query": query,
            "key": self.api_key,
            "languageCode": "fr" # Prefer French results
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=settings.REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()

            claims = data.get("claims", [])
            
            # Simple heuristic for scoring:
            # If no claims found: Neutral (we give some default points for "no known debunking")
            # In Phase 2, we give 25 points max.
            # If claims exist, evaluate them. 
            
            if not claims:
                # No debunking found = Neutral/Good signal
                # Let's give 15/25 points if no negative fact-check is found
                return FactCheckResult(score=15.0, claims=[])

            # Evaluate claims
            # Look for ratings like "False", "Fake", "Misleading"
            negative_ratings = ["false", "faux", "trompeur", "misleading", "incorrect", "partially false"]
            found_negative = False

            for claim in claims:
                for review in claim.get("claimReview", []):
                    rating = review.get("textualRating", "").lower()
                    if any(neg in rating for neg in negative_ratings):
                        found_negative = True
                        break
                if found_negative: break

            if found_negative:
                # Highly likely to be fake news if debunked
                return FactCheckResult(score=0.0, claims=claims[:3]) # Limit to top 3
            
            # If claims exist but aren't strictly "False" (maybe "True" or "Unverified")
            return FactCheckResult(score=20.0, claims=claims[:3])

        except Exception as e:
            print(f"Error in FactChecker: {e}")
            return FactCheckResult(score=0, claims=[])
