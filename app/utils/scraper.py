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
            
        # Metadata extraction placeholders
        author = None 
        # Meta author check
        meta_author = soup.find('meta', attrs={'name': 'author'})
        if meta_author:
            author = meta_author.get('content')
            
        date = None
        # Meta date check
        meta_date = soup.find('meta', attrs={'property': 'article:published_time'})
        if meta_date:
            date = meta_date.get('content')

        return Content(url=url, title=title, text=text, author=author, date=date)

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None
