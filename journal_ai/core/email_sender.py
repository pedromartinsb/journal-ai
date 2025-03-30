import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional
from ..config.settings import settings
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

class EmailSender:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.username = settings.EMAIL_USERNAME
        self.password = settings.EMAIL_PASSWORD
        self.recipient = settings.RECIPIENT_EMAIL
    
    def send_newsletter(self, content: str, subject: Optional[str] = None) -> bool:
        """
        Send the newsletter via email.
        
        Args:
            content: Newsletter content
            subject: Email subject (optional)
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not subject:
            subject = f"Daily News Summary - {datetime.now().strftime('%Y-%m-%d')}"
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = self.recipient
            
            # Create HTML content
            html_content = self._create_html_content(content)
            
            # Attach both plain text and HTML versions
            msg.attach(MIMEText(content, 'plain'))
            msg.attach(MIMEText(html_content, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            logger.info("Newsletter sent successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False
    
    def _create_html_content(self, content: str) -> str:
        """Create an HTML version of the newsletter content."""
        # Convert plain text to HTML with basic formatting
        paragraphs = content.split('\n\n')
        html_paragraphs = []
        
        for p in paragraphs:
            if p.strip():  # Skip empty paragraphs
                # Convert newlines to <br> within paragraphs
                p = p.replace('\n', '<br>')
                html_paragraphs.append(f'<p>{p}</p>')
        
        html_content = '\n'.join(html_paragraphs)
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        p {{
            margin-bottom: 15px;
        }}
        a {{
            color: #3498db;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>{paragraphs[0] if paragraphs else 'Daily News Summary'}</h1>
    {html_content}
</body>
</html>""" 