from datetime import datetime, timedelta
from typing import List, Dict, Any
from newsapi import NewsApiClient
from ..config.settings import settings
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class NewsFetcher:
    def __init__(self):
        self.api = NewsApiClient(api_key=settings.NEWSAPI_KEY)
        
    def fetch_news(self, sources: List[str], language: str = 'pt') -> List[Dict[str, Any]]:
        """
        Fetch news articles from specific sources.
        
        Args:
            sources: List of news source IDs
            language: Language code (default: 'pt' for Portuguese)
            
        Returns:
            List of news articles
        """
        try:
            # Calculate date range (last 24 hours)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=1)
            
            # Split sources into chunks of 20 (NewsAPI limit)
            source_chunks = [sources[i:i + 20] for i in range(0, len(sources), 20)]
            all_articles = []
            
            for chunk in source_chunks:
                response = self.api.get_everything(
                    sources=','.join(chunk),
                    language=language,
                    from_param=start_date.strftime('%Y-%m-%d'),
                    to=end_date.strftime('%Y-%m-%d'),
                    sort_by='relevancy'
                )
                
                if response['status'] == 'ok':
                    # Format articles before adding them
                    formatted_articles = [self.format_article(article) for article in response['articles']]
                    all_articles.extend(formatted_articles)
            
            # Sort by published date and limit to max articles
            all_articles.sort(key=lambda x: x['published_at'], reverse=True)
            return all_articles[:settings.MAX_ARTICLES_PER_CATEGORY]
            
        except Exception as e:
            logger.error(f"Error fetching news from sources: {str(e)}")
            return []
    
    def fetch_all_news(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Fetch news from all configured sources.
        
        Returns:
            Dictionary mapping categories to lists of articles
        """
        all_news = {}
        
        # Fetch Brazilian news
        logger.info("Fetching Brazilian news...")
        br_articles = self.fetch_news(settings.BRAZILIAN_SOURCES, 'pt')
        if br_articles:
            all_news['brazilian_news'] = br_articles
        
        # Fetch international news
        logger.info("Fetching international news...")
        int_articles = self.fetch_news(settings.INTERNATIONAL_SOURCES, 'en')
        if int_articles:
            all_news['international_news'] = int_articles
        
        return all_news
    
    def format_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format an article for processing.
        
        Args:
            article: Raw article data
            
        Returns:
            Formatted article data
        """
        formatted = {
            'title': article.get('title', ''),
            'description': article.get('description', ''),
            'url': article.get('url', ''),
            'source': article.get('source', {}).get('name', ''),
            'published_at': article.get('publishedAt', ''),
            'content': article.get('content', ''),
            'summary': ''  # This will be filled by the AI processor
        }
        
        # If content is empty, use description as content
        if not formatted['content']:
            formatted['content'] = formatted['description']
        
        return formatted 