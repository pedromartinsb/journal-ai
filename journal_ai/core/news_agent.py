from typing import Dict, List, Any
from datetime import datetime
import schedule
import time
from ..config.settings import settings
from ..utils.logger import setup_logger
from .news_fetcher import NewsFetcher
from .ai_processor import AIProcessor
from .email_sender import EmailSender

logger = setup_logger(__name__)

class NewsAgent:
    def __init__(self):
        self.news_fetcher = NewsFetcher()
        self.ai_processor = AIProcessor()
        self.email_sender = EmailSender()
    
    def generate_and_send_newsletter(self) -> bool:
        """
        Generate and send the daily newsletter.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Fetch news
            logger.info("Fetching news...")
            news_data = self.news_fetcher.fetch_all_news()
            
            if not news_data:
                logger.warning("No news articles found.")
                return False
            
            # Process news with AI
            logger.info("Processing news with AI...")
            newsletter_content = self.ai_processor.generate_newsletter(
                news_data.get('brazilian_news', []),
                news_data.get('international_news', [])
            )
            
            # Send newsletter
            logger.info("Sending newsletter...")
            success = self.email_sender.send_newsletter(newsletter_content)
            
            if success:
                logger.info("Newsletter sent successfully!")
            else:
                logger.error("Failed to send newsletter.")
            
            return success
            
        except Exception as e:
            logger.error(f"Error generating and sending newsletter: {str(e)}")
            return False
    
    def run_scheduled(self):
        """Run the newsletter generation at the configured time."""
        # Schedule the newsletter generation
        schedule.every().day.at(settings.DELIVERY_TIME).do(self.generate_and_send_newsletter)
        
        logger.info(f"Newsletter agent started. Will send newsletter at {settings.DELIVERY_TIME} daily.")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute 