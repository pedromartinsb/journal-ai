"""Core components of Journal AI."""

from .news_agent import NewsAgent
from .news_fetcher import NewsFetcher
from .ai_processor import AIProcessor
from .email_sender import EmailSender

__all__ = ['NewsAgent', 'NewsFetcher', 'AIProcessor', 'EmailSender'] 