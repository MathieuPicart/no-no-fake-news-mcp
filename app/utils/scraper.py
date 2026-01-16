import cloudscraper
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any
from app.config import settings

class Content:
    def __init__(self, url: str, title: str, text: str, author: str = None, date: str = None):
        self.url = url
        self.title = title
        self.text = text
        self.author = author
        self.date = date

def extract_content(url: str) -> Optional[Content]:
    """
    Extracts content from a given URL using Cloudscraper (bypasses Cloudflare) and BeautifulSoup.
    """
    try:
        # Create a scraper instance
        scraper = cloudscraper.create_scraper()
        
        # We can still use custom user agent if we want, but cloudscraper manages its own to look like a browser.
        # However, passing our bot UA might flag us again on some sites, so let's trust cloudscraper's default or mix it.
        # For safety/transparency, we can try to append our bot info if possible, but for avoidance, standard browser UA is best.
        # Let's stick to cloudscraper defaults which usually mimic Chrome/Firefox.
        
        response = scraper.get(url, timeout=settings.REQUEST_TIMEOUT)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Basic extraction logic (to be improved for specific sites)
        title = soup.title.string if soup.title else ""
        
        # Try to find main content
        article = soup.find('article')
        if article:
            text = article.get_text(separator=' ', strip=True)
        else:
            # Fallback to all paragraphs
            text = ' '.join([p.get_text() for p in soup.find_all('p')])
            
        # Metadata extraction
        author = None
        
        # 1. Try JSON-LD (Standard for news)
        import json
        ld_json = soup.find_all('script', type='application/ld+json')
        for script in ld_json:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    # Article standard
                    if 'author' in data:
                        a = data['author']
                        if isinstance(a, list) and len(a) > 0:
                            author = a[0].get('name')
                        elif isinstance(a, dict):
                            author = a.get('name')
                if author: break
            except: continue

        # 2. Try OpenGraph or Meta author
        if not author:
            meta_author = soup.find('meta', attrs={'name': 'author'}) or \
                          soup.find('meta', attrs={'property': 'og:article:author'}) or \
                          soup.find('meta', attrs={'name': 'twitter:creator'})
            if meta_author:
                author = meta_author.get('content')

        # 3. Try Common CSS Selectors
        if not author:
            author_tag = soup.select_one('.author, .byline, [rel="author"], .entry-author-name, .c-byline__item')
            if author_tag:
                author = author_tag.get_text(strip=True)
            
        date = None
        # Meta date check
        meta_date = soup.find('meta', attrs={'property': 'article:published_time'}) or \
                    soup.find('meta', attrs={'name': 'pubdate'})
        if meta_date:
            date = meta_date.get('content')

        return Content(url=url, title=title, text=text, author=author, date=date)

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
