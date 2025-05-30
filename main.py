import os
import sys
import dotenv

# Ensure src is in sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.GenerateContent import NewsContentGenerator
from src.publish_news_response import Publisher

# Load environment variables
env_path = os.getenv('ENV_PATH', r'C:\Users\johnj\secure_configs\AgenticResearch\.env')
dotenv.load_dotenv(env_path)

# Get blog ID from environment
BLOG_ID = os.getenv('JRYLE_BLOG_ID')

# Get initial query from config_settings
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
import config_settings

NEWS_HTML_PATH = "news_response.html"

def run_generate_content():
    print("Generating content...")
    generator = NewsContentGenerator(env_path, BLOG_ID, html_file=NEWS_HTML_PATH)
    news_prompt = generator.build_news_prompt(config_settings.initial_query)
    print("Prompt:\n", news_prompt)
    response = generator.generate_content(news_prompt)
    generator.print_response(response)
    html_file = generator.render_html_response(response.text)
    print(f"Generated HTML file: {html_file}")
    return html_file

def run_publish_news_response(html_file=NEWS_HTML_PATH):
    print("Publishing news response...")
    publisher = Publisher(html_file, BLOG_ID)
    publisher.publish()

def main():
    html_file = run_generate_content()
    run_publish_news_response(html_file)

if __name__ == "__main__":
    main()
