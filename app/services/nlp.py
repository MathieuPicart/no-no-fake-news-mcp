import spacy
from typing import List, Dict

class EntityExtractor:
    def __init__(self, model: str = "fr_core_news_sm"):
        try:
            self.nlp = spacy.load(model)
        except Exception:
            try:
                # Try direct import if shortcut link fails
                import fr_core_news_sm
                self.nlp = fr_core_news_sm.load()
            except ImportError as e:
                print(f"Warning: Could not load spacy model {model}. Error: {e}")
                self.nlp = None
        except Exception as e:
            print(f"General error loading spacy: {e}")
            self.nlp = None

    def extract(self, text: str) -> List[Dict[str, str]]:
        """
        Extract named entities from text.
        Returns a list of dicts: {'text': '...', 'label': '...'}
        Labels: PER (Person), ORG (Organization), GPE (Location), etc.
        """
        if not self.nlp or not text:
            return []

        doc = self.nlp(str(text))
        entities = []
        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_
            })
        
        return entities

    def get_keywords(self, text: str) -> List[str]:
        """
        Get a list of unique names/organizations to use for searches.
        """
        entities = self.extract(text)
        # Prioritize PER and ORG for fact-checking
        keywords = set()
        for ent in entities:
            if ent["label"] in ["PER", "ORG", "GPE"]:
                keywords.add(ent["text"])
        
        return list(keywords)
