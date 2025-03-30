from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # API Keys
    ANTHROPIC_API_KEY: str
    NEWSAPI_KEY: str
    
    # Email Configuration
    SMTP_SERVER: str
    SMTP_PORT: int
    EMAIL_USERNAME: str
    EMAIL_PASSWORD: str
    RECIPIENT_EMAIL: str
    
    # AI Configuration
    AI_MODEL: str = "claude-3-opus-20240229"  # Using Claude 3 Opus
    
    # Newsletter Configuration
    DELIVERY_TIME: str = "07:00"
    MAX_ARTICLES_PER_CATEGORY: int = 3
    MAX_TOTAL_ARTICLES: int = 15
    
    # News Sources
    BRAZILIAN_SOURCES: List[str] = [
        "globo",
        "info-money",
        "google-news-br"
    ]
    
    INTERNATIONAL_SOURCES: List[str] = [
        "bbc-news",
        "reuters",
        "bloomberg",
        "the-wall-street-journal"
    ]
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)

# Create settings instance
settings = Settings() 