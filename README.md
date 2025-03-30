# Journal AI

An AI-powered newsletter generator that creates personalized daily newsletters by fetching and summarizing news articles from various sources.

## Features

- Fetches news from multiple sources (Brazilian and international)
- Uses Claude AI to generate concise summaries of articles
- Creates personalized newsletters with categorized content
- Sends newsletters via email
- Configurable news sources and categories
- Support for multiple languages

## Prerequisites

- Python 3.8 or higher
- NewsAPI key
- Anthropic API key (for Claude AI)
- Email server credentials (SMTP)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/journal-ai.git
cd journal-ai
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in development mode:

```bash
pip install -e .
```

## Configuration

Create a `.env` file in the project root with the following variables:

```env
NEWSAPI_KEY=your_newsapi_key
ANTHROPIC_API_KEY=your_anthropic_api_key
SMTP_SERVER=your_smtp_server
SMTP_PORT=587
EMAIL_USERNAME=your_email
EMAIL_PASSWORD=your_password
RECIPIENT_EMAIL=recipient@example.com
```

## Usage

### Command Line Interface

Send a test newsletter:

```bash
journal-ai --test
```

Schedule regular newsletters:

```bash
journal-ai --schedule
```

### Python API

```python
from journal_ai.core.news_agent import NewsAgent

agent = NewsAgent()
agent.generate_and_send_newsletter()
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
