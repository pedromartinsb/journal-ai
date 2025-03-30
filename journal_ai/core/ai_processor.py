from anthropic import Anthropic
from ..config.settings import settings
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class AIProcessor:
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-opus-20240229"
        
    def summarize_article(self, article):
        """Summarize an article using Claude."""
        try:
            prompt = f"""Please provide a concise summary of the following article. Focus on the key points and main message:

{article['title']}

{article['content']}

Summary:"""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Error summarizing article: {e}")
            return self._get_fallback_summary(article)
    
    def generate_newsletter(self, br_articles, intl_articles):
        """Generate a newsletter using Claude."""
        try:
            # First, summarize all articles
            for article in br_articles:
                if not article.get('summary'):
                    article['summary'] = self.summarize_article(article)
            
            for article in intl_articles:
                if not article.get('summary'):
                    article['summary'] = self.summarize_article(article)

            prompt = self._create_newsletter_prompt(br_articles, intl_articles)
            
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Error generating newsletter: {e}")
            return self._get_fallback_newsletter()
    
    def _create_newsletter_prompt(self, br_articles, intl_articles):
        """Create a prompt for newsletter generation."""
        br_summaries = "\n\n".join([
            f"Title: {article['title']}\nSummary: {article['summary']}"
            for article in br_articles
        ])
        
        intl_summaries = "\n\n".join([
            f"Title: {article['title']}\nSummary: {article['summary']}"
            for article in intl_articles
        ])
        
        return f"""Please create a newsletter that summarizes the following news articles. 
The newsletter should be divided into two sections: Brazilian News and International News.
Each section should present the information in a clear, engaging, and professional manner.

Brazilian News:
{br_summaries}

International News:
{intl_summaries}

Please format the newsletter with clear sections, proper spacing, and a professional tone.
The summary should be comprehensive yet concise, highlighting the most important aspects of each story."""

    def _get_fallback_summary(self, article):
        """Return a basic summary when AI processing fails."""
        return f"Summary of: {article['title']}\n\nUnable to generate AI summary at this time."

    def _get_fallback_newsletter(self):
        """Return a basic newsletter when AI processing fails."""
        return "We apologize, but we were unable to generate the newsletter at this time. Please try again later." 