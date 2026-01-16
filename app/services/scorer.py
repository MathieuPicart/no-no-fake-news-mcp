from typing import Dict

class Scorer:
    def __init__(self):
        # Weighted points from spec
        # Linguistic: 30
        # Source: 25
        # Fact Check: 25
        # Propagation: 20
        self.weights = {
            'linguistic': 30,
            'source': 25,
            'fact_check': 25,
            'propagation': 20
        }

    def calculate(self, linguistic_score: float, source_score: float, fact_check_score: float = 0, propagation_score: float = 0) -> int:
        """
        Calculates the final credibility score (0-100).
        Inputs are raw scores for each category.
        Linguistic: 0-100 (scaled to 30)
        Source: 0-25 (scaled to 25, or raw?)
        
        Let's unify inputs to be "completion percentage" (0.0 to 1.0) or match the spec's points directly.
        Spec says:
        Emotivity 0-10, Clickbait 0-10, Nuance 0-10 -> Total 30.
        
        Linguistic Analyzer currently returns:
        Emotivity (0-10), Clickbait (0-10). (Missing nuance right now) -> Max 20 points.
        
        Source Checker returns:
        Domain (0-15), Author (0-10). -> Max 25 points.
        
        So the inputs to this function should probably be the sum of points from each module.
        """
        
        # Current implementation assumes inputs are the raw points obtained from modules
        
        total_points = linguistic_score + source_score + fact_check_score + propagation_score
        
        # Ensure bounds 0-100
        return int(max(0, min(100, total_points)))

    def get_verdict(self, score: int) -> Dict[str, str]:
        if score <= 40:
            return {
                "label": "DANGER : TRES SUSPECT", 
                "badge": "🔴 DANGER",
                "color": "#ef4444",
                "message": "Cette analyse révèle des signaux critiques (clickbait fort, source non vérifiée). Ne partagez pas cet article sans vérification approfondie."
            }
        elif score <= 79:
            return {
                "label": "ATTENTION : DOUTEUX",
                "badge": "🟠 ATTENTION", 
                "color": "#f59e0b",
                "message": "Plusieurs éléments manquent de fiabilité (émotivité élevée ou source peu connue). Nous vous conseillons de croiser cette information."
            }
        else:
            return {
                "label": "FIABLE : ANALYSE POSITIVE",
                "badge": "🟢 FIABLE",
                "color": "#10b981",
                "message": "Cette source présente des gages de fiabilité solides. Le ton est neutre et l'information est relayée par des médias reconnus."
            }
