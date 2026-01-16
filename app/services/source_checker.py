from typing import Optional
from app.utils.scraper import Content

class SourceScore:
    def __init__(self, domain_score: float, author_score: float, total: float, domain_name: str, author_name: Optional[str] = None):
        self.domain_score = domain_score # 0-15
        self.author_score = author_score # 0-10
        self.total_score = total # 0-25
        self.domain_name = domain_name
        self.author_name = author_name

class SourceChecker:
    def __init__(self):
        # Placeholder for known domains (Allowlist/Blocklist)
        self.trusted_domains = ['bbc.com', 'reuters.com', 'apnews.com', 'nytimes.com', 'lemonde.fr', 'lefigaro.fr', 'liberation.fr']
        self.suspect_domains = ['theonion.com', 'infowars.com', 'weeklyworldnews.com']
        
        # Mapping for pretty names
        self.pretty_names = {
            'lemonde.fr': 'Le Monde',
            'bbc.com': 'BBC News',
            'reuters.com': 'Reuters',
            'nytimes.com': 'The New York Times',
            'lefigaro.fr': 'Le Figaro',
            'liberation.fr': 'Libération',
            'cnews.fr': 'CNEWS',
            'bfmtv.com': 'BFMTV'
        }
    
    def check(self, content: Content) -> SourceScore:
        domain_score = 7.0 # Neutral start
        
        from urllib.parse import urlparse
        domain = urlparse(content.url).netloc.replace('www.', '')
        
        # Extract base domain name for display
        domain_name = self.pretty_names.get(domain, domain.split('.')[0].capitalize())
        
        if any(d in domain for d in self.trusted_domains):
            domain_score = 15.0
        elif any(d in domain for d in self.suspect_domains):
            domain_score = 0.0
            
        # Author check (0-10)
        author_score = 0.0
        if content.author:
            author_lower = content.author.lower().strip()
            # List of generic/anonymous indicators
            generic_indicators = ['rédaction', 'redaction', 'admin', 'staff', 'correspondant', 'collectif', 'service', 'agence', 'presse', 'anonymous']
            
            if any(indicator in author_lower for indicator in generic_indicators) or len(author_lower) < 3:
                author_score = 5.0 # Intermediate score for generic author
            else:
                author_score = 10.0 # High score for named author
        else:
            author_score = 0.0 # Low score for missing author
            
        total = domain_score + author_score
        
        return SourceScore(
            domain_score=domain_score,
            author_score=author_score,
            total=total,
            domain_name=domain_name,
            author_name=content.author
        )
