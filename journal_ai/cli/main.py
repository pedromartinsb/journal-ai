import argparse
import sys
from ..config.settings import settings
from ..core.news_agent import NewsAgent
from ..utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    """Main entry point for the CLI."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='AI News Newsletter Agent')
    parser.add_argument('--test', action='store_true', help='Send a test newsletter immediately')
    args = parser.parse_args()
    
    try:
        # Initialize and run the news agent
        agent = NewsAgent()
        
        if args.test:
            logger.info("Sending test newsletter...")
            agent.generate_and_send_newsletter()
        else:
            logger.info("Starting scheduled newsletter service...")
            agent.run_scheduled()
            
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main() 