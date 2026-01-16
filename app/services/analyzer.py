from app.utils.scraper import extract_content
from app.services.linguistic import LinguisticAnalyzer
from app.services.source_checker import SourceChecker
from app.services.fact_checker import FactChecker
from app.services.propagation import PropagationService
from app.services.nlp import EntityExtractor
from app.services.scorer import Scorer
from app.services.cache import CacheManager
from typing import Dict, Any

class NewsAnalyzer:
    def __init__(self):
        self.linguistic = LinguisticAnalyzer()
        self.source_checker = SourceChecker()
        self.fact_checker = FactChecker()
        self.propagation = PropagationService()
        self.nlp = EntityExtractor()
        self.scorer = Scorer()
        self.cache = CacheManager()
        
    async def analyze(self, url: str) -> Dict[str, Any]:
        # 0. Check Cache (NEW)
        cached_result = self.cache.get_analysis(url)
        if cached_result:
            print(f"Cache hit for {url}")
            return cached_result

        # 1. Scraping
        content = extract_content(url)
        if not content:
            raise ValueError(f"Could not extract content from {url}")
            
        # 2. Sequential Processing
        
        # NLP - Extract Entities (NEW)
        entities = self.nlp.extract(content.text[:2000] if content.text else content.title)
        keywords = self.nlp.get_keywords(content.title)
        
        # Linguistic Analysis (Max 20 pts)
        ling_result = self.linguistic.analyze(content.text, content.title)
        
        # Source Analysis (Max 25 pts)
        source_result = self.source_checker.check(content)
        
        # Fact Check Analysis (Max 25 pts)
        fact_result = self.fact_checker.check(content.title)
        
        # Propagation (Max 20 pts) - NEW
        # Use first 2 keywords or title for search
        search_query = " ".join(keywords[:3]) if keywords else content.title
        prop_result = self.propagation.analyze(search_query)
        
        # 3. Scoring
        linguistic_points = ling_result.emotivity + ling_result.clickbait
        source_points = source_result.total_score
        fact_points = fact_result.score
        prop_score = prop_result.score
        
        final_score = self.scorer.calculate(
            linguistic_score=linguistic_points,
            source_score=source_points,
            fact_check_score=fact_points,
            propagation_score=prop_score
        )
        
        # Update Scaling: Now we have 20 (ling) + 25 (source) + 25 (fact) + 20 (prop) = 90 points max
        max_possible = 90
        scaled_score = int((final_score / max_possible) * 100) if final_score > 0 else 0
        
        verdict = self.scorer.get_verdict(scaled_score)
        
        result = {
            "url": url,
            "title": content.title,
            "score": scaled_score, 
            "original_points": final_score,
            "verdict": verdict,
            "entities": entities[:10], # Limit to first 10 for UI
            "details": {
                "linguistic": {
                    "score": linguistic_points,
                    "emotivity": ling_result.emotivity,
                    "clickbait": ling_result.clickbait,
                    "sentiment": ling_result.sentiment_label
                },
                "source": {
                    "name": source_result.domain_name,
                    "author_name": source_result.author_name,
                    "score": source_points,
                    "domain_score": source_result.domain_score,
                    "author_score": source_result.author_score
                },
                "fact_check": {
                    "score": fact_points,
                    "claims": fact_result.claims
                },
                "propagation": {
                    "score": prop_score,
                    "count": prop_result.article_count,
                    "sources": prop_result.sources
                }
            }
        }
        
        # 4. Save to Cache (NEW) - TTL 1h (3600s)
        self.cache.set_analysis(url, result)
        
        return result
